from pydantic import Field, ConfigDict
from typing import Union

from .ginas_common_sub_data import GinasCommonSubData

class Code(GinasCommonSubData):
    """Code model."""

    model_config = ConfigDict(extra='forbid')

    codeText: Union[str, None] = Field(
        default=None,
        alias='codeText',
        title='Code Text',
        description='Code Text',
    )
    codeSystem: Union[str, None] = Field(
        default=None,
        alias='codeSystem',
        title='Code system',
        description='Code system',
    )
    code: str = Field(
        default=...,
        alias='code',
        title='Code',
        description='Code',
    )
    comments: Union[str, None] = Field(
        default=None,
        alias='comments',
        title='Code Comments',
        description='Code Comments',
    )
    type: Union[str, None] = Field(
        default=None,
        alias='type',
        title='Code Type',
        description='Code Type',
    )
    url: Union[str, None] = Field(
        default=None,
        alias='url',
        title='Code URL',
        description='Code URL',
    )
    isClassification: Union[bool, None] = Field(
        default=None,
        alias='_isClassification',
        title='Classification Flag',
        description='System flag indicating whether the code is treated as a classification.',
    )

    def to_embedding_chunks(self) -> list[dict[str, object]]:
        code_system = self._clean_text(self.codeSystem)
        code = self._clean_text(self.code)
        code_type = self._clean_text(self.type)
        code_text = self._clean_text(self.codeText)
        comments = self._clean_text(self.comments)
        url = self._clean_text(self.url)
        access = 'protected' if getattr(self, 'access', None) else 'public'
        if not code:
            return []

        subject = self._embedding_root_name()
        document_id = self._embedding_document_id()
        text_parts = [f"{subject} {access} {code_type.lower()}"]
        class_parts = []
        class_metadata = {}
        if self.isClassification:
            text_parts.append(f"classification in {code_system or 'unknown'} code system:")
            class_parts = [self._clean_text(part) for part in (self.comments or '').split('|')]
            class_parts = [part for part in class_parts if part]
            if class_parts:
                class_metadata = {
                    'classification_hierarchy': class_parts,
                    'classification_path': ' > '.join(class_parts),
                }
                text_parts.append(f"{class_metadata['classification_path']}.")
            else:
                text_parts.append(f"{code}.")
        else:
            text_parts.append(f"Identifier in {code_system or 'unknown'} code system: {code}.")
        if code_text and code_text != code:
            text_parts.append(f'Code text {code_text}.')
        rows = [
            {
                'chunk_id': f'root_codes_uuid:{self.uuid}',
                'document_id': document_id,
                'source_url': self._embedding_source_name(),
                'section': 'codes',
                'text': ' '.join(text_parts),
                'metadata': {
                    **self._embedding_root_metadata(),
                    **self._hierarchy_metadata('root', 'codes'),
                    **class_metadata,
                    'json_path': self._embedding_json_path('$.codes[*]'),
                    'code_system': code_system or None,
                    'code': code,
                    'code_type': code_type or None,
                    'code_text': code_text or None,
                    'comments': comments or None,
                    'url': url or None,
                    'references': self._embedding_references() or None,
                },
            }
        ]
        return rows
