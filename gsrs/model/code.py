from pydantic import Field, ConfigDict
from typing import Union

from .ginas_common_sub_data import GinasCommonSubData

class Code(GinasCommonSubData):
    """Code model."""

    model_config = ConfigDict(extra='forbid')

    codeText: Union[str, None] = Field(
        None,
        alias='codeText',
        title='Code Text',
        description='Code Text',
        element_property=True,
    )
    codeSystem: Union[str, None] = Field(
        None,
        alias='codeSystem',
        title='Code system',
        description='Code system',
        element_property=True,
    )
    code: str = Field(
        ...,
        alias='code',
        title='Code',
        description='Code',
        element_property=True,
    )
    comments: Union[str, None] = Field(
        None,
        alias='comments',
        title='Code Comments',
        description='Code Comments',
        element_property=True,
    )
    type: Union[str, None] = Field(
        None,
        alias='type',
        title='Code Type',
        description='Code Type',
        element_property=True,
    )
    url: Union[str, None] = Field(
        None,
        alias='url',
        title='Code URL',
        description='Code URL',
        element_property=True,
    )
    isClassification: Union[bool, None] = Field(
        None,
        alias='_isClassification',
        title='Classification Flag',
        description='System flag indicating whether the code is treated as a classification.',
        element_property=True,
    )

    def to_embedding_chunks(self) -> list[dict[str, object]]:
        code_system = self._clean_text(self.codeSystem)
        code = self._clean_text(self.code)
        if not code:
            return []

        subject = self._embedding_root_name()
        document_id = self._embedding_document_id()
        rows = [
            {
                'chunk_id': f'root_codes_uuid:{document_id}',
                'document_id': document_id,
                'source': self._embedding_source_name(),
                'section': 'codes',
                'content': f"{subject} identifier in {code_system or 'unknown system'}: {code}.",
                'metadata': {
                    **self._embedding_root_metadata(),
                    **self._hierarchy_metadata('root', 'codes'),
                    'code_system': code_system or None,
                    'code': code,
                },
            }
        ]

        if self.isClassification:
            class_parts = [self._clean_text(part) for part in (self.comments or '').split('|')]
            class_parts = [part for part in class_parts if part]
            if class_parts:
                rows.append(
                    {
                        'chunk_id': f'root_classifications_uuid:{document_id}',
                        'document_id': document_id,
                        'source': self._embedding_source_name(),
                        'section': 'classifications',
                        'content': (
                            f"{subject} classification in {code_system or 'unknown system'}: "
                            f"{' > '.join(class_parts)}."
                        ),
                        'metadata': {
                            **self._embedding_root_metadata(),
                            **self._hierarchy_metadata('root', 'classifications'),
                            'code_system': code_system or None,
                            'code': code,
                            'classification_hierarchy': class_parts,
                            'classification_path': ' > '.join(class_parts),
                        },
                    }
                )

        return rows
