from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import List, Union
from datetime import datetime, timezone
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
        default=None,
        alias='id',
        title='Id',
        description='Id',
        deprecated=True,
    )

    deprecated: Union[bool, None] = Field(
        default=None,
        alias='deprecated',
        title='Deprecated',
        description='Deprecated',
    )

    lastEdited: Union[datetime, None] = Field(
        default=None,
        alias='lastEdited',
        title='Last Modified Date',
        description='Last Modified Date',
    )

    created: Union[datetime, None] = Field(
        default=None,
        alias='created',
        title='Creation Date',
        description='Creation Date',
    )

    references: Union[List[UUID], None] = Field(
        default=None,
        alias='references',
        title='References',
        description='References',
    )

    molfile: Union[str, None] = Field(
        default=None,
        alias='molfile',
        title='Molfile',
        description='Molfile',
    )

    digest: Union[str, None] = Field(
        default=None,
        alias='digest',
        title='Digest',
        description='Digest',
    )

    smiles: Union[str, None] = Field(
        default=None,
        alias='smiles',
        title='Smiles',
        description='Smiles',
    )

    stereochemistry: str = Field(
        default=...,
        alias='stereochemistry',
        title='Stereochemical Type',
        description='Stereochemical Type',
    )

    opticalActivity: OpticalActivity = Field(
        default=...,
        alias='opticalActivity',
        title='Optical Activity',
        description='Optical Activity',
    )

    atropisomerism: Atropisomerism = Field(
        default=...,
        alias='atropisomerism',
        title='Additional Stereochemistry',
        description='Additional Stereochemistry',
    )

    stereoComments: Union[str, None] = Field(
        default=None,
        alias='stereoComments',
        title='Stereochemistry Details',
        description='Stereochemistry Details',
    )

    mwt: Union[float, None] = Field(
        default=None,
        alias='mwt',
        title='Molecular Weight',
        description='Molecular Weight',
    )

    count: Union[int, None] = Field(
        default=None,
        alias='count',
        title='Count',
        description='Count',
    )

    formula: Union[str, None] = Field(
        default=None,
        alias='formula',
        title='Chemical Formula',
        description='Chemical Formula',
    )

    charge: Union[int, None] = Field(
        default=None,
        alias='charge',
        title='Charge',
        description='Charge',
    )

    stereoCenters: Union[int, None] = Field(
        default=None,
        alias='stereoCenters',
        title='Total Stereocenter Count',
        description='Total Stereocenter Count',
    )

    definedStereo: Union[int, None] = Field(
        default=None,
        alias='definedStereo',
        title='Defined Stereocenter Count',
        description='Defined Stereocenter Count',
    )

    ezCenters: Union[int, None] = Field(
        default=None,
        alias='ezCenters',
        title='E/Z Center Count',
        description='E/Z Center Count',
    )

    hash: Union[str, None] = Field(
        default=None,
        alias='hash',
        title='Structure Hash',
        description='Structure Hash',
    )

    properties: Union[List[Value], None] = Field(
        default=None,
        alias='properties',
        title='Properties',
        description='Properties',
    )

    links: Union[List[XRef], None] = Field(
        default=None,
        alias='links',
        title='Links',
        description='Links',
    )

    inchiKey: Union[str, None] = Field(
        default=None,
        alias='_inchiKey',
        title='InChI Key',
        description='Standardized InChIKey generated for the structure.',
    )

    inchi: Union[str, None] = Field(
        default=None,
        alias='_inchi',
        title='InChI',
        description='Standardized InChI generated for the structure.',
    )

    @field_validator('created', 'lastEdited', mode='before')
    @classmethod
    def _parse_unix_timestamp(cls, value):
        if isinstance(value, (int, float)):
            timestamp = value / 1000 if value > 10_000_000_000 else value
            return datetime.fromtimestamp(timestamp, tz=timezone.utc)
        return value

    def model_dump(self, *args, **kwargs):
        kwargs.setdefault('exclude_none', True)
        kwargs.setdefault('by_alias', True)
        return super().model_dump(*args, **kwargs)

    def model_dump_json(self, *args, **kwargs):
        kwargs.setdefault('exclude_none', True)
        kwargs.setdefault('by_alias', True)
        return super().model_dump_json(*args, **kwargs)
