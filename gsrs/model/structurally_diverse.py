from pydantic import Field, ConfigDict
from typing import List, Union

from .ginas_common_sub_data import GinasCommonSubData
from .substance_reference import SubstanceReference

class StructurallyDiverse(GinasCommonSubData):
    """Structurally diverse model for source-material and organism provenance details."""

    model_config = ConfigDict(extra='forbid')

    sourceMaterialClass: Union[str, None] = Field(
        default=None,
        alias='sourceMaterialClass',
        title='Source Material Class',
        description='Class of source material from which the structurally diverse substance is derived.',
    )

    sourceMaterialState: Union[str, None] = Field(
        default=None,
        alias='sourceMaterialState',
        title='Source Material State',
        description='Physical or processing state of the source material.',
    )

    sourceMaterialType: Union[str, None] = Field(
        default=None,
        alias='sourceMaterialType',
        title='Source Material Type',
        description='Origin or source-material type for the raw material.',
    )

    developmentalStage: Union[str, None] = Field(
        default=None,
        alias='developmentalStage',
        title='Developmental Stage',
        description='Developmental stage of the source organism or material when relevant.',
    )

    fractionName: Union[str, None] = Field(
        default=None,
        alias='fractionName',
        title='Fraction Name',
        description='Named fraction of the source material used to obtain the substance.',
    )

    fractionMaterialType: Union[str, None] = Field(
        default=None,
        alias='fractionMaterialType',
        title='Fraction Material Type',
        description='Type of source-material fraction used in the substance description.',
    )

    organismFamily: Union[str, None] = Field(
        default=None,
        alias='organismFamily',
        title='Organism Family',
        description='Taxonomic family of the source organism.',
    )

    organismGenus: Union[str, None] = Field(
        default=None,
        alias='organismGenus',
        title='Organism Genus',
        description='Taxonomic genus of the source organism.',
    )

    organismSpecies: Union[str, None] = Field(
        default=None,
        alias='organismSpecies',
        title='Organism Species',
        description='Taxonomic species of the source organism.',
    )

    organismAuthor: Union[str, None] = Field(
        default=None,
        alias='organismAuthor',
        title='Organism Author',
        description='Authorship or naming authority associated with the organism designation.',
    )

    partLocation: Union[str, None] = Field(
        default=None,
        alias='partLocation',
        title='Part Location',
        description='Detailed anatomical location from which the source material part is taken.',
    )

    part: List[str] = Field(
        default_factory=list,
        alias='part',
        title='Parts',
        description='Anatomical parts of the organism used as source material.',
    )

    infraSpecificType: Union[str, None] = Field(
        default=None,
        alias='infraSpecificType',
        title='Infra Specific Type',
        description='Infraspecific rank or type used to further qualify the organism.',
    )

    infraSpecificName: Union[str, None] = Field(
        default=None,
        alias='infraSpecificName',
        title='Infra Specific Name',
        description='Infraspecific description used to further identify the organism.',
    )

    hybridSpeciesPaternalOrganism: Union[SubstanceReference, None] = Field(
        default=None,
        alias='hybridSpeciesPaternalOrganism',
        title='Hybrid Species Paternal Organism',
        description='Referenced paternal organism for a hybrid source organism.',
    )

    hybridSpeciesMaternalOrganism: Union[SubstanceReference, None] = Field(
        default=None,
        alias='hybridSpeciesMaternalOrganism',
        title='Hybrid Species Maternal Organism',
        description='Referenced maternal organism for a hybrid source organism.',
    )

    parentSubstance: Union[SubstanceReference, None] = Field(
        default=None,
        alias='parentSubstance',
        title='Parent Substance',
        description='Referenced parent substance associated with the structurally diverse material.',
    )

