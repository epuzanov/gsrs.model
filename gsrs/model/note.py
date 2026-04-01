from pydantic import Field, ConfigDict
from typing import Union

from .ginas_common_sub_data import GinasCommonSubData

class Note(GinasCommonSubData):
    """Note model."""

    model_config = ConfigDict(extra='forbid')

    note: Union[str, None] = Field(
        default=...,
        alias='note',
        title='Note',
        description='Note',
    )
