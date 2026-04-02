from pydantic import Field, ConfigDict
from typing import List, Union
from uuid import UUID

from .structure import Structure

class GinasChemicalStructure(Structure):
    """Chemical Structure model."""

    model_config = ConfigDict(extra='forbid')

    access: Union[List[str], None] = Field(
        default=None,
        alias='access',
        title='Access',
        description='Access',
    )

    lastEditedBy: Union[str, None] = Field(
        default=None,
        alias='lastEditedBy',
        title='Last Modified By',
        description='Last Modified By',
    )

    createdBy: Union[str, None] = Field(
        default=None,
        alias='createdBy',
        title='Created By',
        description='Created By',
    )

    def is_public(self) -> bool:
        """Determine if the record is public based on access permissions."""
        return not self.access
