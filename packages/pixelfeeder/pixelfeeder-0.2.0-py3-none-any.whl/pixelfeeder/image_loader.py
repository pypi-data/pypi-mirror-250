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

import abc
import concurrent.futures
import logging
import sys
import threading

from typing import Dict, List

import PIL.Image
import PIL.ImageFile

LOGGER = logging.getLogger(__name__)


class ImageLoaderError(RuntimeError):
    ...


class BaseImageLoader(abc.ABC):
    @abc.abstractmethod
    def open(self, path: str) -> PIL.Image.Image:
        ...

    def clear(self) -> None:
        ...

    def preload(self, paths: List[str]) -> None:
        """ Preload images from list of paths, if applicable with no warranty
        """

    def stop(self) -> None:
        """ Stop routines if applicable
        """

    def _get_image(self, path: str) -> PIL.Image.Image:
        image = PIL.Image.open(path)
        try:
            image.load()
        except OSError as error:
            raise ImageLoaderError(error) from error
        return image

    def open_truncated(self, path: str) -> PIL.Image.Image:
        PIL.ImageFile.LOAD_TRUNCATED_IMAGES = True
        image = self._get_image(path)
        PIL.ImageFile.LOAD_TRUNCATED_IMAGES = False
        return image


class ImageLoader(BaseImageLoader):
    def open(self, path: str) -> PIL.Image.Image:
        return self._get_image(path)


class CachingImageLoader(BaseImageLoader):
    M = 2**20
    max_workers = 3

    def __init__(self, cached_files_limit, debug=False) -> None:
        self._images: Dict[str, PIL.Image.Image] = {}
        self.cached_files_limit = cached_files_limit
        self.debug = debug
        self.lock = threading.Lock()
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers)

    def stop(self) -> None:
        kwargs = {'wait': False}
        if sys.version_info.minor >= 9:
            kwargs['cancel_futures'] = True
        self.executor.shutdown(**kwargs)
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers)

    def get_size(self) -> int:
        with self.lock:
            return sum(len(i.tobytes()) for i in self._images.values())

    def preload(self, paths: List[str]) -> None:
        for path in paths:
            LOGGER.debug(f'Preload {path}')
            fut = self.executor.submit(self._load, path)
            fut.add_done_callback(self.log_future_exception)

    def open(self, path: str) -> PIL.Image.Image:
        image = self._load(path)
        self._trim()
        return image

    @staticmethod
    def log_future_exception(future: concurrent.futures.Future) -> None:
        try:
            exception = future.exception()
        except concurrent.futures.CancelledError:
            LOGGER.info('Preloading task has been cancelled')
            return
        if exception:
            LOGGER.warning(f'Image preloading error: {exception}')

    def _load(self, path: str) -> PIL.Image.Image:
        with self.lock:
            image = self._images.get(path)
        if image is None:
            image = self._get_image(path)
            with self.lock:
                self._images[path] = image
        else:
            LOGGER.debug('"%s" already in cache', path)
        return image

    def _trim(self):
        with self.lock:
            length = len(self._images)
        while length >= self.cached_files_limit:
            with self.lock:
                del_key = list(self._images.keys())[0]
                self._images.pop(del_key)
                length = len(self._images)
            LOGGER.debug('Unload "%s"', del_key)
        if self.debug:
            LOGGER.debug('RAM usage: %i MB', self.get_size() / self.M)

    def clear(self) -> None:
        self._images.clear()
