from pydantic import ConfigDict, Field, PrivateAttr
from typing import TYPE_CHECKING, Any, List, Union
from uuid import UUID

from .ginas_common_data import GinasCommonData

if TYPE_CHECKING:
    from .substance import Substance


class GinasCommonSubData(GinasCommonData):
    """Base model for common GSRS sub-data fields."""

    model_config = ConfigDict(extra='forbid')
    _parent: 'Substance | None' = PrivateAttr(default=None)
    _json_path: str | None = PrivateAttr(default=None)

    references: Union[List[UUID], None] = Field(
        default=None,
        alias='references',
        title='References',
        description='References',
    )

    def _set_parent(self, parent: 'Substance | None', json_path: str | None = None) -> None:
        self._parent = parent
        self._json_path = self._clean_text(json_path) or None

    def _embedding_document_id(self) -> str:
        return self._clean_text(self._parent.uuid if self._parent else self.uuid)

    def _embedding_root_name(self) -> str:
        if self._parent is not None:
            document_id = self._clean_text(self._parent.uuid)
            root_name = self._clean_text(self._parent._stable_name())
            if root_name:
                return f'Substance {document_id}' if document_id and root_name == document_id else root_name
        root_name = self._clean_text(getattr(self, 'name', None))
        if root_name:
            return root_name
        document_id = self._embedding_document_id()
        return f'Substance {document_id}' if document_id else 'Substance'

    def _embedding_json_path(self, fallback: str) -> str:
        return self._clean_text(self._json_path) or fallback

    def _embedding_references(self, references: Any = None) -> list[str]:
        if self._parent is None:
            return []
        return self._parent._embedding_references(self.references if references is None else references)
