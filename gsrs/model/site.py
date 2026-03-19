from pydantic import BaseModel, Field, ConfigDict
from typing import Union

class Site(BaseModel):
    """Site model."""

    model_config = ConfigDict(extra='forbid')

    subunitIndex: Union[float, None] = Field(
        None,
        alias='subunitIndex',
        title='Subunit Index',
        description='Subunit Index',
        element_property=True,
    )

    residueIndex: Union[float, None] = Field(
        None,
        alias='residueIndex',
        title='Residue Index',
        description='Residue Index',
        element_property=True,
    )
