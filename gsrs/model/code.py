from pydantic import Field, ConfigDict
from typing import Union

from .ginas_common_sub_data import GinasCommonSubData

class Code(GinasCommonSubData):
    """Code model."""

    model_config = ConfigDict(extra='forbid')

    codeText: Union[str, None] = Field(
        default=None,
        alias='codeText',
        title='Code Text',
        description='Code Text',
    )
    codeSystem: Union[str, None] = Field(
        default=None,
        alias='codeSystem',
        title='Code system',
        description='Code system',
    )
    code: str = Field(
        default=...,
        alias='code',
        title='Code',
        description='Code',
    )
    comments: Union[str, None] = Field(
        default=None,
        alias='comments',
        title='Code Comments',
        description='Code Comments',
    )
    type: Union[str, None] = Field(
        default=None,
        alias='type',
        title='Code Type',
        description='Code Type',
    )
    url: Union[str, None] = Field(
        default=None,
        alias='url',
        title='Code URL',
        description='Code URL',
    )
    isClassification: Union[bool, None] = Field(
        default=None,
        alias='_isClassification',
        title='Classification Flag',
        description='System flag indicating whether the code is treated as a classification.',
    )
