from pydantic import Field, ConfigDict
from typing import List, Union
from enum import Enum

from .amount import Amount
from .ginas_common_sub_data import GinasCommonSubData
from .site import Site
from .substance_reference import SubstanceReference

class Extent(Enum):
    """Extent model."""

    COMPLETE = 'COMPLETE'
    PARTIAL = 'PARTIAL'
    UNSPECIFIED = 'Unspecified'

class StructuralModification(GinasCommonSubData):
    """Structural Modification model."""

    model_config = ConfigDict(extra='forbid')

    structuralModificationType: str = Field(
        ...,
        alias='structuralModificationType',
        title='Modification Type',
        description='Modification Type',
        element_property=True,
    )
    locationType: Union[str, None] = Field(
        None,
        alias='locationType',
        title='Modification Location Type',
        description='Modification Location Type',
        element_property=True,
    )
    residueModified: Union[str, None] = Field(
        None,
        alias='residueModified',
        title='Residue Modified',
        description='Residue Modified',
        element_property=True,
    )
    sites: Union[List[Site], None] = Field(
        None,
        alias='sites',
        title='Modified Sites',
        description='Modified Sites',
        element_property=True,
    )
    extent: Union[Extent, None] = Field(
        None,
        alias='extent',
        title='Extent',
        description='Extent',
        element_property=True,
    )
    extentAmount: Union[Amount, None] = Field(
        None,
        alias='extentAmount',
        title='Amount',
        description='Amount',
        element_property=True,
    )
    molecularFragment: Union[SubstanceReference, None] = Field(
        None,
        alias='molecularFragment',
        title='Molecular Fragment',
        description='Molecular Fragment',
        element_property=True,
    )
    molecularFragmentRole: Union[str, None] = Field(
        None,
        alias='molecularFragmentRole',
        title='Molecular Fragment Role',
        description='Molecular Fragment Role',
        element_property=True,
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
                'chunk_id': f'root_modifications_structuralModifications_uuid:{document_id}',
                'document_id': document_id,
                'source': self._embedding_source_name(),
                'section': 'structuralModifications',
                'content': f'{subject} structural modification type {self._clean_text(self.structuralModificationType)}.',
                'metadata': {
                    **self._embedding_root_metadata(),
                    **self._hierarchy_metadata('root', 'modifications', 'structuralModifications'),
                    'modification_kind': 'structural',
                },
            }
        ]
