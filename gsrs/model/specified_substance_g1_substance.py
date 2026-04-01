from pydantic import Field, ConfigDict

from .specified_substance_g1 import SpecifiedSubstanceG1
from .substance import Substance


class SpecifiedSubstanceG1Substance(Substance):
    """Specified Substance model."""

    model_config = ConfigDict(extra='forbid')

    specifiedSubstance: SpecifiedSubstanceG1 = Field(
        default=...,
        alias='specifiedSubstance',
        title='specifiedSubstance',
        description='Specified Substance definition for this substance.',
    )
