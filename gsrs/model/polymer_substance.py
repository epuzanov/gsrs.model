from pydantic import Field, ConfigDict
from typing import Union

from .polymer import Polymer
from .substance import Substance

class PolymerSubstance(Substance):
    """Polymer Substance model."""

    model_config = ConfigDict(extra='forbid')

    polymer: Union[Polymer, None] = Field(
        default=None,
        alias='polymer',
        title='Polymer',
        description='Polymer definition for this substance.',
    )

    def _class_summary_chunks(self) -> list[dict[str, object]]:
        document_id = self._clean_text(self.uuid)
        count = len(self.polymer.monomers or []) if self.polymer else 0

        return [
            {
                'chunk_id': f'root_polymer_uuid:{document_id}',
                'document_id': document_id,
                'source_url': self._embedding_source_name(),
                'section': 'polymer',
                'text': f'{self._stable_name()} belongs to substance class polymer. Polymer has {count} monomers.',
                'metadata': {
                    **self._chunk_metadata(self),
                    **self._hierarchy_metadata('root', 'polymer'),
                    'substance_class': 'polymer',
                    'polymer_monomer_count': count,
                },
            }
        ]
