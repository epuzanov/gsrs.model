from pydantic import Field, ConfigDict
from typing import Union
from enum import Enum

from .ginas_common_sub_data import GinasCommonSubData


class SubstanceClass(Enum):
    """Enumeration of GSRS substance classes."""

    reference = 'reference'

class SubstanceReference(GinasCommonSubData):
    """Hybrid Species Paternal Organism model."""

    model_config = ConfigDict(extra='forbid')

    refPname: Union[str, None] = Field(
        default=None,
        alias='refPname',
        title='Referenced Substance Name',
        description='Referenced Substance Name',
    )

    name: Union[str, None] = Field(
        default=None,
        alias='name',
        title='Name',
        description='Name',
    )

    linkingID: Union[str, None] = Field(
        default=None,
        alias='linkingID',
        title='Linking ID',
        description='Linking ID',
    )

    refuuid: str = Field(
        default=...,
        alias='refuuid',
        title='Refuuid',
        description='Refuuid',
    )

    substanceClass: Union[SubstanceClass, None] = Field(
        default=None,
        alias='substanceClass',
        title='Substance Class',
        description='Substance Class',
    )

    approvalID: Union[str, None] = Field(
        default=None,
        alias='approvalID',
        title='Approval ID',
        description='Approval ID',
    )

    def get_refPname(self) -> str:
        """Get the referenced substance name."""
        return self._clean_text(self.refPname or self.name or self.approvalID or self.refuuid or self.linkingID)

    def get_refuuid(self) -> str:
        """Get the referenced substance ID."""
        return self._clean_text(self.approvalID or self.refuuid or self.linkingID or self.uuid)

    def to_embedding_chunks(self) -> list[dict[str, object]]:
        ref_name = self.get_refPname()
        approval_id = self._clean_text(self.approvalID)
        if not ref_name and not approval_id:
            return []

        subject = self._embedding_root_name()
        document_id = self._embedding_document_id()

        content_parts = [f"{subject} references substance"]
        if ref_name:
            content_parts.append(ref_name)
        if approval_id:
            content_parts.append(f"approval ID {approval_id}")

        return [
            {
                'chunk_id': f'root_substance_references_uuid:{document_id}',
                'document_id': document_id,
                'source_url': self._embedding_source_name(),
                'section': 'substance_references',
                'text': '. '.join(content_parts) + '.',
                'metadata': {
                    **self._embedding_root_metadata(),
                    **self._hierarchy_metadata('root', 'substance_references'),
                    'referenced_name': ref_name or None,
                    'referenced_id': self.get_refuuid() or None,
                    'approval_id': approval_id or None,
                },
            }
        ]
