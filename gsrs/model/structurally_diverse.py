from pydantic import Field, ConfigDict
from typing import List, Union

from .ginas_common_sub_data import GinasCommonSubData
from .substance_reference import SubstanceReference

class StructurallyDiverse(GinasCommonSubData):
    """Structurally diverse model for source-material and organism provenance details."""

    model_config = ConfigDict(extra='forbid')

    sourceMaterialClass: Union[str, None] = Field(
        None,
        alias='sourceMaterialClass',
        title='Source Material Class',
        description='Class of source material from which the structurally diverse substance is derived.',
        element_property=True,
    )

    sourceMaterialState: Union[str, None] = Field(
        None,
        alias='sourceMaterialState',
        title='Source Material State',
        description='Physical or processing state of the source material.',
        element_property=True,
    )

    sourceMaterialType: Union[str, None] = Field(
        None,
        alias='sourceMaterialType',
        title='Source Material Type',
        description='Origin or source-material type for the raw material.',
        element_property=True,
    )

    developmentalStage: Union[str, None] = Field(
        None,
        alias='developmentalStage',
        title='Developmental Stage',
        description='Developmental stage of the source organism or material when relevant.',
        element_property=True,
    )

    fractionName: Union[str, None] = Field(
        None,
        alias='fractionName',
        title='Fraction Name',
        description='Named fraction of the source material used to obtain the substance.',
        element_property=True,
    )

    fractionMaterialType: Union[str, None] = Field(
        None,
        alias='fractionMaterialType',
        title='Fraction Material Type',
        description='Type of source-material fraction used in the substance description.',
        element_property=True,
    )

    organismFamily: Union[str, None] = Field(
        None,
        alias='organismFamily',
        title='Organism Family',
        description='Taxonomic family of the source organism.',
        element_property=True,
    )

    organismGenus: Union[str, None] = Field(
        None,
        alias='organismGenus',
        title='Organism Genus',
        description='Taxonomic genus of the source organism.',
        element_property=True,
    )

    organismSpecies: Union[str, None] = Field(
        None,
        alias='organismSpecies',
        title='Organism Species',
        description='Taxonomic species of the source organism.',
        element_property=True,
    )

    organismAuthor: Union[str, None] = Field(
        None,
        alias='organismAuthor',
        title='Organism Author',
        description='Authorship or naming authority associated with the organism designation.',
        element_property=True,
    )

    partLocation: Union[str, None] = Field(
        None,
        alias='partLocation',
        title='Part Location',
        description='Detailed anatomical location from which the source material part is taken.',
        element_property=True,
    )

    part: Union[List[str], None] = Field(
        None,
        alias='part',
        title='Parts',
        description='Anatomical parts of the organism used as source material.',
        element_property=True,
    )

    infraSpecificType: Union[str, None] = Field(
        None,
        alias='infraSpecificType',
        title='Infra Specific Type',
        description='Infraspecific rank or type used to further qualify the organism.',
        element_property=True,
    )

    infraSpecificName: Union[str, None] = Field(
        None,
        alias='infraSpecificName',
        title='Infra Specific Name',
        description='Infraspecific description used to further identify the organism.',
        element_property=True,
    )

    hybridSpeciesPaternalOrganism: Union[SubstanceReference, None] = Field(
        None,
        alias='hybridSpeciesPaternalOrganism',
        title='Hybrid Species Paternal Organism',
        description='Referenced paternal organism for a hybrid source organism.',
        element_property=True,
    )

    hybridSpeciesMaternalOrganism: Union[SubstanceReference, None] = Field(
        None,
        alias='hybridSpeciesMaternalOrganism',
        title='Hybrid Species Maternal Organism',
        description='Referenced maternal organism for a hybrid source organism.',
        element_property=True,
    )


    parentSubstance: Union[SubstanceReference, None] = Field(
        None,
        alias='parentSubstance',
        title='Parent Substance',
        description='Referenced parent substance associated with the structurally diverse material.',
        element_property=True,
    )
