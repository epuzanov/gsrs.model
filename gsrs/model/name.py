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
        default_factory=list,
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
    def get_type_label(cls, value: str) -> str:
        if not value:
            return 'Synonym'
        return cls._NAME_TYPE_LABELS.get(value.lower(), '%s type name'%value)

