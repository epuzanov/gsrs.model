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
        None,
        alias='refPname',
        title='Referenced Substance Name',
        description='Referenced Substance Name',
        element_property=True,
    )

    name: Union[str, None] = Field(
        None,
        alias='name',
        title='Name',
        description='Name',
        element_property=True,
    )

    linkingID: Union[str, None] = Field(
        None,
        alias='linkingID',
        title='Linking ID',
        description='Linking ID',
        element_property=True,
    )

    refuuid: str = Field(
        None,
        alias='refuuid',
        title='Refuuid',
        description='Refuuid',
        element_property=True,
    )

    substanceClass: Union[SubstanceClass, None] = Field(
        None,
        alias='substanceClass',
        title='Substance Class',
        description='Substance Class',
        element_property=True,
    )

    approvalID: Union[str, None] = Field(
        None,
        alias='approvalID',
        title='Approval ID',
        description='Approval ID',
        element_property=True,
    )
