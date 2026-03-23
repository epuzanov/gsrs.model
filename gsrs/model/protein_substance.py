from pydantic import Field, ConfigDict
from typing import Union

from .protein import Protein
from .substance import Substance

class ProteinSubstance(Substance):
    """Protein Substance model."""

    model_config = ConfigDict(extra='forbid')

    protein: Union[Protein, None] = Field(
        None,
        alias='protein',
        title='Protein',
        description='Protein definition for this substance.',
        element_property=True,
    )

    def _class_summary_chunks(self) -> list[dict[str, object]]:
        document_id = self._clean_text(self.uuid)
        count = len(self.protein.subunits or []) if self.protein else 0

        return [
            {
                'chunk_id': f'root_protein_uuid:{document_id}',
                'document_id': document_id,
                'source': self._embedding_source_name(),
                'section': 'protein',
                'content': f'{self._stable_name()} belongs to substance class protein. Protein has {count} subunits.',
                'metadata': {
                    **self._chunk_metadata(self),
                    **self._hierarchy_metadata('root', 'protein'),
                    'substance_class': 'protein',
                    'protein_subunit_count': count,
                },
            }
        ]
