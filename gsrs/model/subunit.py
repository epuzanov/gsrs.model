from pydantic import Field, ConfigDict
from typing import Union

from .ginas_common_sub_data import GinasCommonSubData

class Subunit(GinasCommonSubData):
    """Subunit model for an ordered linear sequence within a protein or nucleic acid."""

    model_config = ConfigDict(extra='forbid')

    sequence: str = Field(
        default=...,
        alias='sequence',
        title='Sequence',
        description='Primary sequence recorded in the appropriate biological direction for the subunit.',
    )

    subunitIndex: Union[float, None] = Field(
        default=None,
        alias='subunitIndex',
        title='Subunit Index',
        description='Ordinal index of the subunit within the full macromolecule.',
    )


    length: Union[float, None] = Field(
        default=None,
        alias='length',
        title='Length',
        description='Recorded residue length of the subunit sequence.',
    )

    def to_embedding_chunks(self) -> list[dict[str, object]]:
        sequence = self._clean_text(self.sequence)
        if not sequence:
            return []

        subject = self._embedding_root_name()
        document_id = self._embedding_document_id()

        return [
            {
                'chunk_id': f'root_subunits_uuid:{document_id}',
                'document_id': document_id,
                'source_url': self._embedding_source_name(),
                'section': 'subunits',
                'text': f"{subject} subunit {int(self.subunitIndex) if self.subunitIndex else 'unspecified'}: sequence length {self.length or len(sequence)} residues.",
                'metadata': {
                    **self._embedding_root_metadata(),
                    **self._hierarchy_metadata('root', 'subunits'),
                    'subunit_index': self.subunitIndex or None,
                    'sequence_length': self.length or len(sequence) if sequence else None,
                    'sequence': sequence[:500] if len(sequence) > 500 else sequence,
                },
            }
        ]
