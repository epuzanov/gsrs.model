from pydantic import Field, ConfigDict

from .structurally_diverse import StructurallyDiverse
from .substance import Substance

class StructurallyDiverseSubstance(Substance):
    """Structurally Diverse Substance model."""

    model_config = ConfigDict(extra='forbid')

    structurallyDiverse: StructurallyDiverse = Field(
        default=...,
        alias='structurallyDiverse',
        title='Structurally Diverse',
        description='Structurally Diverse definition for this substance.',
    )

    def _class_summary_chunks(self) -> list[dict[str, object]]:
        document_id = self._clean_text(self.uuid)
        species = self._clean_text(self.structurallyDiverse.organismSpecies if self.structurallyDiverse else None)

        return [
            {
                'chunk_id': f'root_structurallyDiverse_uuid:{document_id}',
                'document_id': document_id,
                'source': self._embedding_source_name(),
                'section': 'structurallyDiverse',
                'content': f'{self._stable_name()} is a structurally diverse substance. Organism species {species}.',
                'metadata': {
                    **self._chunk_metadata(self),
                    **self._hierarchy_metadata('root', 'structurallyDiverse'),
                    'substance_class': 'structurallyDiverse',
                    'organism_species': species or None,
                },
            }
        ]
