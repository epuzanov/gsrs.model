from pydantic import Field, ConfigDict
from typing import List

from .ginas_common_sub_data import GinasCommonSubData
from .specified_substance_component import SpecifiedSubstanceComponent

class SpecifiedSubstanceG1(GinasCommonSubData):
    """specifiedSubstance model."""

    model_config = ConfigDict(extra='forbid')

    constituents: List[SpecifiedSubstanceComponent] = Field(
        ...,
        alias='constituents',
        title='constituents',
        description='constituents',
        element_property=True,
    )
