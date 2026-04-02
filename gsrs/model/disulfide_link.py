from pydantic import BaseModel, ConfigDict, Field
from typing import List, Union

from .site import Site


class DisulfideLink(BaseModel):
    """Disulfide Link model."""

    model_config = ConfigDict(extra='forbid')

    sites: Union[List[Site], None] = Field(
        default=None,
        alias='sites',
        title='Disulfide Sites',
        description='Disulfide Sites',
        max_length=2,
        min_length=2,
    )

    sitesShorthand: Union[str, None] = Field(
        default=None,
        alias='sitesShorthand',
        title='Sites Shorthand',
        description='Compact system-generated shorthand for the referenced sites.',
    )

