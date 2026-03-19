from pydantic import Field, ConfigDict
from typing import List, Union

from .disulfide_link import DisulfideLink
from .ginas_common_sub_data import GinasCommonSubData
from .glycosylation import Glycosylation
from .modifications import Modifications
from .other_link import OtherLink
from .subunit import Subunit

class Protein(GinasCommonSubData):
    """Protein model for defined amino acid sequences and their subunits."""

    model_config = ConfigDict(extra='forbid')

    proteinType: Union[str, None] = Field(
        None,
        alias='proteinType',
        title='Protein Type',
        description='Classification of the protein substance.',
        element_property=True,
    )

    proteinSubType: Union[List[str], str, None] = Field(
        None,
        alias='proteinSubType',
        title='Protein Subtypes',
        description='Subtype classification for the protein, when multiple subtype labels apply.',
        element_property=True,
    )

    sequenceOrigin: Union[str, None] = Field(
        None,
        alias='sequenceOrigin',
        title='Sequence Origin',
        description='Origin of the protein sequence, such as natural, recombinant, or synthetic.',
        element_property=True,
    )

    sequenceType: Union[str, None] = Field(
        None,
        alias='sequenceType',
        title='Sequence Type',
        description='Sequence basis used to describe the protein when a complete or partial amino acid sequence is available.',
        element_property=True,
    )

    disulfideLinks: Union[List[DisulfideLink], None] = Field(
        None,
        alias='disulfideLinks',
        title='Disulfide Links',
        description='Disulfide bonds linking cysteine residues within or across protein subunits.',
        element_property=True,
    )

    glycosylation: Glycosylation = Field(
        ...,
        alias='glycosylation',
        title='Glycosylation',
        description='Glycosylation pattern associated with the protein substance.',
        element_property=True,
    )

    modifications: Union[Modifications, None] = Field(
        None,
        alias='modifications',
        title='Modifications',
        description='Modifications',
        element_property=True,
    )

    subunits: Union[List[Subunit], None] = Field(
        None,
        alias='subunits',
        title='Subunits',
        description='Protein subunits listed for multi-sequence proteins, ordered consistently for identification.',
        element_property=True,
    )

    otherLinks: Union[List[OtherLink], None] = Field(
        None,
        alias='otherLinks',
        title='Other Linkage',
        description='Additional non-disulfide linkages present in the protein.',
        element_property=True,
    )
