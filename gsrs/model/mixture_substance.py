from pydantic import Field, ConfigDict

from .mixture import Mixture
from .substance import Substance

class MixtureSubstance(Substance):
    """Mixture Substance model."""

    model_config = ConfigDict(extra='forbid')

    mixture: Mixture = Field(
        default=...,
        alias='mixture',
        title='Mixture',
        description='Mixture definition for this substance.',
    )

    def _class_summary_chunks(self) -> list[dict[str, object]]:
        document_id = self._clean_text(self.uuid)
        count = len(self.mixture.components or []) if self.mixture else 0

        return [
            {
                'chunk_id': f'root_mixture_uuid:{document_id}',
                'document_id': document_id,
                'source_url': self._embedding_source_name(),
                'section': 'mixture',
                'text': f'{self._stable_name()} belongs to substance class mixture. Mixture has {count} components.',
                'metadata': {
                    **self._chunk_metadata(self),
                    **self._hierarchy_metadata('root', 'mixture'),
                    'substance_class': 'mixture',
                    'mixture_component_count': count,
                },
            }
        ]
