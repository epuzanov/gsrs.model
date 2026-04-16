from pydantic import Field, ConfigDict, field_validator
from typing import List, Union
from datetime import datetime, timezone

from .ginas_common_sub_data import GinasCommonSubData


class Reference(GinasCommonSubData):
    """Reference model."""

    model_config = ConfigDict(extra='forbid')

    citation: Union[str, None] = Field(
        default=None,
        alias='citation',
        title='Citation Text',
        description='Citation Text',
    )

    docType: Union[str, None] = Field(
        default=None,
        alias='docType',
        title='Reference Type',
        description='Reference Type',
    )

    documentDate: Union[datetime, None] = Field(
        default=None,
        alias='documentDate',
        title='Date Accessed',
        description='Date Accessed',
    )

    publicDomain: Union[bool, None] = Field(
        default=None,
        alias='publicDomain',
        title='Public Domain Reference',
        description='Public Domain Reference',
    )

    tags: Union[List[str], None] = Field(
        default=None,
        alias='tags',
        title='Tags',
        description='Tags',
    )

    uploadedFile: Union[str, None] = Field(
        default=None,
        alias='uploadedFile',
        title='Uploaded Document',
        description='Uploaded Document',
    )

    id: Union[str, None] = Field(
        default=None,
        alias='id',
        title='Ref_ID',
        description='Ref_ID',
    )

    url: Union[str, None] = Field(
        default=None,
        alias='url',
        title='Reference URL',
        description='Reference URL',
    )
