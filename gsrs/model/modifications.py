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
        default=None,
        alias='agentModifications',
        title='Agent Modifications',
        description='Agent Modifications',
    )
    physicalModifications: Union[List[PhysicalModification], None] = Field(
        default=None,
        alias='physicalModifications',
        title='Physical Modifications',
        description='Physical Modifications',
    )
    structuralModifications: Union[List[StructuralModification], None] = Field(
        default=None,
        alias='structuralModifications',
        title='Structural Modifications',
        description='Structural Modifications',
    )

    def to_embedding_chunks(self) -> list[dict[str, object]]:
        rows: list[dict[str, object]] = []

        for item in self.agentModifications or []:
            rows.extend(item.to_embedding_chunks())
        for item in self.physicalModifications or []:
            rows.extend(item.to_embedding_chunks())
        for item in self.structuralModifications or []:
            rows.extend(item.to_embedding_chunks())

        return rows
