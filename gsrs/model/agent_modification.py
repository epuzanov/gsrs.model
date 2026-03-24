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
    agentModificationType: str = Field(
        default=...,
        alias='agentModificationType',
        title='Type',
        description='Type',
    )
    agentSubstance: SubstanceReference = Field(
        default=...,
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

    def to_embedding_chunks(self) -> list[dict[str, object]]:
        subject = self._embedding_root_name()
        document_id = self._embedding_document_id()

        return [
            {
                'chunk_id': f'root_modifications_agentModifications_uuid:{self.uuid}',
                'document_id': document_id,
                'source_url': self._embedding_source_name(),
                'section': 'agentModifications',
                'text': f'{subject} agent modification type {self._clean_text(self.agentModificationType)}.',
                'metadata': {
                    **self._embedding_root_metadata(),
                    **self._hierarchy_metadata('root', 'modifications', 'agentModifications'),
                    'modification_kind': 'agent',
                },
            }
        ]
