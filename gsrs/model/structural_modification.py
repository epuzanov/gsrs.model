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
        default=...,
        alias='structuralModificationType',
        title='Modification Type',
        description='Modification Type',
    )
    locationType: Union[str, None] = Field(
        default=None,
        alias='locationType',
        title='Modification Location Type',
        description='Modification Location Type',
    )
    residueModified: Union[str, None] = Field(
        default=None,
        alias='residueModified',
        title='Residue Modified',
        description='Residue Modified',
    )
    sites: Union[List[Site], None] = Field(
        default=None,
        alias='sites',
        title='Modified Sites',
        description='Modified Sites',
    )
    extent: Union[Extent, None] = Field(
        default=None,
        alias='extent',
        title='Extent',
        description='Extent',
    )
    extentAmount: Union[Amount, None] = Field(
        default=None,
        alias='extentAmount',
        title='Amount',
        description='Amount',
    )
    molecularFragment: Union[SubstanceReference, None] = Field(
        default=None,
        alias='molecularFragment',
        title='Molecular Fragment',
        description='Molecular Fragment',
    )
    molecularFragmentRole: Union[str, None] = Field(
        default=None,
        alias='molecularFragmentRole',
        title='Molecular Fragment Role',
        description='Molecular Fragment Role',
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
                'chunk_id': f'root_modifications_structuralModifications_uuid:{self.uuid}',
                'document_id': document_id,
                'source_url': self._embedding_source_name(),
                'section': 'structuralModifications',
                'text': f'{subject} structural modification type {self._clean_text(self.structuralModificationType)}.',
                'metadata': {
                    **self._embedding_root_metadata(),
                    **self._hierarchy_metadata('root', 'modifications', 'structuralModifications'),
                    'modification_kind': 'structural',
                },
            }
        ]
