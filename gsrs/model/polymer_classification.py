from pydantic import Field, ConfigDict
from typing import List, Union

from .ginas_common_sub_data import GinasCommonSubData
from .substance_reference import SubstanceReference

class PolymerClassification(GinasCommonSubData):
    """Polymer Classification model."""

    model_config = ConfigDict(extra='forbid')

    polymerClass: Union[str, None] = Field(
        None,
        alias='polymerClass',
        title='Polymer Class',
        description='Polymer Class',
        element_property=True,
    )

    polymerGeometry: Union[str, None] = Field(
        None,
        alias='polymerGeometry',
        title='Polymer Geometry',
        description='Polymer Geometry',
        element_property=True,
    )

    polymerSubclass: Union[List[str], None] = Field(
        None,
        alias='polymerSubclass',
        title='Polymer Subclass',
        description='Polymer Subclass',
        element_property=True,
    )

    sourceType: Union[str, None] = Field(
        None,
        alias='sourceType',
        title='Source Type',
        description='Source Type',
        element_property=True,
    )


    parentSubstance: Union[SubstanceReference, None] = Field(
        None,
        alias='parentSubstance',
        title='Parent Substance',
        description='Referenced parent substance used in classifying the polymer.',
        element_property=True,
    )
