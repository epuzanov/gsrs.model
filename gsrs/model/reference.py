from pydantic import ConfigDict, Field, PrivateAttr, field_validator
from typing import TYPE_CHECKING, List, Union
from datetime import datetime, timezone

from .ginas_common_sub_data import GinasCommonData

if TYPE_CHECKING:
    from .substance import Substance


class Reference(GinasCommonData):
    """Reference model."""

    model_config = ConfigDict(
        extra='forbid',
        json_encoders={datetime: lambda value: int(value.timestamp() * 1000)},
    )
    _parent: 'Substance | None' = PrivateAttr(default=None)
    _json_path: str | None = PrivateAttr(default=None)

    citation: Union[str, None] = Field(
        default=None,
        alias='citation',
        title='Citation Text',
        description='Citation Text',
    )

    docType: Union[str, None] = Field(
        default=None,
        alias='docType',
        title='Reference Type',
        description='Reference Type',
    )

    documentDate: Union[datetime, None] = Field(
        default=None,
        alias='documentDate',
        title='Date Accessed',
        description='Date Accessed',
    )

    publicDomain: Union[bool, None] = Field(
        default=None,
        alias='publicDomain',
        title='Public Domain Reference',
        description='Public Domain Reference',
    )

    tags: Union[List[str], None] = Field(
        default=None,
        alias='tags',
        title='Tags',
        description='Tags',
    )

    uploadedFile: Union[str, None] = Field(
        default=None,
        alias='uploadedFile',
        title='Uploaded Document',
        description='Uploaded Document',
    )

    id: Union[str, None] = Field(
        default=None,
        alias='id',
        title='Ref_ID',
        description='Ref_ID',
    )

    url: Union[str, None] = Field(
        default=None,
        alias='url',
        title='Reference URL',
        description='Reference URL',
    )

    def _set_parent(self, parent: 'Substance | None', json_path: str | None = None) -> None:
        self._parent = parent
        self._json_path = json_path

    @field_validator('documentDate', mode='before')
    @classmethod
    def _parse_unix_timestamp(cls, value):
        if isinstance(value, (int, float)):
            timestamp = value / 1000 if value > 10_000_000_000 else value
            return datetime.fromtimestamp(timestamp, tz=timezone.utc)
        return value
