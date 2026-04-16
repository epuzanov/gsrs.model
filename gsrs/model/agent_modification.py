from pydantic import Field, ConfigDict
from typing import Union

from .amount import Amount
from .ginas_common_sub_data import GinasCommonSubData
from .substance_reference import SubstanceReference

class AgentModification(GinasCommonSubData):
    """Agent Modification model."""

    model_config = ConfigDict(extra='forbid')

    agentModificationProcess: Union[str, None] = Field(
        default=None,
        alias='agentModificationProcess',
        title='Process',
        description='Process',
    )

    agentModificationRole: Union[str, None] = Field(
        default=None,
        alias='agentModificationRole',
        title='Role',
        description='Role',
    )

    agentModificationType: Union[str, None] = Field(
        default=None,
        alias='agentModificationType',
        title='Type',
        description='Type',
    )

    agentSubstance: Union[SubstanceReference, None] = Field(
        default=None,
        alias='agentSubstance',
        title='Substance',
        description='Substance',
    )

    amount: Union[Amount, None] = Field(
        default=None,
        alias='amount',
        title='Amount',
        description='Amount',
    )

    modificationGroup: Union[str, None] = Field(
        default=None,
        alias='modificationGroup',
        title='Modification Group',
        description='Modification Group',
    )

