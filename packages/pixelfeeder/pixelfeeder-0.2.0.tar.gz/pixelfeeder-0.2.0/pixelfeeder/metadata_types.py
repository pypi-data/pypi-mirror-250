"""
Provides dataclasses.dataclasses for subsets of metadata structs
"""

import dataclasses
import enum

from datetime import datetime
from typing import Any, Dict, List, Optional

from pixelfeeder.tools import DataclassDictMixin

PIXELFED_DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'
FLICKR_DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'


class FlickrVisibility(enum.Enum):
    PUBLIC = 'public'
    FRIENDS_ONLY = 'friends only'
    FAMILY_ONLY = 'family only'
    FRIENDS_AND_FAMILY = 'friends & family'
    PRIVATE = 'private'

    @classmethod
    def from_pixelfed_visibility(cls, visibility: 'PixelfedVisibility') -> 'FlickrVisibility':
        if visibility == PixelfedVisibility.UNLISTED:
            return cls.FRIENDS_ONLY
        elif visibility == PixelfedVisibility.DIRECT:
            return cls.PRIVATE
        return cls(visibility.value)


class PixelfedVisibility(enum.Enum):
    PUBLIC = 'public'
    PRIVATE = 'private'
    UNLISTED = 'unlisted'
    DIRECT = 'direct'

    @classmethod
    def from_flickr_visibility(cls, visibility: FlickrVisibility) -> 'PixelfedVisibility':
        if visibility in (
                FlickrVisibility.FRIENDS_ONLY,
                FlickrVisibility.FAMILY_ONLY,
                FlickrVisibility.FRIENDS_AND_FAMILY):
            return cls.UNLISTED
        return cls(visibility.value)


@dataclasses.dataclass
class FlickrMetadata(DataclassDictMixin):
    """ Partial metadata struct of Flickr exported picture """
    @dataclasses.dataclass
    class Tag(DataclassDictMixin):
        tag: str

    id: int
    name: str
    description: str
    date_taken: str
    original: str
    license: str
    tags: List[Tag]
    privacy: str
    safety: str

    def __str__(self) -> str:
        return f'photo_{self.id}'

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FlickrMetadata':
        data['tags'] = [cls.Tag.from_dict(tag) for tag in data['tags']]
        return super().from_dict(data)

    @staticmethod
    def from_pixelfed_metadata(obj: 'PixelfedMetadata', use_status_id=False) -> List['FlickrMetadata']:
        result = []

        fl_tags = []
        for tag in obj.tags:
            fl_tags.append(FlickrMetadata.Tag(tag=tag.name))
        pf_visib = PixelfedVisibility(obj.visibility)
        privacy = FlickrVisibility.from_pixelfed_visibility(pf_visib).value
        taken_dt = datetime.strptime(obj.created_at, PIXELFED_DATETIME_FORMAT)
        date_taken = taken_dt.strftime(FLICKR_DATETIME_FORMAT)

        for media in obj.media_attachments:
            result.append(FlickrMetadata(
                id=obj.id if use_status_id else media.id,
                name='',
                description=obj.content_text,
                date_taken=date_taken,
                license=media.license.title,  # Format is not exact the same
                original=media.url,
                tags=fl_tags,
                privacy=privacy,
                safety='restricted' if obj.sensitive else 'safe'))

        return result


@dataclasses.dataclass
class PixelfedMetadata(DataclassDictMixin):
    """ Partial metadata struct of Pixelfed status """
    @dataclasses.dataclass
    class Media(DataclassDictMixin):
        @dataclasses.dataclass
        class License(DataclassDictMixin):
            id: int
            title: str

        id: int
        type: str
        url: str
        preview_url: str
        description: Optional[str]
        license: License
        is_nsfw: int
        orientation: str

        @classmethod
        def from_dict(cls, data: Dict[str, Any]) -> 'PixelfedMetadata.Media':
            data['license'] = cls.License.from_dict(data['license'])
            return super().from_dict(data)

    @dataclasses.dataclass
    class Tag(DataclassDictMixin):
        name: str

    id: int
    url: str
    content: str
    content_text: str
    created_at: str
    sensitive: bool
    visibility: str
    media_attachments: List[Media]
    tags: List[Tag]

    def __str__(self) -> str:
        return f'status_{self.id}'

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PixelfedMetadata':
        data['media_attachments'] = [cls.Media.from_dict(media) for media in data['media_attachments']]
        data['tags'] = [cls.Tag.from_dict(tag) for tag in data['tags']]
        return super().from_dict(data)
