from pydantic import Field, ConfigDict
from typing import List, Union

from .ginas_common_sub_data import GinasCommonSubData
from .name_org import NameOrg

class Name(GinasCommonSubData):
    """Name model."""

    model_config = ConfigDict(extra='forbid')

    name: str = Field(
        ...,
        alias='name',
        title='Name',
        description='Name',
        element_property=True,
    )

    type: str = Field(
        ...,
        alias='type',
        title='Name Type',
        description='Name Type',
        element_property=True,
    )

    domains: Union[List[str], None] = Field(
        None,
        alias='domains',
        title='Domains',
        description='Domains',
        element_property=True,
    )

    stdName: Union[str, None] = Field(
        None,
        alias='stdName',
        title='Std Name',
        description='Std Name',
        element_property=True,
    )

    languages: List[str] = Field(
        ...,
        alias='languages',
        title='Languages',
        description='Languages',
        element_property=True,
    )

    nameJurisdiction: Union[List[str], None] = Field(
        None,
        alias='nameJurisdiction',
        title='Naming Jurisdictions',
        description='Naming Jurisdictions',
        element_property=True,
    )

    nameOrgs: Union[List[NameOrg], None] = Field(
        None,
        alias='nameOrgs',
        title='Naming Organizations',
        description='Naming Organizations',
        element_property=True,
    )

    preferred: Union[bool, None] = Field(
        None,
        alias='preferred',
        title='Preferred Term',
        description='Preferred Term',
        element_property=True,
    )

    displayName: Union[bool, None] = Field(
        None,
        alias='displayName',
        title='Display Name',
        description='Display Name',
        element_property=True,
    )
