from pydantic import Field, ConfigDict

from .specified_substance_g1 import SpecifiedSubstanceG1
from .substance import Substance

class SpecifiedSubstanceG1Substance(Substance):
    """Specified Substance model."""

    model_config = ConfigDict(extra='forbid')

    specifiedSubstance: SpecifiedSubstanceG1 = Field(
        ...,
        alias='specifiedSubstance',
        title='specifiedSubstance',
        description='specifiedSubstance',
        element_property=True,
    )
