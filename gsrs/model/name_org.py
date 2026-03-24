from pydantic import Field, ConfigDict
from typing import Union
from datetime import date

from .ginas_common_sub_data import GinasCommonSubData

class NameOrg(GinasCommonSubData):
    """Naming Org model."""

    model_config = ConfigDict(extra='forbid')

    nameOrg: str = Field(
        default=...,
        alias='nameOrg',
        title='Naming Organization',
        description='Naming Organization',
    )

    deprecatedDate: Union[date, None] = Field(
        default=None,
        alias='deprecatedDate',
        title='Deprecated Date',
        description='Deprecated Date',
    )

    def to_embedding_chunks(self) -> list[dict[str, object]]:
        org_name = self._clean_text(self.nameOrg)
        if not org_name:
            return []

        subject = self._embedding_root_name()
        document_id = self._embedding_document_id()

        content = f"{subject} naming organization: {org_name}."
        if self.deprecatedDate:
            content += f" Deprecated {self.deprecatedDate}."

        return [
            {
                'chunk_id': f'root_name_orgs_uuid:{self.uuid}',
                'document_id': document_id,
                'source_url': self._embedding_source_name(),
                'section': 'name_orgs',
                'text': content,
                'metadata': {
                    **self._embedding_root_metadata(),
                    **self._hierarchy_metadata('root', 'name_orgs'),
                    'organization': org_name or None,
                    'deprecated_date': str(self.deprecatedDate) if self.deprecatedDate else None,
                },
            }
        ]
