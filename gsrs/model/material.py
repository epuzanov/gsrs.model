from pydantic import Field, ConfigDict
from typing import Union

from .amount import Amount
from .ginas_common_sub_data import GinasCommonSubData
from .substance_reference import SubstanceReference

class Material(GinasCommonSubData):
    """Material model for polymer starting materials or monomer inputs."""

    model_config = ConfigDict(extra='forbid')

    amount: Union[Amount, None] = Field(
        default=None,
        alias='amount',
        title='Amount',
        description='Relative amount of the starting material, often expressed as a percentage or ratio.',
    )

    monomerSubstance: Union[SubstanceReference, None] = Field(
        default=None,
        alias='monomerSubstance',
        title='Monomer Substance',
        description='Referenced substance used as a monomer or starting material.',
    )

    type: Union[str, None] = Field(
        default=None,
        alias='type',
        title='Material Role',
        description='Type or role of the starting material within the polymer description.',
    )

    defining: Union[bool, None] = Field(
        default=None,
        alias='defining',
        title='Defining',
        description='Whether this starting material is a defining element for uniquely identifying the polymer.',
    )

