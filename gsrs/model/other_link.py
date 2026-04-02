from pydantic import Field, ConfigDict

from .site_container import SiteContainer


class OtherLink(SiteContainer):
    """Other Linkage model."""

    model_config = ConfigDict(extra='forbid')

    linkageType: str = Field(
        default=...,
        alias='linkageType',
        title='Linkage type',
        description='Linkage type',
    )

