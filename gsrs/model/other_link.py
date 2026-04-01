from pydantic import Field, ConfigDict
from typing import List, Union

from .ginas_common_sub_data import GinasCommonSubData
from .site import Site

class OtherLink(GinasCommonSubData):
    """Other Linkage model."""

    model_config = ConfigDict(extra='forbid')

    sites: Union[List[Site], None] = Field(
        default=None,
        alias='sites',
        title='Linkage sites',
        description='Linkage sites',
        min_length=2,
    )

    linkageType: str = Field(
        default=...,
        alias='linkageType',
        title='Linkage type',
        description='Linkage type',
    )

    def to_embedding_chunks(self) -> list[dict[str, object]]:
        linkage_type = self._clean_text(self.linkageType)
        sites_shorthand = self._clean_text(self.sitesShorthand)
        if not linkage_type and not sites_shorthand:
            return []

        subject = self._embedding_root_name()
        document_id = self._embedding_document_id()
        access = 'protected' if getattr(self, 'access', None) else 'public'

        return [
            {
                'chunk_id': f'root_other_links_uuid:{self.uuid}',
                'document_id': document_id,
                'source_url': self._embedding_source_name(),
                'section': 'other_links',
                'text': f"{subject} {access} linkage type {linkage_type or 'unspecified'} at {sites_shorthand or 'unspecified sites'}.".strip(),
                'metadata': {
                    **self._chunk_metadata(),
                    **self._hierarchy_metadata('root', 'other_links'),
                    'linkage_type': linkage_type or None,
                    'sites': sites_shorthand or None,
                },
            }
        ]
