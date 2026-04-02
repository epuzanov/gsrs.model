from pydantic import Field
from typing import List, Union

from .component import Component
from .ginas_common_sub_data import GinasCommonSubData
from .substance_reference import SubstanceReference

class Mixture(GinasCommonSubData):
    """Mixture model."""

    components: List[Component] = Field(
        default=...,
        alias='components',
        title='Components',
        description='Components',
    )

    parentSubstance: Union[SubstanceReference, None] = Field(
        default=None,
        alias='parentSubstance',
        title='Parent Substance',
        description='Parent Substance',
    )

