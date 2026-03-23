from pydantic import Field, ConfigDict
from typing import List, Union

from .ginas_common_sub_data import GinasCommonSubData
from .physical_parameter import PhysicalParameter

class PhysicalModification(GinasCommonSubData):
    """Physical Modification model."""

    model_config = ConfigDict(extra='forbid')

    physicalModificationRole: str = Field(
        ...,
        alias='physicalModificationRole',
        title='Role of Modification',
        description='Role of Modification',
        element_property=True,
    )
    parameters: List[PhysicalParameter] = Field(
        ...,
        alias='parameters',
        title='Physical Parameters',
        description='Physical Parameters',
        element_property=True,
        min_length=1,
    )
    modificationGroup: Union[str, None] = Field(
        None,
        alias='modificationGroup',
        title='Modification Group',
        description='Modification Group',
        element_property=True,
    )

    def to_embedding_chunks(self) -> list[dict[str, object]]:
        subject = self._embedding_root_name()
        document_id = self._embedding_document_id()

        return [
            {
                'chunk_id': f'root_modifications_physicalModifications_uuid:{document_id}',
                'document_id': document_id,
                'source': self._embedding_source_name(),
                'section': 'physicalModifications',
                'content': f'{subject} physical modification role {self._clean_text(self.physicalModificationRole)}.',
                'metadata': {
                    **self._embedding_root_metadata(),
                    **self._hierarchy_metadata('root', 'modifications', 'physicalModifications'),
                    'modification_kind': 'physical',
                },
            }
        ]
