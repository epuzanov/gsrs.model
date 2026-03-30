from pydantic import Field, ConfigDict
from typing import List, Union

from .ginas_common_sub_data import GinasCommonSubData


class Reference(GinasCommonSubData):
    """Reference model."""

    model_config = ConfigDict(extra='forbid')

    citation: Union[str, None] = Field(
        default=None,
        alias='citation',
        title='Citation Text',
        description='Citation Text',
    )
    docType: str = Field(
        default=...,
        alias='docType',
        title='Reference Type',
        description='Reference Type',
    )
    documentDate: Union[float, None] = Field(
        default=None,
        alias='documentDate',
        title='Date Accessed',
        description='Date Accessed',
    )
    publicDomain: Union[bool, None] = Field(
        default=None,
        alias='publicDomain',
        title='Public Domain Reference',
        description='Public Domain Reference',
    )
    tags: Union[List[str], None] = Field(
        default=None,
        alias='tags',
        title='Tags',
        description='Tags',
    )
    uploadedFile: Union[str, None] = Field(
        default=None,
        alias='uploadedFile',
        title='Uploaded Document',
        description='Uploaded Document',
    )
    id: Union[str, None] = Field(
        default=None,
        alias='id',
        title='Ref_ID',
        description='Ref_ID',
    )
    url: Union[str, None] = Field(
        default=None,
        alias='url',
        title='Reference URL',
        description='Reference URL',
    )

    def embedding_reference_text(self) -> str:
        doc_type = self._clean_text(self.docType)
        citation = self._clean_text(self.citation)
        if doc_type and citation:
            return f'{doc_type}: {citation}'
        return doc_type or citation

    def to_embedding_chunks(self) -> list[dict[str, object]]:
        citation = self._clean_text(self.citation)
        doc_type = self._clean_text(self.docType)
        tags = self._clean_list(self.tags)
        reference_url = self._clean_text(self.url)
        uploaded_file = self._clean_text(self.uploadedFile)
        reference_id = self._clean_text(self.id or self.uuid)
        reference_text = self.embedding_reference_text()
        if not citation and not doc_type:
            return []

        subject = self._embedding_root_name()
        parts = [f'Reference for {subject}.']
        if doc_type:
            parts.append(f'Document type {doc_type}.')
        if citation:
            parts.append(f'Citation: {citation}.')
        if reference_url:
            parts.append(f'URL: {reference_url}.')

        document_id = self._embedding_document_id()

        return [
            {
                'chunk_id': f'root_references_uuid:{self.uuid}',
                'document_id': document_id,
                'source_url': self._embedding_source_name(),
                'section': 'references',
                'text': ' '.join(parts),
                'metadata': {
                    **self._embedding_root_metadata(),
                    **self._hierarchy_metadata('root', 'references'),
                    'json_path': '$.references[*]',
                    'references': [reference_text] if reference_text else None,
                    'doc_type': doc_type or None,
                    'citation': citation or None,
                    'reference_url': reference_url or None,
                    'reference_id': reference_id or None,
                    'uploaded_file': uploaded_file or None,
                    'public_domain': bool(self.publicDomain),
                    'tags': tags or None,
                },
            }
        ]
