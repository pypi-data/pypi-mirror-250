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

import dataclasses
import logging
import mimetypes
import os

from numbers import Real
from pathlib import Path
from types import TracebackType
from typing import Any, Dict, Generator, List, Optional, Type, Union
from urllib.parse import urlparse

import yaml

LOGGER = logging.getLogger(__name__)

PathUnion = Union[str, os.PathLike]
ENCODING = 'UTF-8'


class NumericKwargs(dict):
    def _calc(self, operator: str, other: float) -> 'NumericKwargs':
        result = {}
        for key, val in self.items():
            if isinstance(val, Real):
                if operator == '*':
                    new_val = val * other
                elif operator == '/':
                    new_val = val / other
                else:
                    raise AssertionError(f'Unknown operator {operator}')
            else:
                new_val = val
            result[key] = new_val
        return NumericKwargs(result)

    def __mul__(self, other: float) -> 'NumericKwargs':
        return self._calc('*', other)

    def __div__(self, other: float) -> 'NumericKwargs':
        return self._calc('*', other)


class Retry:
    """
    Helper to retry operation

    Usage:

    for attempt in Retry(3, MyExceptionType):
        with attempt:
            operation()
    """
    class MaxRetriesExceeded(RuntimeError):
        ...

    class Attempt:
        def __init__(self) -> None:
            self.exc_type: Optional[Type[Exception]] = None
            self.exc: Optional[Exception] = None

        def __enter__(self):
            ...

        def __exit__(self, exc_type: Type[Exception], exc_value: Exception, traceback: TracebackType) -> bool:
            self.exc_type = exc_type
            self.exc = exc_value
            return True

    def __init__(self, max_retries=3, skip_exception=Exception) -> None:
        """
        :param max_retries: Amount of attempts before fail
        :param skip_exception: If operation raises exception of this type or subtype, retry.
            Other exceptions will not be catched.
        """
        self.max_retries = max_retries
        self.skip_exception = skip_exception

    def __iter__(self) -> Generator[Attempt, None, None]:
        for i in range(1, self.max_retries + 1):
            attempt = self.Attempt()
            yield attempt
            if attempt.exc is None:
                return
            assert attempt.exc_type is not None
            if not issubclass(attempt.exc_type, self.skip_exception):
                raise attempt.exc
            LOGGER.warning('Error: %s', str(attempt.exc))
            LOGGER.warning(f'Retry {i}')
        raise Exception(f'Failed after {self.max_retries} retries')


@dataclasses.dataclass
class DataclassDictMixin:
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Any:
        field_names = {field.name for field in dataclasses.fields(cls)}
        filtered_data = {key: val for key, val in data.items() if key in field_names}
        return cls(**filtered_data)

    def to_dict(self) -> Dict[str, Any]:
        return dataclasses.asdict(self)


def filename_from_url(url: str) -> str:
    """ Get filename part of URL """
    path = urlparse(url).path
    return Path(path).name


def metadata_file_predicate(file_path: Path) -> bool:
    """ Check if a file type matches metadata file
    """
    filename = file_path.name.lower()
    mimetype, _enc = mimetypes.guess_type(file_path)
    return mimetype == 'application/json' and filename.startswith('photo_')


def photo_file_predicate(file_path: Path) -> bool:
    """ Check if a file type matches appropirate photo format
    """
    mimetype, _enc = mimetypes.guess_type(file_path)
    return mimetype in {'image/jpeg', 'image/png'}


def get_file_paths(path: PathUnion) -> List[Path]:
    """ Traverse the path and return list of file paths
    """
    result = []
    for root, _dirs, files in os.walk(top=Path(path)):
        root_path = Path(root)
        for filename in files:
            result.append(root_path / filename)
    return result


def prepare_string(value: Any) -> str:
    assert isinstance(value, str)
    return value.strip()


def load_config(file_path: PathUnion, create_missing=False) -> Dict[str, Any]:
    file_path_casted = Path(file_path)
    if create_missing:
        file_path_casted.parent.mkdir(parents=True, exist_ok=True)
        file_path_casted.touch()
    with open(file_path_casted, 'r', encoding=ENCODING) as conf_file:
        return yaml.safe_load(conf_file) or {}


def save_config(file_path: PathUnion, data: Dict, create_missing=False) -> None:
    file_path_casted = Path(file_path)
    if create_missing:
        file_path_casted.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path_casted, 'w', encoding=ENCODING) as conf_file:
        yaml.dump(data, conf_file)


class ValidationError(RuntimeError):
    ...


def validate_timeout(val: Any) -> float:
    """ Return validated value or raises ValidationError """
    try:
        val = float(val)
    except ValueError as err:
        raise ValidationError(err)
    if val <= 0.0:
        raise ValidationError('Expect positive value')
    return val


def validate_url(val: Any) -> str:
    """ Return validated value or raises ValidationError """
    VALID_SCHEMES = ('http://', 'https://')
    VALID_SCH_STR = ', '.join(VALID_SCHEMES)
    try:
        val = str(val)
    except ValueError as err:
        raise ValidationError(err)
    lc_val = val.lower()
    if not any([lc_val.startswith(scheme) for scheme in VALID_SCHEMES]):
        raise ValidationError(f'URL with unsupported schema, expected {VALID_SCH_STR}')
    return val


def validate_path_exists(arg: str) -> Path:
    if (file := Path(arg)).exists():
        return file
    raise FileNotFoundError(f'Path "{file}" does not exist')
