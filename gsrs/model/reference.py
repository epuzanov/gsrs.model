from pydantic import Field, ConfigDict
from typing import List, Union

from .ginas_common_data import GinasCommonData

class Reference(GinasCommonData):
    """Reference model."""

    model_config = ConfigDict(extra='forbid')

    citation: Union[str, None] = Field(
        None,
        alias='citation',
        title='Citation Text',
        description='Citation Text',
        element_property=True,
    )

    docType: str = Field(
        ...,
        alias='docType',
        title='Reference Type',
        description='Reference Type',
        element_property=True,
    )

    documentDate: Union[float, None] = Field(
        None,
        alias='documentDate',
        title='Date Accessed',
        description='Date Accessed',
        element_property=True,
    )

    publicDomain: Union[bool, None] = Field(
        None,
        alias='publicDomain',
        title='Public Domain Reference',
        description='Public Domain Reference',
        element_property=True,
    )

    tags: Union[List[str], None] = Field(
        None,
        alias='tags',
        title='Tags',
        description='Tags',
        element_property=True,
    )

    uploadedFile: Union[str, None] = Field(
        None,
        alias='uploadedFile',
        title='Uploaded Document',
        description='Uploaded Document',
        element_property=True,
    )

    id: Union[str, None] = Field(
        None,
        alias='id',
        title='Ref_ID',
        description='Ref_ID',
        element_property=True,
    )

    url: Union[str, None] = Field(
        None,
        alias='url',
        title='Reference URL',
        description='Reference URL',
        element_property=True,
    )
