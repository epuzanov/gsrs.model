from pydantic import Field, ConfigDict
from typing import Union

from .amount import Amount
from .ginas_common_sub_data import GinasCommonSubData

class Parameter(GinasCommonSubData):
    """Parameter model."""

    model_config = ConfigDict(extra='forbid')

    name: str = Field(
        default=...,
        alias='name',
        title='Parameter Name',
        description='Parameter Name',
    )

    type: Union[str, None] = Field(
        default=None,
        alias='type',
        title='Parameter Type',
        description='Parameter Type',
    )

    value: Union[Amount, None] = Field(
        default=None,
        alias='value',
        title='Amount',
        description='Amount',
    )
