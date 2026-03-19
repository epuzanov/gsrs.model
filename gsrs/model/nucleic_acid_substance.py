from pydantic import Field, ConfigDict
from typing import Union

from .nucleic_acid import NucleicAcid
from .substance import Substance

class NucleicAcidSubstance(Substance):
    """Nucleic Acid Substance model."""

    model_config = ConfigDict(extra='forbid')

    nucleicAcid: Union[NucleicAcid, None] = Field(
        None,
        alias='nucleicAcid',
        title='Nucleic Acid',
        description='Nucleic Acid',
        element_property=True,
    )
