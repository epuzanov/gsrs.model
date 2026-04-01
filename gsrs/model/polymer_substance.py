from pydantic import Field, ConfigDict
from typing import Union

from .polymer import Polymer
from .substance import Substance


class PolymerSubstance(Substance):
    """Polymer Substance model."""

    model_config = ConfigDict(extra='forbid')

    polymer: Union[Polymer, None] = Field(
        default=None,
        alias='polymer',
        title='Polymer',
        description='Polymer definition for this substance.',
    )
