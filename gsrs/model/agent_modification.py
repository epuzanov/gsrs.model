from pydantic import Field, ConfigDict
from typing import Union

from .amount import Amount
from .ginas_common_sub_data import GinasCommonSubData
from .substance_reference import SubstanceReference

class AgentModification(GinasCommonSubData):
    """Agent Modification model."""

    model_config = ConfigDict(extra='forbid')

    agentModificationProcess: Union[str, None] = Field(
        None,
        alias='agentModificationProcess',
        title='Process',
        description='Process',
        element_property=True,
    )

    agentModificationRole: Union[str, None] = Field(
        None,
        alias='agentModificationRole',
        title='Role',
        description='Role',
        element_property=True,
    )

    agentModificationType: str = Field(
        ...,
        alias='agentModificationType',
        title='Type',
        description='Type',
        element_property=True,
    )

    agentSubstance: SubstanceReference = Field(
        ...,
        alias='agentSubstance',
        title='Substance',
        description='Substance',
        element_property=True,
    )

    amount: Union[Amount, None] = Field(
        None,
        alias='amount',
        title='Amount',
        description='Amount',
        element_property=True,
    )

    modificationGroup: Union[str, None] = Field(
        None,
        alias='modificationGroup',
        title='Modification Group',
        description='Modification Group',
        element_property=True,
    )
