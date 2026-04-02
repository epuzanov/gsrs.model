from pydantic import Field, ConfigDict
from typing import List, Union

from .ginas_common_sub_data import GinasCommonSubData
from .physical_parameter import PhysicalParameter

class PhysicalModification(GinasCommonSubData):
    """Physical Modification model."""

    model_config = ConfigDict(extra='forbid')

    physicalModificationRole: str = Field(
        default=...,
        alias='physicalModificationRole',
        title='Role of Modification',
        description='Role of Modification',
    )

    parameters: List[PhysicalParameter] = Field(
        default=...,
        alias='parameters',
        title='Physical Parameters',
        description='Physical Parameters',
        min_length=1,
    )

    modificationGroup: Union[str, None] = Field(
        default=None,
        alias='modificationGroup',
        title='Modification Group',
        description='Modification Group',
    )

