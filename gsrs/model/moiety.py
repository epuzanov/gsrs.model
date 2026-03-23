from pydantic import Field, ConfigDict
from typing import Union
from uuid import UUID

from .amount import Amount
from .ginas_chemical_structure import GinasChemicalStructure

class Moiety(GinasChemicalStructure):
    """Moiety model."""

    model_config = ConfigDict(extra='forbid')

    uuid: Union[UUID, None] = Field(
        default=None,
        alias='uuid',
        title='Uuid',
        description='Uuid',
    )

    countAmount: Union[Amount, None] = Field(
        default=None,
        alias='countAmount',
        title='Count',
        description='Count',
    )
