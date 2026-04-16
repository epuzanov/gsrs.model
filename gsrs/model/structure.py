from pydantic import BaseModel, ConfigDict, Field, field_serializer, field_validator
from typing import List, Union
from datetime import datetime, timezone
from uuid import UUID, uuid4
from enum import Enum


from ._serialization import dump_json, exclude_non_public_elements
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

    id: UUID = Field(
        default_factory=uuid4,
        alias='id',
        title='Id',
        description='Id',
        deprecated=True,
    )

    deprecated: bool = Field(
        default=False,
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

    references: List[Union[UUID, str]] = Field(
        default_factory=list,
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

    stereochemistry: Union[str, None] = Field(
        default=None,
        alias='stereochemistry',
        title='Stereochemical Type',
        description='Stereochemical Type',
    )

    opticalActivity: Union[OpticalActivity, None] = Field(
        default=None,
        alias='opticalActivity',
        title='Optical Activity',
        description='Optical Activity',
    )

    atropisomerism: Union[Atropisomerism, None] = Field(
        default=None,
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

    def is_deprecated(self) -> bool:
        """Determine if the record is deprecated."""
        return self.deprecated is True

    def model_dump(self, *args, exclude_non_public: bool = False, **kwargs):
        kwargs.setdefault('exclude_none', True)
        kwargs.setdefault('by_alias', True)
        if exclude_non_public:
            exclude_none = kwargs.get('exclude_none', False)
            filtered_kwargs = dict(kwargs)
            filtered_kwargs['exclude_none'] = False
            data = super().model_dump(*args, **filtered_kwargs)
            return exclude_non_public_elements(data, exclude_none=exclude_none)
        return super().model_dump(*args, **kwargs)

    def model_dump_json(self, *args, exclude_non_public: bool = False, **kwargs):
        kwargs.setdefault('exclude_none', True)
        kwargs.setdefault('by_alias', True)
        if exclude_non_public:
            indent = kwargs.pop('indent', None)
            ensure_ascii = kwargs.pop('ensure_ascii', False)
            data = self.model_dump(*args, mode='json', exclude_non_public=True, **kwargs)
            return dump_json(data, indent=indent, ensure_ascii=ensure_ascii)
        return super().model_dump_json(*args, **kwargs)

    @field_serializer('references', when_used='always')
    def _serialize_references(self, value: List[Union[UUID, str]]):
        new_values = []
        for item in value:
            if isinstance(item, UUID):
                new_values.append(str(item))
            elif isinstance(item, str):
                new_values.append(item)
        return new_values
