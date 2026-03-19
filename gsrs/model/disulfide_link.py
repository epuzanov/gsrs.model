from pydantic import Field, ConfigDict
from typing import List, Union

from .ginas_common_sub_data import GinasCommonSubData
from .site import Site

class DisulfideLink(GinasCommonSubData):
    """Disulfide Link model."""

    model_config = ConfigDict(extra='forbid')

    sites: Union[List[Site], None] = Field(
        None,
        alias='sites',
        title='Disulfide Sites',
        description='Disulfide Sites',
        element_property=True,
        max_items=2,
        min_length=2,
    )
