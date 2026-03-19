from pydantic import AnyUrl, Field, ConfigDict
from typing import Union

from .ginas_common_sub_data import GinasCommonSubData

class Code(GinasCommonSubData):
    """Code model."""

    model_config = ConfigDict(extra='forbid')

    codeText: Union[str, None] = Field(
        None,
        alias='codeText',
        title='Code Text',
        description='Code Text',
        element_property=True,
    )

    codeSystem: Union[str, None] = Field(
        None,
        alias='codeSystem',
        title='Code system',
        description='Code system',
        element_property=True,
    )

    code: str = Field(
        ...,
        alias='code',
        title='Code',
        description='Code',
        element_property=True,
    )

    comments: Union[str, None] = Field(
        None,
        alias='comments',
        title='Code Comments',
        description='Code Comments',
        element_property=True,
    )

    type: Union[str, None] = Field(
        None,
        alias='type',
        title='Code Type',
        description='Code Type',
        element_property=True,
    )

    url: Union[str, None] = Field(
        None,
        alias='url',
        title='Code URL',
        description='Code URL',
        element_property=True,
    )


    isClassification: Union[bool, None] = Field(
        None,
        alias='_isClassification',
        title='Classification Flag',
        description='System flag indicating whether the code is treated as a classification.',
        element_property=True,
    )
