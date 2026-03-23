from pydantic import Field, constr, ConfigDict
from typing import Any, Dict, List, Union

from .amount import Amount
from .ginas_common_sub_data import GinasCommonSubData

class Unit(GinasCommonSubData):
    """Unit model."""

    model_config = ConfigDict(extra='forbid')

    amap: Union[List[float], None] = Field(
        default=None,
        alias='amap',
        title='Amap',
        description='Amap',
    )

    amount: Union[Amount, None] = Field(
        default=None,
        alias='amount',
        title='Amount',
        description='Amount',
    )

    attachmentCount: Union[float, None] = Field(
        default=None,
        alias='attachmentCount',
        title='Attachment Count',
        description='Attachment Count',
    )

    attachmentMap: Union[
        dict[constr(pattern=r'^[_].*'), Any],
        dict[
            constr(pattern=r'^R[0-9][0-9]*$'),
            list[constr(pattern=r'^R[0-9][0-9]*$')]
        ],
        None
    ] = Field(
        default=None,
        alias='attachmentMap',
        title='Attachment Map',
        description='Attachment Map',
    )

    label: Union[str, None] = Field(
        default=None,
        alias='label',
        title='Label',
        description='Label',
    )

    structure: Union[str, None] = Field(
        default=None,
        alias='structure',
        title='Structure',
        description='Structure',
    )

    type: Union[str, None] = Field(
        default=None,
        alias='type',
        title='Type',
        description='Type',
    )
