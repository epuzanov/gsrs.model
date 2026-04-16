from pydantic import Field, ConfigDict
from typing import List, Union

from .ginas_common_sub_data import GinasCommonSubData
from .site import Site

class SiteContainer(GinasCommonSubData):
    """Site Container model."""

    model_config = ConfigDict(extra='forbid')

    sites: List[Site] = Field(
        default_factory=list,
        alias='sites',
        title='Sites',
        description='Sites',
    )

    sitesShorthand: Union[str, None] = Field(
        default=None,
        alias='sitesShorthand',
        title='Sites Shorthand',
        description='Compact system-generated shorthand for the referenced sites.',
    )
