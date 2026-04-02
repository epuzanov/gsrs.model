from datetime import datetime, timezone
from typing import List, Union
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field, field_validator


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

    def is_public(self) -> bool:
        """Determine if the record is public based on access permissions."""
        return not self.access

    def is_deprecated(self) -> bool:
        """Determine if the record is deprecated."""
        return self.deprecated is True

    def model_dump(self, *args, **kwargs):
        kwargs.setdefault('exclude_none', True)
        kwargs.setdefault('by_alias', True)
        return super().model_dump(*args, **kwargs)

    def model_dump_json(self, *args, **kwargs):
        kwargs.setdefault('exclude_none', True)
        kwargs.setdefault('by_alias', True)
        return super().model_dump_json(*args, **kwargs)
