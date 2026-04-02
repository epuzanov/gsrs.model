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
        default=None,
        alias='proteinType',
        title='Protein Type',
        description='Classification of the protein substance.',
    )

    proteinSubType: Union[List[str], str, None] = Field(
        default=None,
        alias='proteinSubType',
        title='Protein Subtypes',
        description='Subtype classification for the protein, when multiple subtype labels apply.',
    )

    sequenceOrigin: Union[str, None] = Field(
        default=None,
        alias='sequenceOrigin',
        title='Sequence Origin',
        description='Origin of the protein sequence, such as natural, recombinant, or synthetic.',
    )

    sequenceType: Union[str, None] = Field(
        default=None,
        alias='sequenceType',
        title='Sequence Type',
        description='Sequence basis used to describe the protein when a complete or partial amino acid sequence is available.',
    )

    disulfideLinks: Union[List[DisulfideLink], None] = Field(
        default=None,
        alias='disulfideLinks',
        title='Disulfide Links',
        description='Disulfide bonds linking cysteine residues within or across protein subunits.',
    )

    glycosylation: Glycosylation = Field(
        default=...,
        alias='glycosylation',
        title='Glycosylation',
        description='Glycosylation pattern associated with the protein substance.',
    )

    modifications: Union[Modifications, None] = Field(
        default=None,
        alias='modifications',
        title='Modifications',
        description='Modifications',
    )

    subunits: Union[List[Subunit], None] = Field(
        default=None,
        alias='subunits',
        title='Subunits',
        description='Protein subunits listed for multi-sequence proteins, ordered consistently for identification.',
    )

    otherLinks: Union[List[OtherLink], None] = Field(
        default=None,
        alias='otherLinks',
        title='Other Linkage',
        description='Additional non-disulfide linkages present in the protein.',
    )
