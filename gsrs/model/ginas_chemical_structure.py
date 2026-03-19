from pydantic import Field, ConfigDict
from typing import List, Union
from uuid import UUID

from .structure import Structure

class GinasChemicalStructure(Structure):
    """Chemical Structure model."""

    model_config = ConfigDict(extra='forbid')

    access: Union[List[str], None] = Field(
        None,
        alias='access',
        title='Access',
        description='Access',
        element_property=True,
    )

    lastEditedBy: Union[str, None] = Field(
        None,
        alias='lastEditedBy',
        title='Last Modified By',
        description='Last Modified By',
        element_property=True,
    )

    createdBy: Union[str, None] = Field(
        None,
        alias='createdBy',
        title='Created By',
        description='Created By',
        element_property=True,
    )
