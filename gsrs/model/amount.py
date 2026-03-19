from pydantic import Field, ConfigDict
from typing import Union

from .ginas_common_sub_data import GinasCommonSubData

class Amount(GinasCommonSubData):
    """Amount model."""

    model_config = ConfigDict(extra='forbid')

    type: Union[str, None] = Field(
        None,
        alias='type',
        title='Amount Type',
        description='Amount Type',
        element_property=True,
    )

    average: Union[float, None] = Field(
        None,
        alias='average',
        title='Average',
        description='Average',
        element_property=True,
    )

    highLimit: Union[float, None] = Field(
        None,
        alias='highLimit',
        title='High Limit',
        description='High Limit',
        element_property=True,
    )

    high: Union[float, None] = Field(
        None,
        alias='high',
        title='High',
        description='High',
        element_property=True,
    )

    lowLimit: Union[float, None] = Field(
        None,
        alias='lowLimit',
        title='Low Limit',
        description='Low Limit',
        element_property=True,
    )

    low: Union[float, None] = Field(
        None,
        alias='low',
        title='Low',
        description='Low',
        element_property=True,
    )

    units: Union[str, None] = Field(
        None,
        alias='units',
        title='Units',
        description='Units',
        element_property=True,
    )

    nonNumericValue: Union[str, None] = Field(
        None,
        alias='nonNumericValue',
        title='Non-numeric Value',
        description='Non-numeric Value',
        element_property=True,
    )
