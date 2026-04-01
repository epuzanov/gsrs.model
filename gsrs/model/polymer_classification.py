from pydantic import Field, ConfigDict
from typing import List, Union

from .ginas_common_sub_data import GinasCommonSubData
from .substance_reference import SubstanceReference

class PolymerClassification(GinasCommonSubData):
    """Polymer Classification model."""

    model_config = ConfigDict(extra='forbid')

    polymerClass: Union[str, None] = Field(
        default=None,
        alias='polymerClass',
        title='Polymer Class',
        description='Polymer Class',
    )

    polymerGeometry: Union[str, None] = Field(
        default=None,
        alias='polymerGeometry',
        title='Polymer Geometry',
        description='Polymer Geometry',
    )

    polymerSubclass: Union[List[str], None] = Field(
        default=None,
        alias='polymerSubclass',
        title='Polymer Subclass',
        description='Polymer Subclass',
    )

    sourceType: Union[str, None] = Field(
        default=None,
        alias='sourceType',
        title='Source Type',
        description='Source Type',
    )


    parentSubstance: Union[SubstanceReference, None] = Field(
        default=None,
        alias='parentSubstance',
        title='Parent Substance',
        description='Referenced parent substance used in classifying the polymer.',
    )
