from pydantic import Field, ConfigDict
from typing import Union
from datetime import date

from .ginas_common_sub_data import GinasCommonSubData

class NameOrg(GinasCommonSubData):
    """Naming Org model."""

    model_config = ConfigDict(extra='forbid')

    nameOrg: str = Field(
        ...,
        alias='nameOrg',
        title='Naming Organization',
        description='Naming Organization',
        element_property=True,
    )

    deprecatedDate: Union[date, None] = Field(
        None,
        alias='deprecatedDate',
        title='Deprecated Date',
        description='Deprecated Date',
        element_property=True,
    )
