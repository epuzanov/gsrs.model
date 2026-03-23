from pydantic import BaseModel, Field, ConfigDict
from typing import Union


class Value(BaseModel):
    """Value model."""

    model_config = ConfigDict(extra='forbid')

    id: int = Field(
        default=...,
        alias='id',
        title='ID',
        description='ID',
    )

    label: str = Field(
        default=...,
        alias='label',
        title='Label',
        description='Label',
    )

    text: Union[str, None] = Field(
        default=None,
        alias='text',
        title='Text',
        description='Text',
    )

    term: Union[str, None] = Field(
        default=None,
        alias='term',
        title='Term',
        description='Term',
    )

