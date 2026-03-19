from pydantic import Field, ConfigDict

from .structurally_diverse import StructurallyDiverse
from .substance import Substance

class StructurallyDiverseSubstance(Substance):
    """Structurally Diverse Substance model."""

    model_config = ConfigDict(extra='forbid')

    structurallyDiverse: StructurallyDiverse = Field(
        ...,
        alias='structurallyDiverse',
        title='Structurally Diverse',
        description='Structurally Diverse',
        element_property=True,
    )
