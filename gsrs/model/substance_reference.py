from pydantic import Field, ConfigDict
from typing import Union
from enum import Enum

from .ginas_common_sub_data import GinasCommonSubData


class SubstanceClass(Enum):
    """Enumeration of GSRS substance classes."""

    reference = 'reference'

class SubstanceReference(GinasCommonSubData):
    """Hybrid Species Paternal Organism model."""

    model_config = ConfigDict(extra='forbid')

    refPname: Union[str, None] = Field(
        default=None,
        alias='refPname',
        title='Referenced Substance Name',
        description='Referenced Substance Name',
    )

    name: Union[str, None] = Field(
        default=None,
        alias='name',
        title='Name',
        description='Name',
    )

    linkingID: Union[str, None] = Field(
        default=None,
        alias='linkingID',
        title='Linking ID',
        description='Linking ID',
    )

    refuuid: str = Field(
        default=None,
        alias='refuuid',
        title='Refuuid',
        description='Refuuid',
    )

    substanceClass: Union[SubstanceClass, None] = Field(
        default=None,
        alias='substanceClass',
        title='Substance Class',
        description='Substance Class',
    )

    approvalID: Union[str, None] = Field(
        default=None,
        alias='approvalID',
        title='Approval ID',
        description='Approval ID',
    )
