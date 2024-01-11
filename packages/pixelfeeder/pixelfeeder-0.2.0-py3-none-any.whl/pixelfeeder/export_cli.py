# Copyright 2023 Anton Karmanov
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

import argparse
import json
import logging

from pathlib import Path

import argcomplete

from pixelfeeder.metadata_types import FlickrMetadata, PixelfedMetadata
from pixelfeeder.pixelfed_client import HttpClient, PixelfedExporter, PixelfedClientError
from pixelfeeder.tools import load_config, Retry


LOGGER = logging.getLogger(__name__)
DESCRIPTION = '''
Download pictures and save metadata in subdirs of selected --output-dir from Pixelfed instance.
Does not download image, if media file already exists.

Command saves Pixelfed origin posts metadata and also Flickr-like formatted metadata to upload
with pixelfeeder.
'''


def get_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog='pixelfeeder-export',
        usage='Save Pixelfed user statuses locally',
        description=DESCRIPTION,
        epilog=None)

    parser.add_argument(
        '--upper-id',
        help='Get statues with ID only lesser than',
        type=int)
    parser.add_argument(
        '--lower-id',
        help='Get statues with ID only greater than',
        type=int)
    parser.add_argument(
        '-d', '--output-dir',
        help='Path to save files, will be created if not exists',
        type=Path,
        required=True)
    parser.add_argument(
        '-c', '--config-file',
        type=Path,
        default=Path('config.yaml'),
        help='Settings file with a base URL and a token at least')
    parser.add_argument(
        '-t', '--timeout',
        type=float,
        help='HTTP requests timeout, sec')
    parser.add_argument(
        '-v', '--verbose',
        help='More information to stdout/stderr',
        action='store_true')
    parser.add_argument(
        '--ignore-ssl-verify',
        help='Skip SSL verification for the Pixelfed instance',
        action='store_true')
    parser.add_argument(
        '--skip-media',
        help='Skip downloading images, only save metadata files',
        action='store_true')

    argcomplete.autocomplete(parser)
    return parser


def get_retry_media(exporter: PixelfedExporter, url: str, directory: Path) -> Path:
    for attempt in Retry(3, PixelfedClientError):
        with attempt:
            result = exporter.get_media(url=url, directory=directory)
    return result


def main() -> None:
    args = get_argparser().parse_args()
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)

    conf = load_config(args.config_file)
    base_url = conf['instance']
    token = conf['token']
    strict_ssl = not (args.ignore_ssl_verify or conf.get('ignore_ssl_verify', False))
    timeout = args.timeout
    if timeout is None:
        timeout = conf.get('timeout')
    output_dir = args.output_dir

    http_client = HttpClient(strict_ssl=strict_ssl, timeout=timeout)
    exporter = PixelfedExporter(http_client, base_url=base_url, token=token)

    pf_dir = output_dir/'metadata'
    pf_dir.mkdir(exist_ok=True, parents=True)
    flickr_dir = output_dir/'metadata_flickr'
    flickr_dir.mkdir(exist_ok=True, parents=True)
    media_dir = args.output_dir/'media'

    # TODO Use ThreadPool, recheck time
    # 10m15.3s for 313 M from pxlmo.net
    for stat in exporter.list_statuses(since_id=args.lower_id, max_id=args.upper_id):
        attachments = stat['media_attachments']
        stat_id = int(stat['id'])
        for media in attachments:
            pf_meta_path = pf_dir/f'status_{stat_id}.json'
            with open(pf_meta_path, 'w') as file:
                json.dump(stat, file, indent=2)
            LOGGER.debug('Wrote %s', str(pf_meta_path))
            if not args.skip_media:
                get_retry_media(exporter, url=media['url'], directory=media_dir)

        pf_meta = PixelfedMetadata.from_dict(stat)
        # Non-uniq ids with use_status_id, but better ordering
        fl_meta_lst = FlickrMetadata.from_pixelfed_metadata(pf_meta, use_status_id=True)
        for i, fl_meta in enumerate(fl_meta_lst):
            flickr_meta_path = flickr_dir/f'photo_{stat_id}-{i}.json'
            with open(flickr_meta_path, 'w') as file:
                json.dump(fl_meta.to_dict(), file, indent=2)
            LOGGER.debug('Wrote %s', str(flickr_meta_path))

        LOGGER.info('Status ID %i with %i media attachments has been processed', stat_id, len(attachments))


if __name__ == '__main__':
    main()
