from pydantic import ConfigDict, Field, PrivateAttr, field_serializer
from typing import TYPE_CHECKING, List, Union
from uuid import UUID

from .ginas_common_data import GinasCommonData

if TYPE_CHECKING:
    from .substance import Substance


class GinasCommonSubData(GinasCommonData):
    """Base model for common GSRS sub-data fields."""

    model_config = ConfigDict(extra='forbid')
    _parent: 'Substance | None' = PrivateAttr(default=None)
    _json_path: str | None = PrivateAttr(default=None)

    references: List[Union[UUID, str]] = Field(
        default_factory=list,
        alias='references',
        title='References',
        description='References',
    )

    def _set_parent(self, parent: 'Substance | None', json_path: str | None = None) -> None:
        self._parent = parent
        self._json_path = json_path

    @field_serializer('references', when_used='always')
    def _serialize_references(self, value: List[Union[UUID, str]]):
        new_values = []
        for item in value:
            if isinstance(item, UUID):
                new_values.append(str(item))
            elif isinstance(item, str):
                new_values.append(item)
        return new_values
