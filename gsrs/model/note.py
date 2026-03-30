from pydantic import Field, ConfigDict
from typing import Union

from .ginas_common_sub_data import GinasCommonSubData

class Note(GinasCommonSubData):
    """Note model."""

    model_config = ConfigDict(extra='forbid')

    note: Union[str, None] = Field(
        default=...,
        alias='note',
        title='Note',
        description='Note',
    )

    def to_embedding_chunks(self) -> list[dict[str, object]]:
        note = self._clean_text(self.note)
        if not note:
            return []

        subject = self._embedding_root_name()
        document_id = self._embedding_document_id()

        return [
            {
                'chunk_id': f'root_notes_uuid:{self.uuid}',
                'document_id': document_id,
                'source_url': self._embedding_source_name(),
                'section': 'notes',
                'text': f'{subject} note: {note}',
                'metadata': {
                    **self._embedding_root_metadata(),
                    **self._hierarchy_metadata('root', 'notes'),
                    'json_path': '$.notes[*]',
                    'note_length': len(note),
                    'references': self._embedding_references() or None,
                },
            }
        ]
