from pydantic import Field, ConfigDict

from .site_container import SiteContainer


class Sugar(SiteContainer):
    """Sugar model for nucleotide sugar or sugar-like components."""

    model_config = ConfigDict(extra='forbid')

    sugar: str = Field(
        default=...,
        alias='sugar',
        title='Sugar',
        description='Name or identifier of the sugar or sugar-like component in the nucleotide.',
    )

    def to_embedding_chunks(self) -> list[dict[str, object]]:
        sugar_name = self._clean_text(self.sugar)
        sites_shorthand = self._clean_text(self.sitesShorthand)
        if not sugar_name:
            return []

        subject = self._embedding_root_name()
        document_id = self._embedding_document_id()
        access = 'protected' if getattr(self, 'access', None) else 'public'

        return [
            {
                'chunk_id': f'root_sugars_uuid:{self.uuid}',
                'document_id': document_id,
                'source_url': self._embedding_source_name(),
                'section': 'sugars',
                'text': f"{subject} {access} nucleic acid sugar {sugar_name} at {sites_shorthand or 'unspecified sites'}.".strip(),
                'metadata': {
                    **self._chunk_metadata(),
                    **self._hierarchy_metadata('root', 'sugars'),
                    'sugar_name': sugar_name or None,
                    'sites': sites_shorthand or None,
                },
            }
        ]
