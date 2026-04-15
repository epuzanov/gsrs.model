from datetime import datetime, timezone
from typing import List, Union
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field, field_validator

from ._serialization import dump_json, exclude_non_public_elements


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

    def model_dump(self, *args, exclude_non_public: bool = False, **kwargs):
        kwargs.setdefault('exclude_none', True)
        kwargs.setdefault('by_alias', True)
        if exclude_non_public:
            exclude_none = kwargs.get('exclude_none', False)
            filtered_kwargs = dict(kwargs)
            filtered_kwargs['exclude_none'] = False
            data = super().model_dump(*args, **filtered_kwargs)
            return exclude_non_public_elements(data, exclude_none=exclude_none)
        return super().model_dump(*args, **kwargs)

    def model_dump_json(self, *args, exclude_non_public: bool = False, **kwargs):
        kwargs.setdefault('exclude_none', True)
        kwargs.setdefault('by_alias', True)
        if exclude_non_public:
            indent = kwargs.pop('indent', None)
            ensure_ascii = kwargs.pop('ensure_ascii', False)
            data = self.model_dump(*args, mode='json', exclude_non_public=True, **kwargs)
            return dump_json(data, indent=indent, ensure_ascii=ensure_ascii)
        return super().model_dump_json(*args, **kwargs)
