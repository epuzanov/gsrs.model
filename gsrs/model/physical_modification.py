from pydantic import Field, ConfigDict
from typing import List, Union

from .ginas_common_sub_data import GinasCommonSubData
from .physical_parameter import PhysicalParameter

class PhysicalModification(GinasCommonSubData):
    """Physical Modification model."""

    model_config = ConfigDict(extra='forbid')

    physicalModificationRole: str = Field(
        default=...,
        alias='physicalModificationRole',
        title='Role of Modification',
        description='Role of Modification',
    )
    parameters: List[PhysicalParameter] = Field(
        default=...,
        alias='parameters',
        title='Physical Parameters',
        description='Physical Parameters',
        min_length=1,
    )
    modificationGroup: Union[str, None] = Field(
        default=None,
        alias='modificationGroup',
        title='Modification Group',
        description='Modification Group',
    )

    def to_embedding_chunks(self) -> list[dict[str, object]]:
        subject = self._embedding_root_name()
        document_id = self._embedding_document_id()

        return [
            {
                'chunk_id': f'root_modifications_physicalModifications_uuid:{document_id}',
                'document_id': document_id,
                'source_url': self._embedding_source_name(),
                'section': 'physicalModifications',
                'text': f'{subject} physical modification role {self._clean_text(self.physicalModificationRole)}.',
                'metadata': {
                    **self._embedding_root_metadata(),
                    **self._hierarchy_metadata('root', 'modifications', 'physicalModifications'),
                    'modification_kind': 'physical',
                },
            }
        ]
