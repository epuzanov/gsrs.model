from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import List, Union
from datetime import datetime, timezone
from uuid import UUID, uuid4

class GinasCommonData(BaseModel):
    """Base model for common GSRS data fields."""

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


    def model_dump(self, *args, **kwargs):
        kwargs.setdefault('exclude_none', True)
        kwargs.setdefault('by_alias', True)
        return super().model_dump(*args, **kwargs)

    def model_dump_json(self, *args, **kwargs):
        kwargs.setdefault('exclude_none', True)
        kwargs.setdefault('by_alias', True)
        return super().model_dump_json(*args, **kwargs)
