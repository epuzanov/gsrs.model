from pydantic import ConfigDict, Field, PrivateAttr
from typing import List, Union
from uuid import UUID

from .ginas_common_data import GinasCommonData

class GinasCommonSubData(GinasCommonData):
    """Base model for common GSRS sub-data fields."""

    model_config = ConfigDict(extra='forbid')
    _parentUuid: UUID | None = PrivateAttr(default=None)
    _parentName: str | None = PrivateAttr(default=None)

    references: Union[List[UUID], None] = Field(
        default=None,
        alias='references',
        title='References',
        description='References',
    )

    sitesShorthand: Union[str, None] = Field(
        default=None,
        alias='sitesShorthand',
        title='Sites Shorthand',
        description='Compact system-generated shorthand for the referenced sites.',
    )

    def _set_parent_context(
        self,
        parent_uuid: UUID | None,
        parent_name: str | None = None,
        source_name: str | None = None,
    ) -> None:
        self._parentUuid = parent_uuid
        self._parentName = parent_name
        self._set_source_name(source_name)

    def _embedding_document_id(self) -> str:
        return self._clean_text(self._parentUuid or self.uuid)

    def _embedding_root_name(self) -> str:
        root_name = self._clean_text(self._parentName) or self._clean_text(getattr(self, 'name', None))
        if root_name:
            return root_name
        document_id = self._embedding_document_id()
        return f'Substance {document_id}' if document_id else 'Substance'

    def _embedding_root_metadata(self) -> dict[str, str | None]:
        return {
            'created': self._clean_text(self.created) or None,
            'lastEdited': self._clean_text(self.lastEdited) or None,
        }
