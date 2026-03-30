from pydantic import Field, ConfigDict
from typing import Union

from .amount import Amount
from .ginas_common_sub_data import GinasCommonSubData
from .substance_reference import SubstanceReference

class Relationship(GinasCommonSubData):
    """Relationship model."""

    model_config = ConfigDict(extra='forbid')

    amount: Union[Amount, None] = Field(
        default=None,
        alias='amount',
        title='Amount',
        description='Amount',
    )
    comments: Union[str, None] = Field(
        default=None,
        alias='comments',
        title='Comments',
        description='Comments',
    )
    interactionType: Union[str, None] = Field(
        default=None,
        alias='interactionType',
        title='Interaction Type',
        description='Interaction Type',
    )
    originatorUuid: Union[str, None] = Field(
        default=None,
        alias='originatorUuid',
        title='Originator UUID',
        description='Originator UUID',
    )
    qualification: Union[str, None] = Field(
        default=None,
        alias='qualification',
        title='Qualification',
        description='Qualification',
    )
    relatedSubstance: SubstanceReference = Field(
        default=...,
        alias='relatedSubstance',
        title='Related Substance',
        description='Related Substance',
    )
    type: Union[str, None] = Field(
        default=...,
        alias='type',
        title='Relationship Type',
        description='Relationship Type',
    )
    mediatorSubstance: Union[SubstanceReference, None] = Field(
        default=None,
        alias='mediatorSubstance',
        title='Mediator Substance',
        description='Mediator Substance',
    )

    def to_embedding_chunks(self) -> list[dict[str, object]]:
        rel_type = self._clean_text(self.type)
        related_name = self.relatedSubstance.get_refPname()
        related_id = self.relatedSubstance.get_refuuid()
        qualification = self._clean_text(self.qualification)
        interaction_type = self._clean_text(self.interactionType)
        mediator_name = self.mediatorSubstance.get_refPname() if self.mediatorSubstance else ''
        mediator_id = self.mediatorSubstance.get_refuuid() if self.mediatorSubstance else ''
        amount_text = self.amount.as_string() if self.amount else ''
        comments = self._clean_text(self.comments)
        if not rel_type and not related_name:
            return []

        subject = self._embedding_root_name()
        document_id = self._embedding_document_id()
        parts = [f'{subject} has relationship {rel_type} with {related_name}.']
        if qualification:
            parts.append(f'Qualification {qualification}.')
        if interaction_type:
            parts.append(f'Interaction type {interaction_type}.')
        if mediator_name:
            parts.append(f'Mediator substance {mediator_name}.')
        if amount_text:
            parts.append(f'Amount {amount_text}.')
        if comments:
            parts.append(f'Comments {comments}.')

        return [
            {
                'chunk_id': f'root_relationships_uuid:{self.uuid}',
                'document_id': document_id,
                'source_url': self._embedding_source_name(),
                'section': 'relationships',
                'text': ' '.join(parts).strip(),
                'metadata': {
                    **self._embedding_root_metadata(),
                    **self._hierarchy_metadata('root', 'relationships'),
                    'json_path': '$.relationships[*]',
                    'relationship_type': rel_type or None,
                    'related_name': related_name or None,
                    'related_id': related_id or None,
                    'qualification': qualification or None,
                    'interaction_type': interaction_type or None,
                    'mediator_name': mediator_name or None,
                    'mediator_id': mediator_id or None,
                    'amount_text': amount_text or None,
                    'comments': comments or None,
                    'references': self._embedding_references() or None,
                },
            }
        ]
