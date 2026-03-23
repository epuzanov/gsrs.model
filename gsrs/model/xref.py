from pydantic import BaseModel, Field, ConfigDict
from typing import List, Union
from uuid import UUID

from .value import Value


class XRef(BaseModel):
    """Cross-reference model for linking to external resources."""

    model_config = ConfigDict(extra='forbid')

    refid: Union[UUID, None] = Field(
        default=...,
        alias='refid',
        title='Reference ID',
        description='Reference ID for the external resource.',
    )

    kind: str = Field(
        default=...,
        alias='kind',
        title='Kind',
        description='Kind',
    )

    deprecated: Union[bool, None] = Field(
        default=None,
        alias='deprecated',
        title='Deprecated',
        description='Deprecated',
    )

    properties: Union[List[Value], None] = Field(
        default=None,
        alias='properties',
        title='Properties',
        description='Properties',
    )
