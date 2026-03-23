from pydantic import Field, ConfigDict
from typing import List, Union

from .ginas_common_sub_data import GinasCommonSubData

class Reference(GinasCommonSubData):
    """Reference model."""

    model_config = ConfigDict(extra='forbid')

    citation: Union[str, None] = Field(
        None,
        alias='citation',
        title='Citation Text',
        description='Citation Text',
        element_property=True,
    )
    docType: str = Field(
        ...,
        alias='docType',
        title='Reference Type',
        description='Reference Type',
        element_property=True,
    )
    documentDate: Union[float, None] = Field(
        None,
        alias='documentDate',
        title='Date Accessed',
        description='Date Accessed',
        element_property=True,
    )
    publicDomain: Union[bool, None] = Field(
        None,
        alias='publicDomain',
        title='Public Domain Reference',
        description='Public Domain Reference',
        element_property=True,
    )
    tags: Union[List[str], None] = Field(
        None,
        alias='tags',
        title='Tags',
        description='Tags',
        element_property=True,
    )
    uploadedFile: Union[str, None] = Field(
        None,
        alias='uploadedFile',
        title='Uploaded Document',
        description='Uploaded Document',
        element_property=True,
    )
    id: Union[str, None] = Field(
        None,
        alias='id',
        title='Ref_ID',
        description='Ref_ID',
        element_property=True,
    )
    url: Union[str, None] = Field(
        None,
        alias='url',
        title='Reference URL',
        description='Reference URL',
        element_property=True,
    )

    def to_embedding_chunks(self) -> list[dict[str, object]]:
        citation = self._clean_text(self.citation)
        doc_type = self._clean_text(self.docType)
        if not citation and not doc_type:
            return []

        subject = self._embedding_root_name()
        parts = [f'Reference for {subject}.']
        if doc_type:
            parts.append(f'Document type {doc_type}.')
        if citation:
            parts.append(f'Citation: {citation}.')

        document_id = self._embedding_document_id()

        return [
            {
                'chunk_id': f'root_references_uuid:{document_id}',
                'document_id': document_id,
                'source': self._embedding_source_name(),
                'section': 'references',
                'content': ' '.join(parts),
                'metadata': {
                    **self._embedding_root_metadata(),
                    **self._hierarchy_metadata('root', 'references'),
                    'doc_type': doc_type or None,
                    'citation': citation or None,
                },
            }
        ]
