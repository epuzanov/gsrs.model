from pydantic import Field, ConfigDict
from typing import List, Union

from .ginas_common_sub_data import GinasCommonSubData
from .physical_parameter import PhysicalParameter

class PhysicalModification(GinasCommonSubData):
    """Physical Modification model."""

    model_config = ConfigDict(extra='forbid')

    physicalModificationRole: str = Field(
        ...,
        alias='physicalModificationRole',
        title='Role of Modification',
        description='Role of Modification',
        element_property=True,
    )

    parameters: List[PhysicalParameter] = Field(
        ...,
        alias='parameters',
        title='Physical Parameters',
        description='Physical Parameters',
        element_property=True,
        min_length=1,
    )

    modificationGroup: Union[str, None] = Field(
        None,
        alias='modificationGroup',
        title='Modification Group',
        description='Modification Group',
        element_property=True,
    )
