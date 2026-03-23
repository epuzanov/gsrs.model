from pydantic import BaseModel, ConfigDict, Field
from pydantic._internal._model_construction import ModelMetaclass
from typing import Any, ClassVar, List, Union
from importlib import import_module
from enum import Enum

from .code import Code
from .ginas_common_data import GinasCommonData
from .ginas_common_sub_data import GinasCommonSubData
from .modifications import Modifications
from .name import Name
from .note import Note
from .property import Property
from .reference import Reference
from .relationship import Relationship



class SubstanceMetaclass(ModelMetaclass):
    """Metaclass that dispatches Substance construction to concrete subclasses."""

    def __call__(cls, *args, **kwargs):
        if cls.__name__ == 'Substance' and cls.__module__ == __name__:
            target_cls = cls._resolve_subclass_from_input(args, kwargs)
            if target_cls is not cls:
                return target_cls(*args, **kwargs)
        return super().__call__(*args, **kwargs)

class SubstanceClass(Enum):
    """Enumeration of GSRS substance classes."""

    chemical = 'chemical'
    protein = 'protein'
    nucleicAcid = 'nucleicAcid'
    mixture = 'mixture'
    polymer = 'polymer'
    structurallyDiverse = 'structurallyDiverse'
    specifiedSubstance = 'specifiedSubstance'
    specifiedSubstanceG1 = 'specifiedSubstanceG1'
    specifiedSubstanceG2 = 'specifiedSubstanceG2'
    specifiedSubstanceG3 = 'specifiedSubstanceG3'
    specifiedSubstanceG4 = 'specifiedSubstanceG4'
    concept = 'concept'

class Substance(GinasCommonData, metaclass=SubstanceMetaclass):
    """Detailed GSRS description of a substance beyond routine prescribing use."""

    model_config = ConfigDict(extra='forbid')

    substanceClass: SubstanceClass = Field(
        SubstanceClass.chemical,
        alias='substanceClass',
        title='Substance Type',
        description='High-level categorization of the substance, such as polymer, nucleic acid, protein, or chemical.',
        element_property=True,
    )

    definitionType: Union[str, None] = Field(
        None,
        alias='definitionType',
        title='Definition Type',
        description='Definition Type',
        element_property=True,
    )

    definitionLevel: Union[str, None] = Field(
        None,
        alias='definitionLevel',
        title='Definition Level',
        description='Definition Level',
        element_property=True,
    )

    names: List[Name] = Field(
        ...,
        alias='names',
        title='Names',
        description='Names',
        element_property=True,
        min_length=1,
    )

    codes: Union[List[Code], None] = Field(
        None,
        alias='codes',
        title='Codes',
        description='Codes',
        element_property=True,
    )

    modifications: Union[Modifications, None] = Field(
        None,
        alias='modifications',
        title='Modifications',
        description='Modifications',
        element_property=True,
    )

    notes: Union[List[Note], None] = Field(
        None,
        alias='notes',
        title='Notes',
        description='Notes',
        element_property=True,
    )

    properties: Union[List[Property], None] = Field(
        None,
        alias='properties',
        title='Properties',
        description='Properties',
        element_property=True,
    )

    relationships: Union[List[Relationship], None] = Field(
        None,
        alias='relationships',
        title='Relationships',
        description='Relationships',
        element_property=True,
    )

    references: List[Reference] = Field(
        ...,
        alias='references',
        title='References',
        description='References',
        element_property=True,
        min_length=1,
    )

    approvalID: Union[str, None] = Field(
        None,
        alias='approvalID',
        title='Approval ID',
        description='Approval ID',
        element_property=True,
    )

    version: str = Field(
        ...,
        alias='version',
        title='Substance Version',
        description='Substance Version',
        element_property=True,
    )

    tags: Union[List[str], None] = Field(
        None,
        alias='tags',
        title='Tags',
        description='Tags',
        element_property=True,
    )

    status: Union[str, None] = Field(
        None,
        alias='status',
        title='Status',
        description='Lifecycle status of the substance record in the catalogue or registry.',
        element_property=True,
    )

    approved: Union[float, None] = Field(
        None,
        alias='approved',
        title='Approval Date',
        description='Approval Date',
        element_property=True,
    )

    approvedBy: Union[str, None] = Field(
        None,
        alias='approvedBy',
        title='Approved By',
        description='Approved By',
        element_property=True,
    )

    schemaVersion: Union[str, None] = Field(
        None,
        alias='schemaVersion',
        title='Schema Version',
        description='Schema Version',
        element_property=True,
    )


    systemName: Union[str, None] = Field(
        None,
        alias='_name',
        title='System Name',
        description='System-generated preferred display name for the substance record.',
        element_property=True,
    )

    approvalIDDisplay: Union[str, None] = Field(
        None,
        alias='_approvalIDDisplay',
        title='Approval ID Display',
        description='System-generated approval identifier formatted for display.',
        element_property=True,
    )

    selfLink: Union[str, None] = Field(
        None,
        alias='_self',
        title='Self Link',
        description='Canonical API URL for the full substance record.',
        element_property=True,
    )


    _SUBSTANCE_CLASS_MODULES: ClassVar[dict[str, tuple[str, str]]] = {
        'chemical': ('.chemical_substance', 'ChemicalSubstance'),
        'protein': ('.protein_substance', 'ProteinSubstance'),
        'nucleicAcid': ('.nucleic_acid_substance', 'NucleicAcidSubstance'),
        'mixture': ('.mixture_substance', 'MixtureSubstance'),
        'polymer': ('.polymer_substance', 'PolymerSubstance'),
        'structurallyDiverse': ('.structurally_diverse_substance', 'StructurallyDiverseSubstance'),
        'specifiedSubstanceG1': ('.specified_substance_g1_substance', 'SpecifiedSubstanceG1Substance'),
        'concept': (__name__, 'Substance'),
        'specifiedSubstance': (__name__, 'Substance'),
        'specifiedSubstanceG2': (__name__, 'Substance'),
        'specifiedSubstanceG3': (__name__, 'Substance'),
        'specifiedSubstanceG4': (__name__, 'Substance'),
    }

    @classmethod
    def _extract_substance_class_value(cls, args, kwargs) -> Union[str, None]:
        payload = None
        if args and isinstance(args[0], dict):
            payload = args[0]
        elif kwargs:
            payload = kwargs
        if not isinstance(payload, dict):
            return None

        value = payload.get('substanceClass')
        if isinstance(value, SubstanceClass):
            return value.value
        return value

    @classmethod
    def _resolve_subclass_from_input(cls, args, kwargs):
        substance_class = cls._extract_substance_class_value(args, kwargs)
        if not substance_class:
            return cls

        module_path, class_name = cls._SUBSTANCE_CLASS_MODULES.get(substance_class, (__name__, 'Substance'))
        if module_path == __name__:
            return cls

        module = import_module(module_path, package=__package__)
        return getattr(module, class_name)

    @classmethod
    def model_validate(cls, obj: Any, *args, **kwargs):
        if cls is Substance and isinstance(obj, dict):
            target_cls = cls._resolve_subclass_from_input((obj,), {})
            if target_cls is not cls:
                return target_cls.model_validate(obj, *args, **kwargs)
        return super().model_validate(obj, *args, **kwargs)

    def model_post_init(self, __context: Any) -> None:
        super_post_init = getattr(super(), 'model_post_init', None)
        if callable(super_post_init):
            super_post_init(__context)
        self._assign_parent_uuid(self, self.uuid)

    @classmethod
    def _assign_parent_uuid(cls, value: Any, parent_uuid) -> None:
        if isinstance(value, GinasCommonSubData):
            value._set_parent_uuid(parent_uuid)

        if isinstance(value, BaseModel):
            for field_name in value.__class__.model_fields:
                cls._assign_parent_uuid(getattr(value, field_name), parent_uuid)
            return

        if isinstance(value, (list, tuple, set)):
            for item in value:
                cls._assign_parent_uuid(item, parent_uuid)
