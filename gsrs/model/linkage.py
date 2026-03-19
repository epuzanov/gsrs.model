from pydantic import Field, ConfigDict
from typing import List, Union

from .ginas_common_sub_data import GinasCommonSubData
from .site import Site

class Linkage(GinasCommonSubData):
    """Linkage model for the connector between sugar residues in a nucleic acid."""

    model_config = ConfigDict(extra='forbid')

    linkage: Union[str, None] = Field(
        None,
        alias='linkage',
        title='Linkage',
        description='Linking entity between sugar residues, such as phosphate or another linkage group.',
        element_property=True,
    )

    sites: Union[List[Site], None] = Field(
        None,
        alias='sites',
        title='Sites',
        description='Residue sites associated with the linkage within the sequence.',
        element_property=True,
    )
