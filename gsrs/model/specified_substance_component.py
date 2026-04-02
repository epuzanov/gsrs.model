from pydantic import Field, ConfigDict
from typing import Union

from .amount import Amount
from .component import Component

class SpecifiedSubstanceComponent(Component):
    """constituents model."""

    model_config = ConfigDict(extra='forbid')

    role: Union[str, None] = Field(
        default=None,
        alias='role',
        title='Role',
        description='Role',
    )

    amount: Union[Amount, None] = Field(
        default=None,
        alias='amount',
        title='Amount',
        description='Amount',
    )

