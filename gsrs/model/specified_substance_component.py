from pydantic import Field, ConfigDict
from typing import Union

from .amount import Amount
from .component import Component

class SpecifiedSubstanceComponent(Component):
    """constituents model."""

    model_config = ConfigDict(extra='forbid')

    role: Union[str, None] = Field(
        None,
        alias='role',
        title='Role',
        description='Role',
        element_property=True,
    )

    amount: Union[Amount, None] = Field(
        None,
        alias='amount',
        title='Amount',
        description='Amount',
        element_property=True,
    )
