from pydantic import Field, ConfigDict
from typing import List, Union

from .ginas_common_sub_data import GinasCommonSubData
from .linkage import Linkage
from .modifications import Modifications
from .subunit import Subunit
from .sugar import Sugar

class NucleicAcid(GinasCommonSubData):
    """Nucleic acid model described through base, sugar, and linkage components."""

    model_config = ConfigDict(extra='forbid')

    linkages: Union[List[Linkage], None] = Field(
        default=None,
        alias='linkages',
        title='Linkages',
        description='Linkages connecting sugar residues within the nucleic acid sequence.',
    )

    modifications: Union[Modifications, None] = Field(
        default=None,
        alias='modifications',
        title='Modifications',
        description='Modifications',
    )

    nucleicAcidType: Union[str, None] = Field(
        default=None,
        alias='nucleicAcidType',
        title='Nucleic Acid Type',
        description='Controlled classification of the nucleic acid sequence type.',
    )

    nucleicAcidSubType: Union[List[str], None] = Field(
        default=None,
        alias='nucleicAcidSubType',
        title='Nucleic Acid Subtypes',
        description='Subtype labels for the nucleic acid when more specific classification is needed.',
    )

    sequenceOrigin: Union[str, None] = Field(
        default=None,
        alias='sequenceOrigin',
        title='Sequence Origin',
        description='Origin of the nucleic acid sequence, such as natural or synthetic.',
    )

    sequenceType: Union[str, None] = Field(
        default=None,
        alias='sequenceType',
        title='Sequence Type',
        description='Type of sequence being described for the nucleic acid.',
    )

    subunits: Union[List[Subunit], None] = Field(
        default=None,
        alias='subunits',
        title='Subunits',
        description='Ordered nucleic acid strands or closely associated sequences that make up the substance.',
    )

    sugars: List[Sugar] = Field(
        default=...,
        alias='sugars',
        title='Sugars',
        description='Sugar or sugar-like components that make up the nucleotide residues.',
    )

