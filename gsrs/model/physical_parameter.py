from pydantic import Field, ConfigDict
from typing import Union

from .amount import Amount
from .ginas_common_sub_data import GinasCommonSubData

class PhysicalParameter(GinasCommonSubData):
    """Physical Parameter model."""

    model_config = ConfigDict(extra='forbid')

    parameterName: str = Field(
        default=...,
        alias='parameterName',
        title='Parameter Name',
        description='Parameter Name',
    )

    amount: Union[Amount, None] = Field(
        default=None,
        alias='amount',
        title='Amount',
        description='Amount',
    )

    def to_embedding_chunks(self) -> list[dict[str, object]]:
        param_name = self._clean_text(self.parameterName)
        amount_text = self.amount.as_string() if self.amount else ''
        if not param_name and not amount_text:
            return []

        subject = self._embedding_root_name()
        document_id = self._embedding_document_id()

        return [
            {
                'chunk_id': f'root_physical_parameters_uuid:{document_id}',
                'document_id': document_id,
                'source_url': self._embedding_source_name(),
                'section': 'physical_parameters',
                'text': f"{subject} physical parameter {param_name}: {amount_text}.".strip(),
                'metadata': {
                    **self._embedding_root_metadata(),
                    **self._hierarchy_metadata('root', 'physical_parameters'),
                    'parameter_name': param_name or None,
                },
            }
        ]
