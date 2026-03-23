from pydantic import Field, ConfigDict

from .specified_substance_g1 import SpecifiedSubstanceG1
from .substance import Substance

class SpecifiedSubstanceG1Substance(Substance):
    """Specified Substance model."""

    model_config = ConfigDict(extra='forbid')

    specifiedSubstance: SpecifiedSubstanceG1 = Field(
        default=...,
        alias='specifiedSubstance',
        title='specifiedSubstance',
        description='Specified Substance definition for this substance.',
    )

    def _class_summary_chunks(self) -> list[dict[str, object]]:
        document_id = self._clean_text(self.uuid)
        count = len(self.specifiedSubstance.constituents or []) if self.specifiedSubstance else 0

        return [
            {
                'chunk_id': f'root_specifiedSubstance_uuid:{document_id}',
                'document_id': document_id,
                'source': self._embedding_source_name(),
                'section': 'specifiedSubstance',
                'content': f'{self._stable_name()} belongs to substance class specifiedSubstanceG1. It has {count} constituents.',
                'metadata': {
                    **self._chunk_metadata(self),
                    **self._hierarchy_metadata('root', 'specifiedSubstance'),
                    'substance_class': 'specifiedSubstanceG1',
                    'specified_substance_constituent_count': count,
                },
            }
        ]
