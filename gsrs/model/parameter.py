from pydantic import Field, ConfigDict
from typing import Union

from .amount import Amount
from .ginas_common_sub_data import GinasCommonSubData

class Parameter(GinasCommonSubData):
    """Parameter model."""

    model_config = ConfigDict(extra='forbid')

    name: str = Field(
        ...,
        alias='name',
        title='Parameter Name',
        description='Parameter Name',
        element_property=True,
    )

    type: Union[str, None] = Field(
        None,
        alias='type',
        title='Parameter Type',
        description='Parameter Type',
        element_property=True,
    )

    value: Union[Amount, None] = Field(
        None,
        alias='value',
        title='Amount',
        description='Amount',
        element_property=True,
    )
