from pydantic import Field, ConfigDict
from typing import Union

from .ginas_common_sub_data import GinasCommonSubData

class Amount(GinasCommonSubData):
    """Amount model."""

    model_config = ConfigDict(extra='forbid')

    type: Union[str, None] = Field(
        default=None,
        alias='type',
        title='Amount Type',
        description='Amount Type',
    )

    average: Union[float, None] = Field(
        default=None,
        alias='average',
        title='Average',
        description='Average',
    )

    highLimit: Union[float, None] = Field(
        default=None,
        alias='highLimit',
        title='High Limit',
        description='High Limit',
    )

    high: Union[float, None] = Field(
        default=None,
        alias='high',
        title='High',
        description='High',
    )

    lowLimit: Union[float, None] = Field(
        default=None,
        alias='lowLimit',
        title='Low Limit',
        description='Low Limit',
    )

    low: Union[float, None] = Field(
        default=None,
        alias='low',
        title='Low',
        description='Low',
    )

    units: Union[str, None] = Field(
        default=None,
        alias='units',
        title='Units',
        description='Units',
    )

    nonNumericValue: Union[str, None] = Field(
        default=None,
        alias='nonNumericValue',
        title='Non-numeric Value',
        description='Non-numeric Value',
    )

    def as_string(self) -> str:
        """Render the amount value as a human-readable string."""
        pieces: list[str] = []
        if self.nonNumericValue:
            pieces.append(str(self.nonNumericValue))
        elif self.average is not None:
            pieces.append(str(self.average))
        elif self.low is not None and self.high is not None:
            pieces.append(f'{self.low} to {self.high}')
        elif self.lowLimit is not None and self.highLimit is not None:
            pieces.append(f'{self.lowLimit} to {self.highLimit}')
        elif self.low is not None:
            pieces.append(str(self.low))
        elif self.high is not None:
            pieces.append(str(self.high))
        if self.units:
            pieces.append(str(self.units))
        if self.type:
            pieces.append(f'(amount type {self.type})')
        return ' '.join(pieces).strip()
