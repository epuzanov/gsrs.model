from pydantic import Field, ConfigDict

from .mixture import Mixture
from .substance import Substance


class MixtureSubstance(Substance):
    """Mixture Substance model."""

    model_config = ConfigDict(extra='forbid')

    mixture: Mixture = Field(
        default=...,
        alias='mixture',
        title='Mixture',
        description='Mixture definition for this substance.',
    )
