from pydantic import Field, ConfigDict
from typing import List, Union

from .ginas_common_sub_data import GinasCommonSubData
from .site import Site

class Glycosylation(GinasCommonSubData):
    """Glycosylation model."""

    model_config = ConfigDict(extra='forbid')

    CGlycosylationSites: List[Site] = Field(
        default_factory=list,
        alias='CGlycosylationSites',
        title='C-Glycosylation',
        description='C-Glycosylation',
    )

    NGlycosylationSites: List[Site] = Field(
        default_factory=list,
        alias='NGlycosylationSites',
        title='N-Glycosylation',
        description='N-Glycosylation',
    )

    OGlycosylationSites: List[Site] = Field(
        default_factory=list,
        alias='OGlycosylationSites',
        title='O-Glycosylation',
        description='O-Glycosylation',
    )

    glycosylationType: Union[str, None] = Field(
        default=None,
        alias='glycosylationType',
        title='Glycosylation Type',
        description='Glycosylation Type',
    )

    sitesShorthand: Union[str, None] = Field(
        default=None,
        alias='sitesShorthand',
        title='Sites Shorthand',
        description='Compact system-generated shorthand for the referenced sites.',
    )

