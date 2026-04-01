from pydantic import Field, ConfigDict
from typing import Union

from .protein import Protein
from .substance import Substance


class ProteinSubstance(Substance):
    """Protein Substance model."""

    model_config = ConfigDict(extra='forbid')

    protein: Union[Protein, None] = Field(
        default=None,
        alias='protein',
        title='Protein',
        description='Protein definition for this substance.',
    )
