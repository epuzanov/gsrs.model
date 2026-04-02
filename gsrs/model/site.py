from pydantic import BaseModel, Field, ConfigDict
from typing import Union

class Site(BaseModel):
    """Site model."""

    model_config = ConfigDict(extra='forbid')

    subunitIndex: Union[int, None] = Field(
        default=None,
        alias='subunitIndex',
        title='Subunit Index',
        description='Subunit Index',
    )

    residueIndex: Union[int, None] = Field(
        default=None,
        alias='residueIndex',
        title='Residue Index',
        description='Residue Index',
    )
