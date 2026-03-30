from pydantic import AnyUrl, BaseModel, ConfigDict, Field
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
            target_cls = cls._resolve_subclass_from_input(args, kwargs)  # type: ignore[attr-defined]
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
    )

    definitionType: Union[str, None] = Field(
        default=None,
        alias='definitionType',
        title='Definition Type',
        description='Definition Type',
    )

    definitionLevel: Union[str, None] = Field(
        default=None,
        alias='definitionLevel',
        title='Definition Level',
        description='Definition Level',
    )

    names: List[Name] = Field(
        default=...,
        alias='names',
        title='Names',
        description='Names',
        min_length=1,
    )

    codes: Union[List[Code], None] = Field(
        default=None,
        alias='codes',
        title='Codes',
        description='Codes',
    )

    modifications: Union[Modifications, None] = Field(
        default=None,
        alias='modifications',
        title='Modifications',
        description='Modifications',
    )

    notes: Union[List[Note], None] = Field(
        default=None,
        alias='notes',
        title='Notes',
        description='Notes',
    )

    properties: Union[List[Property], None] = Field(
        default=None,
        alias='properties',
        title='Properties',
        description='Properties',
    )

    relationships: Union[List[Relationship], None] = Field(
        default=None,
        alias='relationships',
        title='Relationships',
        description='Relationships',
    )

    references: List[Reference] = Field(
        default=...,
        alias='references',
        title='References',
        description='References',
        min_length=1,
    )

    approvalID: Union[str, None] = Field(
        default=None,
        alias='approvalID',
        title='Approval ID',
        description='Approval ID',
    )

    version: str = Field(
        default=...,
        alias='version',
        title='Substance Version',
        description='Substance Version',
    )

    tags: Union[List[str], None] = Field(
        default=None,
        alias='tags',
        title='Tags',
        description='Tags',
    )

    status: Union[str, None] = Field(
        default=None,
        alias='status',
        title='Status',
        description='Lifecycle status of the substance record in the catalogue or registry.',
    )

    approved: Union[float, None] = Field(
        default=None,
        alias='approved',
        title='Approval Date',
        description='Approval Date',
    )

    approvedBy: Union[str, None] = Field(
        default=None,
        alias='approvedBy',
        title='Approved By',
        description='Approved By',
    )

    schemaVersion: Union[str, None] = Field(
        default=None,
        alias='schemaVersion',
        title='Schema Version',
        description='Schema Version',
    )

    changeReason: Union[str, None] = Field(
        default=None,
        alias='changeReason',
        title='Change Reason',
        description='Reason for the change',
    )

    systemName: Union[str, None] = Field(
        default=None,
        alias='_name',
        title='System Name',
        description='System-generated preferred display name for the substance record.',
    )

    approvalIDDisplay: Union[str, None] = Field(
        default=None,
        alias='_approvalIDDisplay',
        title='Approval ID Display',
        description='System-generated approval identifier formatted for display.',
    )

    selfLink: Union[AnyUrl, None] = Field(
        default=None,
        alias='_self',
        title='Self Link',
        description='Canonical API URL for the full substance record.',
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

    def _stable_name(self) -> str:
        if self.systemName:
            return self._clean_text(self.systemName)
        for item in self.names:
            if item.displayName and item.name:
                return self._clean_text(item.name)
        for item in self.names:
            if item.preferred and item.name:
                return self._clean_text(item.name)
        for item in self.names:
            if item.name:
                return self._clean_text(item.name)
        return self._clean_text(self.approvalID or self.uuid or 'Unknown substance')

    def _class_summary_chunks(self) -> list[dict[str, object]]:
        return []

    def _substance_class_value(self) -> str:
        if isinstance(self.substanceClass, SubstanceClass):
            return self.substanceClass.value
        return self._clean_text(self.substanceClass) or 'unknown'

    def _reference_text_lookup(self) -> dict[str, str]:
        lookup: dict[str, str] = {}
        for reference in self.references or []:
            reference_text = reference.embedding_reference_text()
            if not reference_text:
                continue
            for reference_id in (self._clean_text(reference.uuid), self._clean_text(reference.id)):
                if reference_id and reference_id not in lookup:
                    lookup[reference_id] = reference_text
        return lookup

    def _embedding_references(self, reference_ids: Any = None) -> list[str]:
        return self._references_from_ids(reference_ids, self._reference_text_lookup())

    def to_embedding_chunks(self) -> list[dict[str, object]]:
        document_id = self._clean_text(self.uuid)
        name = self._stable_name()
        substance_class = self._substance_class_value()
        approval_id = self._clean_text(self.approvalID)
        approval_id_display = self._clean_text(self.approvalIDDisplay or self.approvalID)
        definition_type = self._clean_text(self.definitionType)
        definition_level = self._clean_text(self.definitionLevel)
        status = self._clean_text(self.status)
        approved_by = self._clean_text(self.approvedBy)
        tags = self._clean_list(self.tags)
        parts = [
            f'{name} is a GSRS substance record.',
            f'Substance class {substance_class}.',
        ]
        if approval_id_display:
            parts.append(f'Approval ID {approval_id_display}.')
        if status:
            parts.append(f'Status {status}.')
        if definition_type:
            parts.append(f'Definition type {definition_type}.')
        if definition_level:
            parts.append(f'Definition level {definition_level}.')
        if approved_by:
            parts.append(f'Approved by {approved_by}.')

        rows = [
            {
                'chunk_id': f'root_uuid:{self.uuid}',
                'document_id': document_id,
                'source_url': self._embedding_source_name(),
                'section': 'root',
                'text': ' '.join(parts),
                'metadata': {
                    **self._chunk_metadata(self),
                    **self._hierarchy_metadata('root'),
                    'json_path': '$',
                    'canonical_name': name,
                    'system_name': self._clean_text(self.systemName) or None,
                    'substance_class': substance_class,
                    'approval_id': approval_id or None,
                    'approval_id_display': approval_id_display or None,
                    'status': status or None,
                    'definition_type': definition_type or None,
                    'definition_level': definition_level or None,
                    'approved_by': approved_by or None,
                    'version': self._clean_text(self.version) or None,
                    'tags': tags or None,
                    'name_count': len(self.names or []),
                    'code_count': len(self.codes or []),
                    'property_count': len(self.properties or []),
                    'relationship_count': len(self.relationships or []),
                    'note_count': len(self.notes or []),
                    'reference_count': len(self.references or []),
                },
            }
        ]
        self._assign_parent(self, self)
        rows.extend(self._class_summary_chunks())

        seen_names = set()
        for item in self.names or []:
            key = (self._clean_text(item.name), self._clean_text(item.type))
            if key in seen_names:
                continue
            seen_names.add(key)
            rows.extend(item.to_embedding_chunks())

        seen_codes = set()
        for item in self.codes or []:
            key = (self._clean_text(item.codeSystem), self._clean_text(item.code))
            if key in seen_codes:
                continue
            seen_codes.add(key)
            rows.extend(item.to_embedding_chunks())

        for item in self.properties or []:
            rows.extend(item.to_embedding_chunks())
        for item in self.relationships or []:
            rows.extend(item.to_embedding_chunks())
        for item in self.notes or []:
            rows.extend(item.to_embedding_chunks())
        for item in self.references or []:
            rows.extend(item.to_embedding_chunks())

        if self.modifications is not None:
            rows.extend(self.modifications.to_embedding_chunks())

        return rows

    def model_post_init(self, __context: Any) -> None:
        super_post_init = getattr(super(), 'model_post_init', None)
        if callable(super_post_init):
            super_post_init(__context)
        self._assign_parent(self, self)

    @classmethod
    def _assign_parent(cls, value: Any, parent: 'Substance') -> None:
        if isinstance(value, GinasCommonSubData):
            value._set_parent(parent)
        if isinstance(value, BaseModel):
            for field_name in value.__class__.model_fields:
                cls._assign_parent(getattr(value, field_name), parent)
            return

        if isinstance(value, (list, tuple, set)):
            for item in value:
                cls._assign_parent(item, parent)
