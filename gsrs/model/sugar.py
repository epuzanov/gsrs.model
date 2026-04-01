from pydantic import Field, ConfigDict
from typing import List, Union

from .ginas_common_sub_data import GinasCommonSubData
from .site import Site

class Sugar(GinasCommonSubData):
    """Sugar model for nucleotide sugar or sugar-like components."""

    model_config = ConfigDict(extra='forbid')

    sites: Union[List[Site], None] = Field(
        default=None,
        alias='sites',
        title='Sites',
        description='Residue sites in the sequence that contain the specified sugar component.',
    )

    sugar: str = Field(
        default=...,
        alias='sugar',
        title='Sugar',
        description='Name or identifier of the sugar or sugar-like component in the nucleotide.',
    )

    sitesShorthand: Union[str, None] = Field(
        default=None,
        alias='sitesShorthand',
        title='Sites Shorthand',
        description='Compact system-generated shorthand for the referenced sites.',
    )
