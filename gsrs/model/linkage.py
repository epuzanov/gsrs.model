from pydantic import Field, ConfigDict
from typing import List, Union

from .ginas_common_sub_data import GinasCommonSubData
from .site import Site

class Linkage(GinasCommonSubData):
    """Linkage model for the connector between sugar residues in a nucleic acid."""

    model_config = ConfigDict(extra='forbid')

    linkage: Union[str, None] = Field(
        default=None,
        alias='linkage',
        title='Linkage',
        description='Linking entity between sugar residues, such as phosphate or another linkage group.',
    )

    sites: Union[List[Site], None] = Field(
        default=None,
        alias='sites',
        title='Sites',
        description='Residue sites associated with the linkage within the sequence.',
    )

    def to_embedding_chunks(self) -> list[dict[str, object]]:
        linkage_type = self._clean_text(self.linkage)
        sites_shorthand = self._clean_text(self.sitesShorthand)
        if not linkage_type and not sites_shorthand:
            return []

        subject = self._embedding_root_name()
        document_id = self._embedding_document_id()
        access = 'protected' if getattr(self, 'access', None) else 'public'

        return [
            {
                'chunk_id': f'root_linkages_uuid:{self.uuid}',
                'document_id': document_id,
                'source_url': self._embedding_source_name(),
                'section': 'linkages',
                'text': f"{subject} {access} nucleic acid linkage {linkage_type or 'unspecified'} at {sites_shorthand or 'unspecified sites'}.".strip(),
                'metadata': {
                    **self._chunk_metadata(),
                    **self._hierarchy_metadata('root', 'linkages'),
                    'linkage_type': linkage_type or None,
                    'sites': sites_shorthand or None,
                },
            }
        ]
