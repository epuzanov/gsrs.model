from pydantic import Field, ConfigDict
from typing import Union
from enum import Enum

from .ginas_common_sub_data import GinasCommonSubData
from .substance_reference import SubstanceReference

class Type(Enum):
    """Type model."""
 
    MUST_BE_PRESENT = 'MUST_BE_PRESENT'
    MAY_BE_PRESENT_ONE_OF = 'MAY_BE_PRESENT_ONE_OF'
    MAY_BE_PRESENT_ANY_OF = 'MAY_BE_PRESENT_ANY_OF'

class Component(GinasCommonSubData):
    """Component model."""

    model_config = ConfigDict(extra='forbid')

    type: Union[Type, None] = Field(
        None,
        alias='type',
        title='Type',
        description='Type',
        element_property=True,
    )

    substance: Union[SubstanceReference, None] = Field(
        None,
        alias='substance',
        title='Substance',
        description='Substance',
        element_property=True,
    )
