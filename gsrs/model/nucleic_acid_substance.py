from pydantic import Field, ConfigDict
from typing import Union

from .nucleic_acid import NucleicAcid
from .substance import Substance

class NucleicAcidSubstance(Substance):
    """Nucleic Acid Substance model."""

    model_config = ConfigDict(extra='forbid')

    nucleicAcid: Union[NucleicAcid, None] = Field(
        default=None,
        alias='nucleicAcid',
        title='Nucleic Acid',
        description='Nucleic Acid definition for this substance.',
    )

    def _class_summary_chunks(self) -> list[dict[str, object]]:
        document_id = self._clean_text(self.uuid)
        count = len(self.nucleicAcid.subunits or []) if self.nucleicAcid else 0

        return [
            {
                'chunk_id': f'root_nucleicAcid_uuid:{document_id}',
                'document_id': document_id,
                'source_url': self._embedding_source_name(),
                'section': 'nucleicAcid',
                'text': f'{self._stable_name()} belongs to substance class nucleicAcid. Nucleic acid has {count} subunits.',
                'metadata': {
                    **self._chunk_metadata(self),
                    **self._hierarchy_metadata('root', 'nucleicAcid'),
                    'substance_class': 'nucleicAcid',
                    'na_subunit_count': count,
                },
            }
        ]
