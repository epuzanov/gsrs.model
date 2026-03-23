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
        element_property=True,
    )
    access: Union[List[str], None] = Field(
        None,
        alias='access',
        title='Access',
        description='Access',
        element_property=True,
    )
    deprecated: Union[bool, None] = Field(
        None,
        alias='deprecated',
        title='Deprecated',
        description='Deprecated',
        element_property=True,
    )
    lastEdited: Union[datetime, None] = Field(
        None,
        alias='lastEdited',
        title='Last Modified Date',
        description='Last Modified Date',
        element_property=True,
    )
    lastEditedBy: Union[str, None] = Field(
        None,
        alias='lastEditedBy',
        title='Last Modified By',
        description='Last Modified By',
        element_property=True,
    )
    created: Union[datetime, None] = Field(
        None,
        alias='created',
        title='Creation Date',
        description='Creation Date',
        element_property=True,
    )
    createdBy: Union[str, None] = Field(
        None,
        alias='createdBy',
        title='Created By',
        description='Created By',
        element_property=True,
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

    @classmethod
    def _pick_substance_ref_name(cls, obj: Any) -> str:
        if obj is None:
            return ''
        if isinstance(obj, str):
            return cls._clean_text(obj)
        if isinstance(obj, BaseModel):
            obj = obj.model_dump(by_alias=True, exclude_none=True)
        if isinstance(obj, dict):
            for key in ('refPname', 'name', 'approvalID', 'refuuid', 'linkingID'):
                if obj.get(key):
                    return cls._clean_text(obj[key])
        return cls._clean_text(obj)

    @classmethod
    def _pick_substance_ref_id(cls, obj: Any) -> str:
        if isinstance(obj, BaseModel):
            obj = obj.model_dump(by_alias=True, exclude_none=True)
        if not isinstance(obj, dict):
            return ''
        for key in ('approvalID', 'refuuid', 'linkingID', 'uuid'):
            if obj.get(key):
                return cls._clean_text(obj[key])
        return ''

    @classmethod
    def _render_amount(cls, value: Any) -> str:
        if value is None:
            return ''
        if isinstance(value, BaseModel):
            value = value.model_dump(by_alias=True, exclude_none=True)
        if isinstance(value, dict):
            pieces: list[str] = []
            non_numeric = cls._clean_text(value.get('nonNumericValue'))
            avg = value.get('average')
            low = value.get('low')
            high = value.get('high')
            low_limit = value.get('lowLimit')
            high_limit = value.get('highLimit')
            units = cls._clean_text(value.get('units'))
            amount_type = cls._clean_text(value.get('type'))
            if non_numeric:
                pieces.append(non_numeric)
            elif avg is not None:
                pieces.append(str(avg))
            elif low is not None and high is not None:
                pieces.append(f'{low} to {high}')
            elif low_limit is not None and high_limit is not None:
                pieces.append(f'{low_limit} to {high_limit}')
            elif low is not None:
                pieces.append(str(low))
            elif high is not None:
                pieces.append(str(high))
            if units:
                pieces.append(units)
            if amount_type:
                pieces.append(f'(amount type {amount_type})')
            return ' '.join(pieces).strip()
        return cls._clean_text(value)

    def model_dump(self, *args, **kwargs):
        kwargs.setdefault('exclude_none', True)
        kwargs.setdefault('by_alias', True)
        return super().model_dump(*args, **kwargs)

    def model_dump_json(self, *args, **kwargs):
        kwargs.setdefault('exclude_none', True)
        kwargs.setdefault('by_alias', True)
        return super().model_dump_json(*args, **kwargs)
