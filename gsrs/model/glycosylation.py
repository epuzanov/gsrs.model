from pydantic import Field, ConfigDict
from typing import List, Union

from .ginas_common_sub_data import GinasCommonSubData
from .site import Site

class Glycosylation(GinasCommonSubData):
    """Glycosylation model."""

    model_config = ConfigDict(extra='forbid')

    CGlycosylationSites: Union[List[Site], None] = Field(
        None,
        alias='CGlycosylationSites',
        title='C-Glycosylation',
        description='C-Glycosylation',
        element_property=True,
    )

    NGlycosylationSites: Union[List[Site], None] = Field(
        None,
        alias='NGlycosylationSites',
        title='N-Glycosylation',
        description='N-Glycosylation',
        element_property=True,
    )

    OGlycosylationSites: Union[List[Site], None] = Field(
        None,
        alias='OGlycosylationSites',
        title='O-Glycosylation',
        description='O-Glycosylation',
        element_property=True,
    )

    glycosylationType: Union[str, None] = Field(
        None,
        alias='glycosylationType',
        title='Glycosylation Type',
        description='Glycosylation Type',
        element_property=True,
    )
