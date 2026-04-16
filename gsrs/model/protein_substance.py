from pydantic import Field, ConfigDict

from .protein import Protein
from .substance import Substance


class ProteinSubstance(Substance):
    """Protein Substance model."""

    model_config = ConfigDict(extra='forbid')

    protein: Protein = Field(
        default=...,
        alias='protein',
        title='Protein',
        description='Protein definition for this substance.',
    )
