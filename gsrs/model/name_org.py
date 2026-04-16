from pydantic import Field, ConfigDict
from typing import Union
from datetime import datetime

from .ginas_common_sub_data import GinasCommonSubData

class NameOrg(GinasCommonSubData):
    """Naming Org model."""

    model_config = ConfigDict(extra='forbid')

    nameOrg: Union[str, None] = Field(
        default=None,
        alias='nameOrg',
        title='Naming Organization',
        description='Naming Organization',
    )

    deprecatedDate: Union[datetime, None] = Field(
        default=None,
        alias='deprecatedDate',
        title='Deprecated Date',
        description='Deprecated Date',
    )

