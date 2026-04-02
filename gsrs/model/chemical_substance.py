from pydantic import Field, ConfigDict
from typing import List

from .ginas_chemical_structure import GinasChemicalStructure
from .moiety import Moiety
from .substance import Substance, SubstanceClass


class ChemicalSubstance(Substance):
    """Chemical Substance model."""

    model_config = ConfigDict(extra='forbid')

    substanceClass: SubstanceClass = Field(
        SubstanceClass.chemical,
        alias='substanceClass',
        title='Substance Type',
        description='Substance Type',
    )

    structure: GinasChemicalStructure = Field(
        default=...,
        alias='structure',
        title='Chemical Structure',
        description='Chemical Structure definition for this substance.',
    )

    moieties: List[Moiety] = Field(
        default=...,
        alias='moieties',
        title='Chemical Moieties',
        description='Chemical Moieties',
        min_length=1,
    )
