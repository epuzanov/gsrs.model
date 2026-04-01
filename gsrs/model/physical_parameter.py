from pydantic import Field, ConfigDict
from typing import Union

from .amount import Amount
from .ginas_common_sub_data import GinasCommonSubData

class PhysicalParameter(GinasCommonSubData):
    """Physical Parameter model."""

    model_config = ConfigDict(extra='forbid')

    parameterName: str = Field(
        default=...,
        alias='parameterName',
        title='Parameter Name',
        description='Parameter Name',
    )

    amount: Union[Amount, None] = Field(
        default=None,
        alias='amount',
        title='Amount',
        description='Amount',
    )
