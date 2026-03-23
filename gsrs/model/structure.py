from pydantic import BaseModel, Field, ConfigDict
from typing import List, Union
from uuid import UUID
from enum import Enum

from .value import Value
from .xref import XRef

class OpticalActivity(Enum):
    """Enumeration of optical activity values."""

    PLUS = '( + )'
    MINUS = '( - )'
    PLUS_MINUS = '( + / - )'
    UNSPECIFIED = 'UNSPECIFIED'
    UNKNOWN = 'UNKNOWN'
    NONE = 'NONE'

class Atropisomerism(Enum):
    """Enumeration of atropisomerism values."""

    Yes = 'Yes'
    No = 'No'

class Structure(BaseModel):
    """Chemical Structure model."""

    model_config = ConfigDict(extra='forbid')

    id: Union[UUID, None] = Field(
        None,
        alias='id',
        title='Id',
        description='Id',
        element_property=True,
        deprecated=True,
    )

    deprecated: Union[bool, None] = Field(
        None,
        alias='deprecated',
        title='Deprecated',
        description='Deprecated',
        element_property=True,
    )

    lastEdited: Union[float, None] = Field(
        None,
        alias='lastEdited',
        title='Last Modified Date',
        description='Last Modified Date',
        element_property=True,
    )

    created: Union[float, None] = Field(
        None,
        alias='created',
        title='Creation Date',
        description='Creation Date',
        element_property=True,
    )

    references: Union[List[UUID], None] = Field(
        None,
        alias='references',
        title='References',
        description='References',
        element_property=True,
    )

    molfile: Union[str, None] = Field(
        None,
        alias='molfile',
        title='Molfile',
        description='Molfile',
        element_property=True,
    )

    digest: Union[str, None] = Field(
        None,
        alias='digest',
        title='Digest',
        description='Digest',
        element_property=True,
    )

    smiles: Union[str, None] = Field(
        None,
        alias='smiles',
        title='Smiles',
        description='Smiles',
        element_property=True,
    )

    stereochemistry: str = Field(
        ...,
        alias='stereochemistry',
        title='Stereochemical Type',
        description='Stereochemical Type',
        element_property=True,
    )

    opticalActivity: OpticalActivity = Field(
        ...,
        alias='opticalActivity',
        title='Optical Activity',
        description='Optical Activity',
        element_property=True,
    )

    atropisomerism: Atropisomerism = Field(
        ...,
        alias='atropisomerism',
        title='Additional Stereochemistry',
        description='Additional Stereochemistry',
        element_property=True,
    )

    stereoComments: Union[str, None] = Field(
        None,
        alias='stereoComments',
        title='Stereochemistry Details',
        description='Stereochemistry Details',
        element_property=True,
    )

    mwt: Union[float, None] = Field(
        None,
        alias='mwt',
        title='Molecular Weight',
        description='Molecular Weight',
        element_property=True,
    )

    count: Union[float, None] = Field(
        None,
        alias='count',
        title='Count',
        description='Count',
        element_property=True,
    )

    formula: Union[str, None] = Field(
        None,
        alias='formula',
        title='Chemical Formula',
        description='Chemical Formula',
        element_property=True,
    )

    charge: Union[float, None] = Field(
        None,
        alias='charge',
        title='Charge',
        description='Charge',
        element_property=True,
    )

    stereoCenters: Union[float, None] = Field(
        None,
        alias='stereoCenters',
        title='Total Stereocenter Count',
        description='Total Stereocenter Count',
        element_property=True,
    )

    definedStereo: Union[float, None] = Field(
        None,
        alias='definedStereo',
        title='Defined Stereocenter Count',
        description='Defined Stereocenter Count',
        element_property=True,
    )

    ezCenters: Union[float, None] = Field(
        None,
        alias='ezCenters',
        title='E/Z Center Count',
        description='E/Z Center Count',
        element_property=True,
    )

    hash: Union[str, None] = Field(
        None,
        alias='hash',
        title='Structure Hash',
        description='Structure Hash',
        element_property=True,
    )

    properties: Union[List[Value], None] = Field(
        None,
        alias='properties',
        title='Properties',
        description='Properties',
        element_property=True,
    )

    links: Union[List[XRef], None] = Field(
        None,
        alias='links',
        title='Links',
        description='Links',
        element_property=True,
    )

    inchiKey: Union[str, None] = Field(
        None,
        alias='_inchiKey',
        title='InChI Key',
        description='Standardized InChIKey generated for the structure.',
        element_property=True,
    )

    inchi: Union[str, None] = Field(
        None,
        alias='_inchi',
        title='InChI',
        description='Standardized InChI generated for the structure.',
        element_property=True,
    )


    def model_dump(self, *args, **kwargs):
        kwargs.setdefault('exclude_none', True)
        kwargs.setdefault('by_alias', True)
        return super().model_dump(*args, **kwargs)

    def model_dump_json(self, *args, **kwargs):
        kwargs.setdefault('exclude_none', True)
        kwargs.setdefault('by_alias', True)
        return super().model_dump_json(*args, **kwargs)
