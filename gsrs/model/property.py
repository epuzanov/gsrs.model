from pydantic import Field, ConfigDict
from typing import List, Union

from .amount import Amount
from .ginas_common_sub_data import GinasCommonSubData
from .parameter import Parameter
from .substance_reference import SubstanceReference

class Property(GinasCommonSubData):
    """Property model."""

    model_config = ConfigDict(extra='forbid')

    name: str = Field(
        ...,
        alias='name',
        title='Property Name',
        description='Property Name',
        element_property=True,
    )

    type: Union[str, None] = Field(
        None,
        alias='type',
        title='Value Type',
        description='Value Type',
        element_property=True,
    )

    propertyType: Union[str, None] = Field(
        None,
        alias='propertyType',
        title='Property Type',
        description='Property Type',
        element_property=True,
    )

    value: Union[Amount, None] = Field(
        None,
        alias='value',
        title='Amount',
        description='Amount',
        element_property=True,
    )

    referencedSubstance: Union[SubstanceReference, None] = Field(
        None,
        alias='referencedSubstance',
        title='Referenced Substance',
        description='Referenced Substance',
        element_property=True,
    )

    defining: Union[bool, None] = Field(
        None,
        alias='defining',
        title='Defining',
        description='Defining',
        element_property=True,
    )

    parameters: Union[List[Parameter], None] = Field(
        None,
        alias='parameters',
        title='Parameters',
        description='Parameters',
        element_property=True,
    )
