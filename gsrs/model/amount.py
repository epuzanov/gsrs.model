from pydantic import Field, ConfigDict
from typing import Union

from .ginas_common_sub_data import GinasCommonSubData

class Amount(GinasCommonSubData):
    """Amount model."""

    model_config = ConfigDict(extra='forbid')

    type: Union[str, None] = Field(
        default=None,
        alias='type',
        title='Amount Type',
        description='Amount Type',
    )

    average: Union[float, None] = Field(
        default=None,
        alias='average',
        title='Average',
        description='Average',
    )

    highLimit: Union[float, None] = Field(
        default=None,
        alias='highLimit',
        title='High Limit',
        description='High Limit',
    )

    high: Union[float, None] = Field(
        default=None,
        alias='high',
        title='High',
        description='High',
    )

    lowLimit: Union[float, None] = Field(
        default=None,
        alias='lowLimit',
        title='Low Limit',
        description='Low Limit',
    )

    low: Union[float, None] = Field(
        default=None,
        alias='low',
        title='Low',
        description='Low',
    )

    units: Union[str, None] = Field(
        default=None,
        alias='units',
        title='Units',
        description='Units',
    )

    nonNumericValue: Union[str, None] = Field(
        default=None,
        alias='nonNumericValue',
        title='Non-numeric Value',
        description='Non-numeric Value',
    )

    def as_string(self) -> str:
        """Render the amount value as a human-readable string."""
        pieces: list[str] = []
        non_numeric = self._clean_text(self.nonNumericValue)
        avg = self.average
        low = self.low
        high = self.high
        low_limit = self.lowLimit
        high_limit = self.highLimit
        units = self._clean_text(self.units)
        amount_type = self._clean_text(self.type)
        if non_numeric:
            pieces.append(non_numeric)
        elif avg is not None:
            pieces.append(str(avg))
        elif low is not None and high is not None:
            pieces.append(f'{low} to {high}')
        elif low_limit is not None and high_limit is not None:
            pieces.append(f'{low_limit} to {high_limit}')
        elif low is not None:
            pieces.append(str(low))
        elif high is not None:
            pieces.append(str(high))
        if units:
            pieces.append(units)
        if amount_type:
            pieces.append(f'(amount type {amount_type})')
        return ' '.join(pieces).strip()

    def to_embedding_chunks(self) -> list[dict[str, object]]:
        amount_text = self.as_string()
        if not amount_text:
            return []

        subject = self._embedding_root_name()
        document_id = self._embedding_document_id()
        amount_type = self._clean_text(self.type)

        return [
            {
                'chunk_id': f'root_amount_uuid:{document_id}',
                'document_id': document_id,
                'source': self._embedding_source_name(),
                'section': 'amount',
                'content': f"{subject} amount: {amount_text}.",
                'metadata': {
                    **self._embedding_root_metadata(),
                    **self._hierarchy_metadata('root', 'amount'),
                    'amount_type': amount_type or None,
                    'units': self._clean_text(self.units) or None,
                },
            }
        ]
