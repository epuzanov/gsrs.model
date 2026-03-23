from __future__ import annotations

from pydantic import Field, ConfigDict
from typing import Any, Dict, List, Union, Annotated
from typing_extensions import Annotated as TeAnnotated
import re

from .amount import Amount
from .ginas_common_sub_data import GinasCommonSubData


# Type aliases for attachment map keys and values
_RPattern = re.compile(r'^R[0-9][0-9]*$')
_UnderscorePattern = re.compile(r'^_.*$')

AttachmentMapValue = Union[
    Dict[str, Any],
    Dict[str, List[str]],
    None
]


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

    attachmentMap: Union[AttachmentMapValue, None] = Field(
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

    def to_embedding_chunks(self) -> list[dict[str, object]]:
        unit_type = self._clean_text(self.type)
        label = self._clean_text(self.label)
        amount_text = self.amount.as_string() if self.amount else ''
        if not unit_type and not label and not amount_text:
            return []

        subject = self._embedding_root_name()
        document_id = self._embedding_document_id()

        content_parts = [f"{subject} polymer unit"]
        if unit_type:
            content_parts.append(f"type {unit_type}")
        if label:
            content_parts.append(f"label {label}")
        if amount_text:
            content_parts.append(f"amount {amount_text}")

        return [
            {
                'chunk_id': f'root_units_uuid:{document_id}',
                'document_id': document_id,
                'source': self._embedding_source_name(),
                'section': 'units',
                'content': '. '.join(content_parts) + '.',
                'metadata': {
                    **self._embedding_root_metadata(),
                    **self._hierarchy_metadata('root', 'units'),
                    'unit_type': unit_type or None,
                    'label': label or None,
                    'attachment_count': self.attachmentCount or None,
                },
            }
        ]
