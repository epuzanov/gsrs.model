from pydantic import Field, ConfigDict
from typing import List, Union

from .ginas_common_sub_data import GinasCommonSubData
from .site import Site

class DisulfideLink(GinasCommonSubData):
    """Disulfide Link model."""

    model_config = ConfigDict(extra='forbid')

    sites: Union[List[Site], None] = Field(
        default=None,
        alias='sites',
        title='Disulfide Sites',
        description='Disulfide Sites',
        max_length=2,
        min_length=2,
    )

    def to_embedding_chunks(self) -> list[dict[str, object]]:
        sites_shorthand = self._clean_text(self.sitesShorthand)
        if not sites_shorthand:
            return []

        subject = self._embedding_root_name()
        document_id = self._embedding_document_id()

        return [
            {
                'chunk_id': f'root_disulfide_links_uuid:{self.uuid}',
                'document_id': document_id,
                'source_url': self._embedding_source_name(),
                'section': 'disulfide_links',
                'text': f"{subject} disulfide bond at {sites_shorthand}.",
                'metadata': {
                    **self._embedding_root_metadata(),
                    **self._hierarchy_metadata('root', 'disulfide_links'),
                    'sites': sites_shorthand or None,
                },
            }
        ]
