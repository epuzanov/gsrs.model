from pydantic import BaseModel, Field, ConfigDict
from typing import Union


class Value(BaseModel):
    """Value model."""

    model_config = ConfigDict(extra='forbid')

    id: int = Field(
        ...,
        alias='id',
        title='ID',
        description='ID',
        element_property=True,
    )

    label: str = Field(
        ...,
        alias='label',
        title='Label',
        description='Label',
        element_property=True,
    )

    text: Union[str, None] = Field(
        None,
        alias='text',
        title='Text',
        description='Text',
        element_property=True,
    )

    term: Union[str, None] = Field(
        None,
        alias='term',
        title='Term',
        description='Term',
        element_property=True,
    )

