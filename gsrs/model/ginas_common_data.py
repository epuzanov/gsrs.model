import json
import re
from datetime import datetime, timezone
from typing import Any, List, Union
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field, PrivateAttr, field_validator


class GinasCommonData(BaseModel):
    """Base model for common GSRS data fields."""

    _source_name: str | None = PrivateAttr(default=None)

    model_config = ConfigDict(
        extra='forbid',
        json_encoders={datetime: lambda value: int(value.timestamp() * 1000)},
    )

    uuid: Union[UUID, None] = Field(
        default_factory=uuid4,
        alias='uuid',
        title='Uuid',
        description='Uuid',
    )
    access: Union[List[str], None] = Field(
        default=None,
        alias='access',
        title='Access',
        description='Access',
    )
    deprecated: Union[bool, None] = Field(
        default=None,
        alias='deprecated',
        title='Deprecated',
        description='Deprecated',
    )
    lastEdited: Union[datetime, None] = Field(
        default=None,
        alias='lastEdited',
        title='Last Modified Date',
        description='Last Modified Date',
    )
    lastEditedBy: Union[str, None] = Field(
        default=None,
        alias='lastEditedBy',
        title='Last Modified By',
        description='Last Modified By',
    )
    created: Union[datetime, None] = Field(
        default=None,
        alias='created',
        title='Creation Date',
        description='Creation Date',
    )
    createdBy: Union[str, None] = Field(
        default=None,
        alias='createdBy',
        title='Created By',
        description='Created By',
    )

    @field_validator('created', 'lastEdited', mode='before')
    @classmethod
    def _parse_unix_timestamp(cls, value):
        if isinstance(value, (int, float)):
            timestamp = value / 1000 if value > 10_000_000_000 else value
            return datetime.fromtimestamp(timestamp, tz=timezone.utc)
        return value

    @staticmethod
    def _clean_text(value: Any) -> str:
        if value is None:
            return ''
        if isinstance(value, BaseModel):
            value = value.model_dump(by_alias=True, exclude_none=True)
        if isinstance(value, (dict, list)):
            value = json.dumps(value, ensure_ascii=False, sort_keys=True)
        if isinstance(value, datetime):
            value = value.isoformat()
        text = str(value).replace('\r', ' ').replace('\n', ' ')
        return re.sub(r'\s+', ' ', text).strip()

    @classmethod
    def _chunk_metadata(cls, root_substance: 'GinasCommonData') -> dict[str, Any]:
        return {
            'created': cls._clean_text(getattr(root_substance, 'created', None)) or None,
            'lastEdited': cls._clean_text(getattr(root_substance, 'lastEdited', None)) or None,
        }

    @classmethod
    def _hierarchy_metadata(cls, *parts: Any) -> dict[str, Any]:
        hierarchy = [cls._clean_text(part) for part in parts if cls._clean_text(part)]
        return {
            'hierarchy': hierarchy,
            'hierarchy_path': ' > '.join(hierarchy),
            'hierarchy_level': len(hierarchy),
        }

    def _set_source_name(self, value: str | None) -> None:
        self._source_name = self._clean_text(value) or None

    def _embedding_source_name(self) -> str | None:
        return self._clean_text(self._source_name) or None

    def model_dump(self, *args, **kwargs):
        kwargs.setdefault('exclude_none', True)
        kwargs.setdefault('by_alias', True)
        return super().model_dump(*args, **kwargs)

    def model_dump_json(self, *args, **kwargs):
        kwargs.setdefault('exclude_none', True)
        kwargs.setdefault('by_alias', True)
        return super().model_dump_json(*args, **kwargs)
