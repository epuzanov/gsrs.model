from pydantic import Field, ConfigDict
from typing import Union

from .amount import Amount
from .component import Component

class SpecifiedSubstanceComponent(Component):
    """constituents model."""

    model_config = ConfigDict(extra='forbid')

    role: Union[str, None] = Field(
        default=None,
        alias='role',
        title='Role',
        description='Role',
    )

    amount: Union[Amount, None] = Field(
        default=None,
        alias='amount',
        title='Amount',
        description='Amount',
    )

    def to_embedding_chunks(self) -> list[dict[str, object]]:
        component_type = self.type.value if self.type else None
        substance_name = self.substance.get_refPname() if self.substance else ''
        role = self._clean_text(self.role)
        amount_text = self.amount.as_string() if self.amount else ''
        if not component_type and not substance_name and not role:
            return []

        subject = self._embedding_root_name()
        document_id = self._embedding_document_id()

        content_parts = [f"{subject} constituent"]
        if component_type:
            content_parts.append(f"type {component_type}")
        if substance_name:
            content_parts.append(f"substance {substance_name}")
        if role:
            content_parts.append(f"role {role}")
        if amount_text:
            content_parts.append(f"amount {amount_text}")

        return [
            {
                'chunk_id': f'root_constituents_uuid:{document_id}',
                'document_id': document_id,
                'source_url': self._embedding_source_name(),
                'section': 'constituents',
                'text': '. '.join(content_parts) + '.',
                'metadata': {
                    **self._embedding_root_metadata(),
                    **self._hierarchy_metadata('root', 'constituents'),
                    'component_type': component_type or None,
                    'substance_name': substance_name or None,
                    'substance_id': self.substance.get_refuuid() if self.substance else None,
                    'role': role or None,
                },
            }
        ]
