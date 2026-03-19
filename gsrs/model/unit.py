from pydantic import Field, constr, ConfigDict
from typing import Any, Dict, List, Union

from .amount import Amount
from .ginas_common_sub_data import GinasCommonSubData

class Unit(GinasCommonSubData):
    """Unit model."""

    model_config = ConfigDict(extra='forbid')

    amap: Union[List[float], None] = Field(
        None,
        alias='amap',
        title='Amap',
        description='Amap',
        element_property=True,
    )

    amount: Union[Amount, None] = Field(
        None,
        alias='amount',
        title='Amount',
        description='Amount',
        element_property=True,
    )

    attachmentCount: Union[float, None] = Field(
        None,
        alias='attachmentCount',
        title='Attachment Count',
        description='Attachment Count',
        element_property=True,
    )

    attachmentMap: Union[
        dict[constr(pattern=r'^[_].*'), Any],
        dict[
            constr(pattern=r'^R[0-9][0-9]*$'),
            list[constr(pattern=r'^R[0-9][0-9]*$')]
        ],
        None
    ] = Field(
        None,
        alias='attachmentMap',
        title='Attachment Map',
        description='Attachment Map',
        element_property=True,
    )

    label: Union[str, None] = Field(
        None,
        alias='label',
        title='Label',
        description='Label',
        element_property=True,
    )

    structure: Union[str, None] = Field(
        None,
        alias='structure',
        title='Structure',
        description='Structure',
        element_property=True,
    )

    type: Union[str, None] = Field(
        None,
        alias='type',
        title='Type',
        description='Type',
        element_property=True,
    )
