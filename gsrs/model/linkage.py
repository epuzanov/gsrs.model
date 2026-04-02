from pydantic import Field, ConfigDict
from typing import Union

from .site_container import SiteContainer


class Linkage(SiteContainer):
    """Linkage model for the connector between sugar residues in a nucleic acid."""

    model_config = ConfigDict(extra='forbid')

    linkage: Union[str, None] = Field(
        default=None,
        alias='linkage',
        title='Linkage',
        description='Linking entity between sugar residues, such as phosphate or another linkage group.',
    )

