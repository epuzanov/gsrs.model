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
        default=...,
        alias='name',
        title='Property Name',
        description='Property Name',
    )

    type: Union[str, None] = Field(
        default=None,
        alias='type',
        title='Value Type',
        description='Value Type',
    )

    propertyType: Union[str, None] = Field(
        default=None,
        alias='propertyType',
        title='Property Type',
        description='Property Type',
    )

    value: Union[Amount, None] = Field(
        default=None,
        alias='value',
        title='Amount',
        description='Amount',
    )

    referencedSubstance: Union[SubstanceReference, None] = Field(
        default=None,
        alias='referencedSubstance',
        title='Referenced Substance',
        description='Referenced Substance',
    )

    defining: Union[bool, None] = Field(
        default=None,
        alias='defining',
        title='Defining',
        description='Defining',
    )

    parameters: Union[List[Parameter], None] = Field(
        default=None,
        alias='parameters',
        title='Parameters',
        description='Parameters',
    )
