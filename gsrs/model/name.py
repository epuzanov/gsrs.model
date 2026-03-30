from pydantic import Field, ConfigDict
from typing import List, Union

from .ginas_common_sub_data import GinasCommonSubData
from .name_org import NameOrg

class Name(GinasCommonSubData):
    """Name model."""

    model_config = ConfigDict(extra='forbid')

    name: str = Field(
        default=...,
        alias='name',
        title='Name',
        description='Name',
    )
    type: str = Field(
        default=...,
        alias='type',
        title='Name Type',
        description='Name Type',
    )
    domains: Union[List[str], None] = Field(
        default=None,
        alias='domains',
        title='Domains',
        description='Domains',
    )
    stdName: Union[str, None] = Field(
        default=None,
        alias='stdName',
        title='Std Name',
        description='Std Name',
    )
    languages: List[str] = Field(
        default=...,
        alias='languages',
        title='Languages',
        description='Languages',
    )
    nameJurisdiction: Union[List[str], None] = Field(
        default=None,
        alias='nameJurisdiction',
        title='Naming Jurisdictions',
        description='Naming Jurisdictions',
    )
    nameOrgs: Union[List[NameOrg], None] = Field(
        default=None,
        alias='nameOrgs',
        title='Naming Organizations',
        description='Naming Organizations',
    )
    preferred: Union[bool, None] = Field(
        default=None,
        alias='preferred',
        title='Preferred Term',
        description='Preferred Term',
    )
    displayName: Union[bool, None] = Field(
        default=None,
        alias='displayName',
        title='Display Name',
        description='Display Name',
    )

    def to_embedding_chunks(self) -> list[dict[str, object]]:
        raw_name = self._clean_text(self.name)
        name_type = self._clean_text(self.type)
        std_name = self._clean_text(self.stdName)
        if not raw_name:
            return []

        subject = self._embedding_root_name()
        domains = self._clean_list(self.domains)
        languages = self._clean_list(self.languages)
        name_jurisdiction = self._clean_list(self.nameJurisdiction)
        name_orgs = self._clean_list([item.nameOrg for item in (self.nameOrgs or []) if item.nameOrg])
        parts = [f'{subject} name']
        if name_type:
            parts.append(f'type {name_type}')
        parts.append(f': {raw_name}.')
        if std_name and std_name != raw_name:
            parts.append(f'Standardized name {std_name}.')
        if self.preferred:
            parts.append('Preferred name.')
        if self.displayName:
            parts.append('Display name.')

        document_id = self._embedding_document_id()

        return [
            {
                'chunk_id': f'root_names_uuid:{self.uuid}',
                'document_id': document_id,
                'source_url': self._embedding_source_name(),
                'section': 'names',
                'text': ' '.join(parts),
                'metadata': {
                    **self._embedding_root_metadata(),
                    **self._hierarchy_metadata('root', 'names'),
                    'json_path': self._embedding_json_path('$.names[*]'),
                    'name_value': raw_name,
                    'name_type': name_type or None,
                    'std_name': std_name or None,
                    'preferred': bool(self.preferred),
                    'display_name': bool(self.displayName),
                    'domains': domains or None,
                    'languages': languages or None,
                    'name_jurisdiction': name_jurisdiction or None,
                    'name_orgs': name_orgs or None,
                    'references': self._embedding_references() or None,
                },
            }
        ]
