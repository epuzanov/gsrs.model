from pydantic import Field, ConfigDict
from typing import Union

from .amount import Amount
from .ginas_common_sub_data import GinasCommonSubData
from .substance_reference import SubstanceReference

class Relationship(GinasCommonSubData):
    """Relationship model."""

    model_config = ConfigDict(extra='forbid')

    amount: Union[Amount, None] = Field(
        default=None,
        alias='amount',
        title='Amount',
        description='Amount',
    )
    comments: Union[str, None] = Field(
        default=None,
        alias='comments',
        title='Comments',
        description='Comments',
    )
    interactionType: Union[str, None] = Field(
        default=None,
        alias='interactionType',
        title='Interaction Type',
        description='Interaction Type',
    )
    originatorUuid: Union[str, None] = Field(
        default=None,
        alias='originatorUuid',
        title='Originator UUID',
        description='Originator UUID',
    )
    qualification: Union[str, None] = Field(
        default=None,
        alias='qualification',
        title='Qualification',
        description='Qualification',
    )
    relatedSubstance: SubstanceReference = Field(
        default=...,
        alias='relatedSubstance',
        title='Related Substance',
        description='Related Substance',
    )
    type: Union[str, None] = Field(
        default=...,
        alias='type',
        title='Relationship Type',
        description='Relationship Type',
    )
    mediatorSubstance: Union[SubstanceReference, None] = Field(
        default=None,
        alias='mediatorSubstance',
        title='Mediator Substance',
        description='Mediator Substance',
    )
