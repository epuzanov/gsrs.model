from pydantic import Field, ConfigDict
from typing import Union

from .ginas_common_sub_data import GinasCommonSubData

class Subunit(GinasCommonSubData):
    """Subunit model for an ordered linear sequence within a protein or nucleic acid."""

    model_config = ConfigDict(extra='forbid')

    sequence: str = Field(
        ...,
        alias='sequence',
        title='Sequence',
        description='Primary sequence recorded in the appropriate biological direction for the subunit.',
        element_property=True,
    )

    subunitIndex: Union[float, None] = Field(
        None,
        alias='subunitIndex',
        title='Subunit Index',
        description='Ordinal index of the subunit within the full macromolecule.',
        element_property=True,
    )


    length: Union[float, None] = Field(
        None,
        alias='length',
        title='Length',
        description='Recorded residue length of the subunit sequence.',
        element_property=True,
    )
