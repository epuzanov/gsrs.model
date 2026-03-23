from pydantic import Field, ConfigDict
from typing import Union

from .amount import Amount
from .ginas_common_sub_data import GinasCommonSubData
from .substance_reference import SubstanceReference

class Relationship(GinasCommonSubData):
    """Relationship model."""

    model_config = ConfigDict(extra='forbid')

    amount: Union[Amount, None] = Field(
        None,
        alias='amount',
        title='Amount',
        description='Amount',
        element_property=True,
    )
    comments: Union[str, None] = Field(
        None,
        alias='comments',
        title='Comments',
        description='Comments',
        element_property=True,
    )
    interactionType: Union[str, None] = Field(
        None,
        alias='interactionType',
        title='Interaction Type',
        description='Interaction Type',
        element_property=True,
    )
    originatorUuid: Union[str, None] = Field(
        None,
        alias='originatorUuid',
        title='Originator UUID',
        description='Originator UUID',
        element_property=True,
    )
    qualification: Union[str, None] = Field(
        None,
        alias='qualification',
        title='Qualification',
        description='Qualification',
        element_property=True,
    )
    relatedSubstance: SubstanceReference = Field(
        None,
        alias='relatedSubstance',
        title='Related Substance',
        description='Related Substance',
        element_property=True,
    )
    type: Union[str, None] = Field(
        ...,
        alias='type',
        title='Relationship Type',
        description='Relationship Type',
        element_property=True,
    )
    mediatorSubstance: Union[SubstanceReference, None] = Field(
        None,
        alias='mediatorSubstance',
        title='Mediator Substance',
        description='Mediator Substance',
        element_property=True,
    )

    def to_embedding_chunks(self) -> list[dict[str, object]]:
        rel_type = self._clean_text(self.type)
        related_name = self._pick_substance_ref_name(self.relatedSubstance)
        if not rel_type and not related_name:
            return []

        subject = self._embedding_root_name()
        document_id = self._embedding_document_id()

        return [
            {
                'chunk_id': f'root_relationships_uuid:{document_id}',
                'document_id': document_id,
                'source': self._embedding_source_name(),
                'section': 'relationships',
                'content': f"{subject} has relationship {rel_type} with {related_name}.".strip(),
                'metadata': {
                    **self._embedding_root_metadata(),
                    **self._hierarchy_metadata('root', 'relationships'),
                    'relationship_type': rel_type or None,
                    'related_name': related_name or None,
                    'related_id': self._pick_substance_ref_id(self.relatedSubstance) or None,
                },
            }
        ]
