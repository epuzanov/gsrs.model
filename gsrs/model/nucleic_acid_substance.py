from pydantic import Field, ConfigDict
from typing import Union

from .nucleic_acid import NucleicAcid
from .substance import Substance


class NucleicAcidSubstance(Substance):
    """Nucleic Acid Substance model."""

    model_config = ConfigDict(extra='forbid')

    nucleicAcid: Union[NucleicAcid, None] = Field(
        default=None,
        alias='nucleicAcid',
        title='Nucleic Acid',
        description='Nucleic Acid definition for this substance.',
    )
