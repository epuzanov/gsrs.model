from pydantic import Field, ConfigDict
from typing import List, Union

from .ginas_common_sub_data import GinasCommonSubData
from .site import Site

class Glycosylation(GinasCommonSubData):
    """Glycosylation model."""

    model_config = ConfigDict(extra='forbid')

    CGlycosylationSites: Union[List[Site], None] = Field(
        default=None,
        alias='CGlycosylationSites',
        title='C-Glycosylation',
        description='C-Glycosylation',
    )

    NGlycosylationSites: Union[List[Site], None] = Field(
        default=None,
        alias='NGlycosylationSites',
        title='N-Glycosylation',
        description='N-Glycosylation',
    )

    OGlycosylationSites: Union[List[Site], None] = Field(
        default=None,
        alias='OGlycosylationSites',
        title='O-Glycosylation',
        description='O-Glycosylation',
    )

    glycosylationType: Union[str, None] = Field(
        default=None,
        alias='glycosylationType',
        title='Glycosylation Type',
        description='Glycosylation Type',
    )

    sitesShorthand: Union[str, None] = Field(
        default=None,
        alias='sitesShorthand',
        title='Sites Shorthand',
        description='Compact system-generated shorthand for the referenced sites.',
    )

    def to_embedding_chunks(self) -> list[dict[str, object]]:
        glyco_type = self._clean_text(self.glycosylationType)
        sitesShorthand = self._clean_text(getattr(self, 'sitesShorthand', None))

        has_content = glyco_type or self.CGlycosylationSites or self.NGlycosylationSites or self.OGlycosylationSites
        if not has_content:
            return []

        subject = self._embedding_root_name()
        document_id = self._embedding_document_id()
        access = 'protected' if getattr(self, 'access', None) else 'public'

        content_parts = [f"{subject} {access} glycosylation"]
        if glyco_type:
            content_parts.append(f"type {glyco_type}")
        site_info = []
        if self.CGlycosylationSites:
            site_info.append(f"C-glycosylation at {len(self.CGlycosylationSites)} sites")
        if self.NGlycosylationSites:
            site_info.append(f"N-glycosylation at {len(self.NGlycosylationSites)} sites")
        if self.OGlycosylationSites:
            site_info.append(f"O-glycosylation at {len(self.OGlycosylationSites)} sites")
        if sitesShorthand:
            site_info.append(f"sites shorthand: {sitesShorthand}")
        if site_info:
            content_parts.append(', '.join(site_info))

        return [
            {
                'chunk_id': f'root_glycosylation_uuid:{self.uuid}',
                'document_id': document_id,
                'source_url': self._embedding_source_name(),
                'section': 'glycosylation',
                'text': '. '.join(content_parts) + '.',
                'metadata': {
                    **self._chunk_metadata(),
                    **self._hierarchy_metadata('root', 'glycosylation'),
                    'glycosylation_type': glyco_type or None,
                    'sites_shorthand': sitesShorthand or None,
                    'c_sites_count': len(self.CGlycosylationSites) if self.CGlycosylationSites else None,
                    'n_sites_count': len(self.NGlycosylationSites) if self.NGlycosylationSites else None,
                    'o_sites_count': len(self.OGlycosylationSites) if self.OGlycosylationSites else None,
                },
            }
        ]
