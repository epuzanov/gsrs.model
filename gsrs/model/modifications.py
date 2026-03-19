from pydantic import Field, ConfigDict
from typing import List, Union

from .agent_modification import AgentModification
from .ginas_common_sub_data import GinasCommonSubData
from .physical_modification import PhysicalModification
from .structural_modification import StructuralModification

class Modifications(GinasCommonSubData):
    """Modifications model."""

    model_config = ConfigDict(extra='forbid')

    agentModifications: Union[List[AgentModification], None] = Field(
        None,
        alias='agentModifications',
        title='Agent Modifications',
        description='Agent Modifications',
        element_property=True,
    )

    physicalModifications: Union[List[PhysicalModification], None] = Field(
        None,
        alias='physicalModifications',
        title='Physical Modifications',
        description='Physical Modifications',
        element_property=True,
    )

    structuralModifications: Union[List[StructuralModification], None] = Field(
        None,
        alias='structuralModifications',
        title='Structural Modifications',
        description='Structural Modifications',
        element_property=True,
    )
