from pydantic import Field, ConfigDict
from typing import Union

from .site_container import SiteContainer


class OtherLink(SiteContainer):
    """Other Linkage model."""

    model_config = ConfigDict(extra='forbid')

    linkageType: Union[str, None] = Field(
        default=None,
        alias='linkageType',
        title='Linkage type',
        description='Linkage type',
    )

