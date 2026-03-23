from pydantic import Field, ConfigDict
from typing import List, Union

from .ginas_common_sub_data import GinasCommonSubData
from .site import Site

class OtherLink(GinasCommonSubData):
    """Other Linkage model."""

    model_config = ConfigDict(extra='forbid')

    sites: Union[List[Site], None] = Field(
        default=None,
        alias='sites',
        title='Linkage sites',
        description='Linkage sites',
        min_length=2,
    )

    linkageType: str = Field(
        default=...,
        alias='linkageType',
        title='Linkage type',
        description='Linkage type',
    )
