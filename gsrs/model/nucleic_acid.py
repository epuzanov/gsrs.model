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
        None,
        alias='linkages',
        title='Linkages',
        description='Linkages connecting sugar residues within the nucleic acid sequence.',
        element_property=True,
    )

    modifications: Union[Modifications, None] = Field(
        None,
        alias='modifications',
        title='Modifications',
        description='Modifications',
        element_property=True,
    )

    nucleicAcidType: Union[str, None] = Field(
        None,
        alias='nucleicAcidType',
        title='Nucleic Acid Type',
        description='Controlled classification of the nucleic acid sequence type.',
        element_property=True,
    )

    nucleicAcidSubType: Union[List[str], None] = Field(
        None,
        alias='nucleicAcidSubType',
        title='Nucleic Acid Subtypes',
        description='Subtype labels for the nucleic acid when more specific classification is needed.',
        element_property=True,
    )

    sequenceOrigin: Union[str, None] = Field(
        None,
        alias='sequenceOrigin',
        title='Sequence Origin',
        description='Origin of the nucleic acid sequence, such as natural or synthetic.',
        element_property=True,
    )

    sequenceType: Union[str, None] = Field(
        None,
        alias='sequenceType',
        title='Sequence Type',
        description='Type of sequence being described for the nucleic acid.',
        element_property=True,
    )

    subunits: Union[List[Subunit], None] = Field(
        None,
        alias='subunits',
        title='Subunits',
        description='Ordered nucleic acid strands or closely associated sequences that make up the substance.',
        element_property=True,
    )

    sugars: List[Sugar] = Field(
        ...,
        alias='sugars',
        title='Sugars',
        description='Sugar or sugar-like components that make up the nucleotide residues.',
        element_property=True,
    )
