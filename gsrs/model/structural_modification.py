from pydantic import Field, ConfigDict
from typing import Union
from enum import Enum

from .amount import Amount
from .site_container import SiteContainer
from .substance_reference import SubstanceReference

class Extent(Enum):
    """Extent model."""

    COMPLETE = 'COMPLETE'
    PARTIAL = 'PARTIAL'
    UNSPECIFIED = 'Unspecified'

class StructuralModification(SiteContainer):
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

