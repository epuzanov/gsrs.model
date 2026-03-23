from pydantic import BaseModel, Field, ConfigDict
from typing import List, Union
from uuid import UUID

from .value import Value


class XRef(BaseModel):
    """Cross-reference model for linking to external resources."""

    model_config = ConfigDict(extra='forbid')

    refid: Union[UUID, None] = Field(
        ...,
        alias='refid',
        title='Reference ID',
        description='Reference ID for the external resource.',
        element_property=True,
    )

    kind: str = Field(
        ...,
        alias='kind',
        title='Kind',
        description='Kind',
        element_property=True,
    )

    deprecated: Union[bool, None] = Field(
        None,
        alias='deprecated',
        title='Deprecated',
        description='Deprecated',
        element_property=True,
    )

    properties: Union[List[Value], None] = Field(
        None,
        alias='properties',
        title='Properties',
        description='Properties',
        element_property=True,
    )
