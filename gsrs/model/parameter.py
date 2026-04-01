from pydantic import Field, ConfigDict
from typing import Union

from .amount import Amount
from .ginas_common_sub_data import GinasCommonSubData

class Parameter(GinasCommonSubData):
    """Parameter model."""

    model_config = ConfigDict(extra='forbid')

    name: str = Field(
        default=...,
        alias='name',
        title='Parameter Name',
        description='Parameter Name',
    )

    type: Union[str, None] = Field(
        default=None,
        alias='type',
        title='Parameter Type',
        description='Parameter Type',
    )

    value: Union[Amount, None] = Field(
        default=None,
        alias='value',
        title='Amount',
        description='Amount',
    )

    def to_embedding_chunks(self) -> list[dict[str, object]]:
        param_name = self._clean_text(self.name)
        param_type = self._clean_text(self.type)
        value_text = self.value.as_string() if self.value else ''
        if not param_name and not value_text:
            return []

        subject = self._embedding_root_name()
        document_id = self._embedding_document_id()
        access = 'protected' if getattr(self, 'access', None) else 'public'

        return [
            {
                'chunk_id': f'root_parameters_uuid:{self.uuid}',
                'document_id': document_id,
                'source_url': self._embedding_source_name(),
                'section': 'parameters',
                'text': f"{subject} {access} parameter {param_name}{f' ({param_type})' if param_type else ''}: {value_text}.".strip(),
                'metadata': {
                    **self._chunk_metadata(),
                    **self._hierarchy_metadata('root', 'parameters'),
                    'parameter_name': param_name or None,
                    'parameter_type': param_type or None,
                },
            }
        ]
