from pydantic import Field, ConfigDict
from typing import ClassVar, List, Union

from .ginas_common_sub_data import GinasCommonSubData
from .name_org import NameOrg

class Name(GinasCommonSubData):
    """Name model."""

    model_config = ConfigDict(extra='forbid')
    _NAME_TYPE_LABELS: ClassVar[dict[str, str]] = {
        'bn': 'Brand Name',
        'cd': 'Code',
        'cn': 'Common Name',
        'of': 'Official Name',
        'sci': 'Scientific Name',
        'sys': 'Systematic Name',
        'syn': 'Synonym',
    }

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

    @classmethod
    def _name_type_label(cls, value: str) -> str:
        cleaned = cls._clean_text(value)
        if not cleaned:
            return 'synonym'
        return cls._NAME_TYPE_LABELS.get(cleaned.lower(), '%s type name'%cleaned)

    def to_embedding_chunks(self) -> list[dict[str, object]]:
        raw_name = self._clean_text(self.name)
        name_type = self._clean_text(self.type)
        name_type_label = self._name_type_label(name_type)
        std_name = self._clean_text(self.stdName)
        if not raw_name:
            return []

        subject = self._embedding_root_name()
        domains = self._clean_list(self.domains)
        languages = self._clean_list(self.languages)
        name_jurisdiction = self._clean_list(self.nameJurisdiction)
        name_orgs = self._clean_list([item.nameOrg for item in (self.nameOrgs or []) if item.nameOrg])
        access = 'protected' if getattr(self, 'access', None) else 'public'
        parts = [f'{raw_name} is a {access} {name_type_label}']
        if self.displayName or self.preferred:
            parts.append('that is used as')
            if self.displayName and self.preferred:
                parts.append('both a display and preferred')
            elif self.displayName:
                parts.append('a display')
            else:
                parts.append('a preferred')
            parts.append('name')
        parts.append(f'for {subject}.')
        if name_orgs:
            parts.append(f'It is registered by {", ".join(name_orgs)} naming organizations as the official name.')
        if std_name and std_name != raw_name:
            parts.append(f'Standardized name {std_name}.')

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
                    'name_type_label': name_type_label or None,
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
