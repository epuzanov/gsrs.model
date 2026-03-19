from pydantic import Field, ConfigDict
from typing import List, Union
from uuid import UUID

from .ginas_common_data import GinasCommonData

class GinasCommonSubData(GinasCommonData):
    """Base model for common GSRS sub-data fields."""

    model_config = ConfigDict(extra='forbid')

    references: Union[List[UUID], None] = Field(
        None,
        alias='references',
        title='References',
        description='References',
        element_property=True,
    )


    sitesShorthand: Union[str, None] = Field(
        None,
        alias='sitesShorthand',
        title='Sites Shorthand',
        description='Compact system-generated shorthand for the referenced sites.',
        element_property=True,
    )
