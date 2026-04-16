from pydantic import Field, ConfigDict
from typing import List

from .agent_modification import AgentModification
from .ginas_common_sub_data import GinasCommonSubData
from .physical_modification import PhysicalModification
from .structural_modification import StructuralModification

class Modifications(GinasCommonSubData):
    """Modifications model."""

    model_config = ConfigDict(extra='forbid')

    agentModifications: List[AgentModification] = Field(
        default_factory=list,
        alias='agentModifications',
        title='Agent Modifications',
        description='Agent Modifications',
    )

    physicalModifications: List[PhysicalModification] = Field(
        default_factory=list,
        alias='physicalModifications',
        title='Physical Modifications',
        description='Physical Modifications',
    )

    structuralModifications: List[StructuralModification] = Field(
        default_factory=list,
        alias='structuralModifications',
        title='Structural Modifications',
        description='Structural Modifications',
    )

