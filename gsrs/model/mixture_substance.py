from pydantic import Field, ConfigDict

from .mixture import Mixture
from .substance import Substance

class MixtureSubstance(Substance):
    """Mixture Substance model."""

    model_config = ConfigDict(extra='forbid')

    mixture: Mixture = Field(
        ...,
        alias='mixture',
        title='Mixture',
        description='Mixture',
        element_property=True,
    )
