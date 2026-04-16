from pydantic import Field, ConfigDict

from .polymer import Polymer
from .substance import Substance


class PolymerSubstance(Substance):
    """Polymer Substance model."""

    model_config = ConfigDict(extra='forbid')

    polymer: Polymer = Field(
        default=...,
        alias='polymer',
        title='Polymer',
        description='Polymer definition for this substance.',
    )
