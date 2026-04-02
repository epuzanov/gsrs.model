from pydantic import Field, ConfigDict

from .site_container import SiteContainer


class Sugar(SiteContainer):
    """Sugar model for nucleotide sugar or sugar-like components."""

    model_config = ConfigDict(extra='forbid')

    sugar: str = Field(
        default=...,
        alias='sugar',
        title='Sugar',
        description='Name or identifier of the sugar or sugar-like component in the nucleotide.',
    )

