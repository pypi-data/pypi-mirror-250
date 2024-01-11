# Copyright 2023-2024 Anton Karmanov
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# This file is a part of Pixelfeeder utility. Pixelfeeder helps to migrate data
# from Flickr to a Pixelfed instance.

import asyncio
import json
import logging
import mimetypes
import ssl

from pathlib import Path
from pprint import pformat
from typing import Any, Dict, Generator, List, Optional

import httpx

from pixelfeeder.metadata_types import PixelfedVisibility
from pixelfeeder.tools import PathUnion, filename_from_url

LOGGER = logging.getLogger(__name__)
StatusType = Dict[str, Any]


class PixelfedClientError(RuntimeError):
    ...


class PixelfedClientConnectionError(PixelfedClientError):
    ...


class PixelfedClientRequestError(PixelfedClientError):
    ...


class HttpClient:
    """
    Pixelfed API client

    Client supports generic REST API methods with token-based authentication.

    'a' prifix in names of methods means async.
    '_api' postfix means method takes endpoint like 'statuses' against of full-qualified URLs.
    """

    def __init__(self,  timeout: Optional[float] = None, strict_ssl=True) -> None:
        self._client_kwargs = {'verify': strict_ssl, 'timeout': timeout}

    async def aget(
        self,
        url: str,
        headers: Optional[Dict] = None,
        params: Optional[Dict] = None,
    ) -> httpx.Response:
        """ Plain HTTP GET """
        return await self._request(method='GET', headers=headers, url=url, params=params)

    def get(
        self,
        url: str,
        headers: Optional[Dict] = None,
        params: Optional[Dict] = None,
    ) -> httpx.Response:
        """ Plain HTTP GET """
        return asyncio.run(self.aget(url=url, headers=headers, params=params))

    async def apost(
        self,
        url: str,
        headers: Optional[Dict] = None,
        data: Optional[Dict] = None,
        files: Optional[Dict] = None
    ) -> httpx.Response:
        """ POST request to endpoint with auth """
        return await self._request('POST', url=url, headers=headers, data=data, files=files)

    async def post(
        self,
        url: str,
        headers: Optional[Dict] = None,
        data: Optional[Dict] = None,
        files: Optional[Dict] = None
    ) -> httpx.Response:
        """ POST request to endpoint with auth """
        coro = self.apost(url=url, headers=headers, data=data, files=files)
        return asyncio.run(coro)

    async def _request(
            self,
            method: str,
            url: str,
            headers: Optional[Dict] = None,
            params: Optional[Dict] = None,
            data: Optional[Dict] = None,
            files: Optional[Dict] = None) -> httpx.Response:
        try:
            async with httpx.AsyncClient(**self._client_kwargs) as client:
                resp = await client.request(
                    method=method,
                    url=url,
                    headers=headers,
                    params=params,
                    data=data,
                    files=files)
        except (httpx.HTTPError, ssl.SSLCertVerificationError) as error:
            msg = str(error)
            if not msg:
                msg = type(error).__name__
            raise PixelfedClientConnectionError(msg) from error

        content_type = resp.headers.get('content-type', '')

        LOGGER.debug('Response headers:\n' + pformat(dict(resp.headers), indent=2))
        if content_type.lower() == 'application/json':
            data = resp.json()
            LOGGER.debug('Response content:\n' + json.dumps(data, indent=2))
        elif content_type.lower() == 'application/xml':
            LOGGER.debug('Response content:\n' + resp.content.decode())
        else:
            LOGGER.debug(f'Response content len is {len(resp.content)}')

        try:
            resp.raise_for_status()
        except httpx.HTTPStatusError as error:
            raise PixelfedClientRequestError(error) from error

        return resp


class PixelfedClientBase:
    MASTODON_API = '/api/v1/'
    PIXELFED_API = '/api/pixelfed/v1/'

    def __init__(self, http_client: HttpClient, base_url: str, token: str) -> None:
        self.http_client = http_client
        self.base_url = base_url
        self.headers_auth = {
            'Authorization': f"Bearer {token}",
        }
        self.headers_api = self.headers_auth.copy()
        self.headers_api['Accept'] = 'application/json'

    def endpoint_mastodon(self, endpoint: str) -> str:
        """ Get full-qualified URL from endpoint """
        return self.base_url + self.MASTODON_API + endpoint.strip('/')

    def endpoint_pixelfed(self, endpoint: str) -> str:
        """ Get full-qualified URL from endpoint """
        return self.base_url + self.PIXELFED_API + endpoint.strip('/')


class PixelfedUploader(PixelfedClientBase):
    """ Tool to create statuses with media """
    async def _post_media(self, file_path: PathUnion) -> str:
        with open(file_path, 'rb') as file:
            media = file.read()

        mimetype, _enc = mimetypes.guess_type(file_path)

        files_payload = {
            'file': (file_path, media, mimetype),
        }
        resp = await self.http_client.apost(
            url=self.endpoint_mastodon('media'),
            headers=self.headers_api,
            files=files_payload)
        media_id = resp.json()['id']
        return media_id

    async def _post_status(self, media_ids: List[str], caption='', visibility=PixelfedVisibility.PUBLIC) -> str:
        data = {
            'status': caption,
            'media_ids[]': media_ids,
            'sensitive:': False,  # Seems ignored
            'visibility': visibility.value,
        }
        resp = await self.http_client.apost(
                self.endpoint_mastodon('statuses'),
                headers=self.headers_api,
                data=data)
        return resp.json()['url']

    async def acreate_post(self, file_path: PathUnion, caption='', visibility=PixelfedVisibility.PUBLIC) -> str:
        media_id = await self._post_media(file_path)
        result = await self._post_status([media_id], caption, visibility)
        return result

    def create_post(self, file_path: PathUnion, caption='', visibility=PixelfedVisibility.PUBLIC) -> str:
        coro = self.acreate_post(file_path, caption, visibility)
        return asyncio.run(coro)


class PixelfedExporter(PixelfedClientBase):
    """ Tool to obtain user's satatuses and media """

    LIST_STATUSES_LIMIT = 20  # Mastodon docs declares 40 as a ceil, api/pixelfed reports max 24

    def __init__(self, *args, **kwargs) -> None:
        self.__user_id: Optional[int] = None
        super().__init__(*args, **kwargs)

    @property
    def user_id(self) -> int:
        """ DB ID of the owner of the token """
        if self.__user_id is None:
            resp = self.http_client.get(
                url=self.endpoint_mastodon('accounts/verify_credentials'),
                headers=self.headers_api)
            self.__user_id = int(resp.json()['id'])
            LOGGER.debug(f'Got from server owner of token ID {self.__user_id}')
        return self.__user_id

    def list_statuses(
        self,
        since_id: Optional[int] = None,
        max_id: Optional[int] = None
    ) -> Generator[StatusType, None, None]:
        """
        Get all statuses of the user

        Statuses goes from higher ID to lower ID, from later to older. To start
        after some higher ID and stop before some lower ID, pass since_id and
        max_id args.

        Lazy returns statuses one-by-one lazy requesting bunches of maximum
        self.LIST_STATUSES_LIMIT.

        Returns no reblogs and no statuses without media (even if any).
        status['media_attachments'][0]['url'] is URL of first picture of a status.

        :param since_id: Lower bound of status ID
        :param max_id: Upper bound of status ID
        :return: Status dicts
        """
        stat_list = self._list_statuses(max_id=max_id)
        while stat_list:
            for s in stat_list:
                status_id = int(s['id'])
                if since_id is not None and status_id <= since_id:
                    return
                yield s
            new_max_id = status_id
            stat_list = self._list_statuses(max_id=new_max_id)

    def _list_statuses(self, max_id: Optional[int] = None) -> List[StatusType]:
        url = self.endpoint_pixelfed(f'/accounts/{self.user_id}/statuses')
        params = {
            'only_media': True,
            'limit': self.LIST_STATUSES_LIMIT,
            'exclude_reblogs': True,
        }
        if max_id is not None:
            params['max_id'] = max_id
        resp = self.http_client.get(
                url=url,
                headers=self.headers_api,
                params=params)
        result = resp.json()
        LOGGER.debug(f'Got from server {len(result)} status records')
        return result

    async def aget_media(self, url: str, directory: PathUnion, overwrite=False) -> Path:
        """ Save file by ULR into directory and get a local path """
        directory = Path(directory)
        directory.mkdir(parents=True, exist_ok=True)
        filename = filename_from_url(url)
        file_path = directory/filename
        if file_path.exists() and not overwrite:
            LOGGER.info('File %s exists, skip downloading', str(file_path))
            return file_path

        resp = await self.http_client.aget(url)

        with open(file_path, 'wb') as file:
            file.write(resp.content)

        LOGGER.debug(f'Wrote {file_path}')

        return file_path

    def get_media(self, url: str, directory: PathUnion, overwrite=False) -> Path:
        """ Save file by ULR into directory and get a local path """
        coro = self.aget_media(url=url, directory=directory, overwrite=overwrite)
        return asyncio.run(coro)
