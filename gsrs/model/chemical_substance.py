from pydantic import Field, ConfigDict
from typing import List

from .ginas_chemical_structure import GinasChemicalStructure
from .moiety import Moiety
from .substance import Substance, SubstanceClass

class ChemicalSubstance(Substance):
    """Chemical Substance model."""

    model_config = ConfigDict(extra='forbid')

    substanceClass: SubstanceClass = Field(
        SubstanceClass.chemical,
        alias='substanceClass',
        title='Substance Type',
        description='Substance Type',
    )
    structure: GinasChemicalStructure = Field(
        default=...,
        alias='structure',
        title='Chemical Structure',
        description='Chemical Structure definition for this substance.',
    )
    moieties: List[Moiety] = Field(
        default=...,
        alias='moieties',
        title='Chemical Moieties',
        description='Chemical Moieties',
        min_length=1,
    )

    def _class_summary_chunks(self) -> list[dict[str, object]]:
        document_id = self._clean_text(self.uuid)
        formula = self._clean_text(self.structure.formula if self.structure else None)

        return [
            {
                'chunk_id': f'root_structure_uuid:{document_id}',
                'document_id': document_id,
                'source_url': self._embedding_source_name(),
                'section': 'structure',
                'text': f'{self._stable_name()} belongs to substance class chemical. Formula {formula}.'.strip(),
                'metadata': {
                    **self._chunk_metadata(self),
                    **self._hierarchy_metadata('root', 'structure'),
                    'substance_class': 'chemical',
                    'formula': formula or None,
                    'molecular_weight': self.structure.mwt if self.structure else None,
                },
            }
        ]
