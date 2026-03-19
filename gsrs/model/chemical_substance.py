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
        element_property=True,
    )

    structure: GinasChemicalStructure = Field(
        ...,
        alias='structure',
        title='Chemical Structure',
        description='Chemical Structure',
        element_property=True,
    )

    moieties: List[Moiety] = Field(
        ...,
        alias='moieties',
        title='Chemical Moieties',
        description='Chemical Moieties',
        element_property=True,
        min_length=1,
    )
