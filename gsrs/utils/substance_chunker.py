"""Substance chunking utilities for embedding generation."""

from __future__ import annotations

import json
import re
from datetime import datetime
from enum import Enum
from typing import Any, List, Union

from pydantic import BaseModel


class SubstanceChunker:
    """Class for generating embedding chunks from a Substance instance.
    
    This class accepts a Substance instance as input and provides methods
    to generate embedding chunks for all nested model objects.
    """

    def __init__(self, substance: Any):
        """Initialize the chunker with a Substance instance.
        
        Args:
            substance: The Substance instance to generate chunks from.
        """
        self.substance = substance
        self._json_paths: dict[int, str] = {}
        self._assign_parent_references()

    def _assign_parent_references(self) -> None:
        """Recursively assign parent reference to all child objects."""
        from gsrs.model.ginas_common_sub_data import GinasCommonSubData
        
        def _assign(value: Any, parent: Any, json_path: str = '$') -> None:
            if isinstance(value, GinasCommonSubData):
                value._set_parent(parent)
                self._json_paths[id(value)] = json_path
            if isinstance(value, BaseModel):
                self._json_paths[id(value)] = json_path
                for field_name in value.__class__.model_fields:
                    child_path = f'{json_path}.{field_name}'
                    _assign(value.__dict__.get(field_name), parent, child_path)
                return

            if isinstance(value, (list, tuple, set)):
                for index, item in enumerate(value):
                    _assign(item, parent, f'{json_path}[{index}]')
        
        _assign(self.substance, self.substance)

    @staticmethod
    def _safe_get(obj: Any, attr: str, default: Any = None) -> Any:
        """Safely get an attribute from an object."""
        return getattr(obj, attr, default)

    @staticmethod
    def _clean_text(value: Any) -> str:
        """Clean and normalize text value for embedding."""
        if value is None:
            return ''
        if isinstance(value, BaseModel):
            value = value.model_dump(by_alias=True, exclude_none=True)
        if isinstance(value, (dict, list)):
            value = json.dumps(value, ensure_ascii=False, sort_keys=True)
        if isinstance(value, datetime):
            value = value.isoformat()
        text = str(value).replace('\r', ' ').replace('\n', ' ')
        return re.sub(r'\s+', ' ', text).strip()

    @classmethod
    def _clean_list(cls, values: Any) -> list[str]:
        """Clean and deduplicate list of values."""
        if values is None:
            return []
        if isinstance(values, (str, BaseModel)) or not isinstance(values, (list, tuple, set)):
            values = [values]

        cleaned_values: list[str] = []
        for value in values:
            cleaned = cls._clean_text(value)
            if cleaned and cleaned not in cleaned_values:
                cleaned_values.append(cleaned)
        return cleaned_values

    def _references_from_ids(
        self,
        reference_ids: Any,
        reference_text_by_id: dict[str, str] | None,
    ) -> list[str]:
        """Build reference texts from reference IDs."""
        if not reference_text_by_id:
            return []

        references: list[str] = []
        for reference_id in self._clean_list(reference_ids):
            reference_text = self._clean_text(reference_text_by_id.get(reference_id))
            if reference_text and reference_text not in references:
                references.append(reference_text)
        return references

    @classmethod
    def _hierarchy_metadata(cls, *parts: Any) -> dict[str, Any]:
        """Generate hierarchy metadata for embedding chunk."""
        hierarchy = [cls._clean_text(part) for part in parts if cls._clean_text(part)]
        return {
            'hierarchy': hierarchy,
            'hierarchy_path': ' > '.join(hierarchy),
            'hierarchy_level': len(hierarchy),
        }

    def _chunk_metadata(self, obj: Any) -> dict[str, Any]:
        """Generate common chunk metadata."""
        return {
            'access': 'protected' if self._safe_get(obj, 'access') else 'public',
            'created': self._clean_text(self._safe_get(obj, 'created')) or None,
            'lastEdited': self._clean_text(self._safe_get(obj, 'lastEdited')) or None,
        }

    def _embedding_source_name(self, obj: Any) -> str | None:
        """Get the source URL for embedding."""
        self_link = self._clean_text(self._safe_get(obj, 'selfLink'))
        if self_link:
            return self_link
        parent = self._safe_get(obj, '_parent')
        if parent is not None:
            return self._embedding_source_name(parent)
        return None

    def _embedding_document_id(self, obj: Any) -> str:
        """Get the document ID for embedding."""
        parent = obj._parent if hasattr(obj, '_parent') else None
        if parent:
            return self._clean_text(parent.uuid)
        return self._clean_text(obj.uuid)

    def _embedding_root_name(self, obj: Any) -> str:
        """Get the root substance name for embedding context."""
        parent = obj._parent if hasattr(obj, '_parent') else None
        if parent is not None:
            document_id = self._clean_text(parent.uuid)
            root_name = self._clean_text(self._stable_name())
            if root_name:
                return f'Substance {document_id}' if document_id and root_name == document_id else root_name
        root_name = self._clean_text(obj.name) if hasattr(obj, 'name') and obj.name else ''
        if root_name:
            return root_name
        document_id = self._embedding_document_id(obj)
        return f'Substance {document_id}' if document_id else 'Substance'

    def _embedding_json_path(self, obj: Any, fallback: str) -> str:
        """Get the JSON path for embedding."""
        return self._json_paths.get(id(obj), fallback)

    def _embedding_references(self, obj: Any, reference_ids: Any = None) -> list[str]:
        """Get reference texts for embedding."""
        parent = obj._parent if hasattr(obj, '_parent') else None
        if parent is None:
            return []
        refs = reference_ids if reference_ids is not None else obj.references
        return self._references_from_ids(refs, self._reference_text_lookup())

    def _reference_text_lookup(self) -> dict[str, str]:
        """Build lookup dictionary of reference texts by ID."""
        lookup: dict[str, str] = {}
        for reference in self.substance.references or []:
            reference_text = self._embedding_reference_text(reference)
            if not reference_text:
                continue
            for reference_id in (self._clean_text(reference.uuid), self._clean_text(reference.id)):
                if reference_id and reference_id not in lookup:
                    lookup[reference_id] = reference_text
        return lookup

    def _embedding_reference_text(self, reference: Any) -> str:
        """Get reference text from a Reference object."""
        doc_type = self._clean_text(reference.docType) if reference.docType else ''
        citation = self._clean_text(reference.citation) if reference.citation else ''
        if doc_type and citation:
            return f'{doc_type}: {citation}'
        return doc_type or citation

    def _get_refPname(self, ref: Any) -> str:
        """Get the referenced substance name from a SubstanceReference object."""
        if ref is None:
            return ''
        for attr in ('refPname', 'name', 'approvalID', 'refuuid', 'linkingID'):
            val = getattr(ref, attr, None)
            if val:
                return self._clean_text(val)
        return ''

    def _get_refuuid(self, ref: Any) -> str:
        """Get the referenced substance ID from a SubstanceReference object."""
        if ref is None:
            return ''
        for attr in ('approvalID', 'refuuid', 'linkingID', 'uuid'):
            val = getattr(ref, attr, None)
            if val:
                return self._clean_text(val)
        return ''

    @staticmethod
    def _oxford_join(values: list[str]) -> str:
        """Join list values with Oxford comma."""
        cleaned = [value for value in values if value]
        if not cleaned:
            return ''
        if len(cleaned) == 1:
            return cleaned[0]
        if len(cleaned) == 2:
            return f'{cleaned[0]} and {cleaned[1]}'
        return f"{', '.join(cleaned[:-1])}, and {cleaned[-1]}"

    def _stable_name(self) -> str:
        """Get stable name for substance."""
        if self.substance.systemName:
            return self._clean_text(self.substance.systemName)
        for item in self.substance.names or []:
            if item.displayName and item.name:
                return self._clean_text(item.name)
        for item in self.substance.names or []:
            if item.preferred and item.name:
                return self._clean_text(item.name)
        for item in self.substance.names or []:
            if item.name:
                return self._clean_text(item.name)
        approval_id = self.substance.approvalID if hasattr(self.substance, 'approvalID') else None
        uuid = self.substance.uuid
        return self._clean_text(approval_id or uuid or 'Unknown substance')

    def _summary_definitional_sentence(self) -> str:
        """Generate definitional sentence for substance summary based on substance class."""
        substance_class = self.substance.substanceClass
        if isinstance(substance_class, Enum):
            substance_class = substance_class.value
        
        if substance_class == 'chemical':
            return self._chemical_summary_definitional_sentence()
        elif substance_class == 'mixture':
            return self._mixture_summary_definitional_sentence()
        elif substance_class == 'protein':
            return self._protein_summary_definitional_sentence()
        elif substance_class == 'nucleicAcid':
            return self._nucleic_acid_summary_definitional_sentence()
        elif substance_class == 'polymer':
            return self._polymer_summary_definitional_sentence()
        elif substance_class == 'structurallyDiverse':
            return self._structurally_diverse_summary_definitional_sentence()
        elif substance_class == 'specifiedSubstanceG1':
            return self._specified_substance_g1_summary_definitional_sentence()
        
        return ''

    def _substance_class_metadata(self) -> dict[str, object]:
        """Get substance class specific metadata based on substance class."""
        substance_class = self.substance.substanceClass
        if isinstance(substance_class, Enum):
            substance_class = substance_class.value
        
        if substance_class == 'chemical':
            return self._chemical_substance_class_metadata()
        elif substance_class == 'mixture':
            return self._mixture_substance_class_metadata()
        elif substance_class == 'protein':
            return self._protein_substance_class_metadata()
        elif substance_class == 'nucleicAcid':
            return self._nucleic_acid_substance_class_metadata()
        elif substance_class == 'polymer':
            return self._polymer_substance_class_metadata()
        elif substance_class == 'structurallyDiverse':
            return self._structurally_diverse_substance_class_metadata()
        elif substance_class == 'specifiedSubstanceG1':
            return self._specified_substance_g1_substance_class_metadata()
        
        return {}

    # =========================================================================
    # ChemicalSubstance methods
    # =========================================================================

    def _chemical_summary_definitional_sentence(self) -> str:
        """Generate definitional sentence for ChemicalSubstance."""
        structure = self.substance.structure
        if structure is None:
            return ''

        formula = self._clean_text(structure.formula) if structure.formula else ''
        molecular_weight = structure.mwt
        stereochemistry = self._clean_text(structure.stereochemistry).lower() if structure.stereochemistry else ''
        smiles = self._clean_text(structure.smiles) if structure.smiles else ''
        inchi_key = self._clean_text(structure.inchiKey) if structure.inchiKey else ''
        moieties = self._clean_list([m.formula for m in self.substance.moieties or [] if m.formula])
        access = 'protected' if self.substance.access else 'public'

        descriptors: list[str] = [f'Structure is a {access} chemical structure']
        if formula:
            descriptors.append(f'molecular formula {formula}')
        if molecular_weight is not None:
            descriptors.append(f'molecular weight {molecular_weight}')
        if stereochemistry:
            descriptors.append('racemic' if stereochemistry == 'racemic' else stereochemistry)
        if smiles and inchi_key:
            descriptors.append(f'with SMILES {smiles} and InChIKey {inchi_key}')
        elif smiles:
            descriptors.append(f'with SMILES {smiles}')
        elif inchi_key:
            descriptors.append(f'with InChIKey {inchi_key}')
        if moieties:
            descriptors.append(f'and moieties {", ".join(moieties)}')
        if not descriptors:
            return ''
        return f"{', '.join(descriptors)}."

    def _chemical_substance_class_metadata(self) -> dict[str, object]:
        """Get ChemicalSubstance specific metadata."""
        structure = self.substance.structure
        if not structure:
            return {}
        return {
            'formula': self._clean_text(structure.formula) or None,
            'molecular_weight': structure.mwt,
            'smiles': self._clean_text(structure.smiles) or None,
            'inchi_key': self._clean_text(structure.inchiKey) or None,
            'inchi': self._clean_text(structure.inchi) or None,
            'structure_digest': self._clean_text(structure.digest) or None,
            'structure_hash': self._clean_text(structure.hash) or None,
            'stereochemistry': self._clean_text(structure.stereochemistry) or None,
            'optical_activity': structure.opticalActivity.value if structure.opticalActivity else None,
            'atropisomerism': structure.atropisomerism.value if structure.atropisomerism else None,
            'stereo_centers': structure.stereoCenters,
            'defined_stereo': structure.definedStereo,
            'ez_centers': structure.ezCenters,
            'charge': structure.charge,
            'structure_references': self._clean_list(structure.references) or None,
            'has_molfile': bool(structure.molfile),
            'moieties': self._clean_list([m.formula for m in self.substance.moieties or [] if m.formula]) or [],
        }

    # =========================================================================
    # MixtureSubstance methods
    # =========================================================================

    def _mixture_summary_definitional_sentence(self) -> str:
        """Generate definitional sentence for MixtureSubstance."""
        mixture = self.substance.mixture
        if mixture is None:
            return ''

        details: list[str] = []
        component_count = len(mixture.components or [])
        if component_count:
            label = 'component' if component_count == 1 else 'components'
            details.append(f'Mixture with {component_count} {label}')

        parent_substance = mixture.parentSubstance
        if parent_substance:
            parent_name = self._get_refPname(parent_substance)
            if parent_name:
                details.append(f'parent substance {parent_name}')
        if not details:
            return ''
        return f"{', '.join(details)}."

    def _mixture_substance_class_metadata(self) -> dict[str, object]:
        """Get MixtureSubstance specific metadata."""
        mixture = self.substance.mixture
        if not mixture:
            return {}
        parent = mixture.parentSubstance
        return {
            'mixture_component_count': len(mixture.components or []),
            'mixture_parent_substance': self._get_refPname(parent) if parent else None,
            'mixture_parent_substance_id': self._get_refuuid(parent) if parent else None,
        }

    # =========================================================================
    # ProteinSubstance methods
    # =========================================================================

    def _protein_summary_definitional_sentence(self) -> str:
        """Generate definitional sentence for ProteinSubstance."""
        protein = self.substance.protein
        if protein is None:
            return ''

        parts: list[str] = []
        protein_type = self._clean_text(protein.proteinType) if protein.proteinType else ''
        if protein_type:
            parts.append(f'Protein type {protein_type}')

        protein_subtypes = self._clean_list(protein.proteinSubType) if protein.proteinSubType else []
        if protein_subtypes:
            parts.append(f'subtypes {self._oxford_join(protein_subtypes)}')

        subunit_count = len(protein.subunits or [])
        if subunit_count:
            label = 'subunit' if subunit_count == 1 else 'subunits'
            parts.append(f'{subunit_count} {label}')

        sequence_origin = self._clean_text(protein.sequenceOrigin) if protein.sequenceOrigin else ''
        if sequence_origin:
            parts.append(f'sequence origin {sequence_origin}')

        sequence_type = self._clean_text(protein.sequenceType) if protein.sequenceType else ''
        if sequence_type:
            parts.append(f'sequence type {sequence_type}')

        glycosylation = protein.glycosylation
        glycosylation_type = self._clean_text(glycosylation.glycosylationType) if glycosylation and glycosylation.glycosylationType else ''
        if glycosylation_type:
            parts.append(f'glycosylation type {glycosylation_type}')
        if not parts:
            return ''
        return f"{', '.join(parts)}."

    def _protein_substance_class_metadata(self) -> dict[str, object]:
        """Get ProteinSubstance specific metadata."""
        protein = self.substance.protein
        if not protein:
            return {}
        glycosylation = protein.glycosylation
        return {
            'protein_subunit_count': len(protein.subunits or []),
            'protein_disulfide_link_count': len(protein.disulfideLinks or []),
            'protein_other_link_count': len(protein.otherLinks or []),
            'protein_type': self._clean_text(protein.proteinType) or None,
            'protein_subtypes': self._clean_list(protein.proteinSubType) or None,
            'protein_sequence_origin': self._clean_text(protein.sequenceOrigin) or None,
            'protein_sequence_type': self._clean_text(protein.sequenceType) or None,
            'glycosylation_type': self._clean_text(glycosylation.glycosylationType) if glycosylation else None,
            'c_sites_count': len(glycosylation.CGlycosylationSites or []) if glycosylation else 0,
            'n_sites_count': len(glycosylation.NGlycosylationSites or []) if glycosylation else 0,
            'o_sites_count': len(glycosylation.OGlycosylationSites or []) if glycosylation else 0,
            'has_protein_modifications': bool(protein.modifications),
        }

    # =========================================================================
    # NucleicAcidSubstance methods
    # =========================================================================

    def _nucleic_acid_summary_definitional_sentence(self) -> str:
        """Generate definitional sentence for NucleicAcidSubstance."""
        nucleic_acid = self.substance.nucleicAcid
        if nucleic_acid is None:
            return ''

        parts: list[str] = []
        nucleic_acid_type = self._clean_text(nucleic_acid.nucleicAcidType) if nucleic_acid.nucleicAcidType else ''
        if nucleic_acid_type:
            parts.append(f'Nucleic acid type {nucleic_acid_type}')

        subtypes = self._clean_list(nucleic_acid.nucleicAcidSubType) if nucleic_acid.nucleicAcidSubType else []
        if subtypes:
            parts.append(f'subtypes {self._oxford_join(subtypes)}')

        subunit_count = len(nucleic_acid.subunits or [])
        if subunit_count:
            label = 'subunit' if subunit_count == 1 else 'subunits'
            parts.append(f'{subunit_count} {label}')

        sequence_origin = self._clean_text(nucleic_acid.sequenceOrigin) if nucleic_acid.sequenceOrigin else ''
        if sequence_origin:
            parts.append(f'sequence origin {sequence_origin}')

        sequence_type = self._clean_text(nucleic_acid.sequenceType) if nucleic_acid.sequenceType else ''
        if sequence_type:
            parts.append(f'sequence type {sequence_type}')
        if not parts:
            return ''
        return f"{', '.join(parts)}."

    def _nucleic_acid_substance_class_metadata(self) -> dict[str, object]:
        """Get NucleicAcidSubstance specific metadata."""
        nucleic_acid = self.substance.nucleicAcid
        if not nucleic_acid:
            return {}
        return {
            'na_subunit_count': len(nucleic_acid.subunits or []),
            'na_linkage_count': len(nucleic_acid.linkages or []),
            'na_sugar_count': len(nucleic_acid.sugars or []),
            'nucleic_acid_type': self._clean_text(nucleic_acid.nucleicAcidType) or None,
            'nucleic_acid_subtypes': self._clean_list(nucleic_acid.nucleicAcidSubType) or None,
            'nucleic_acid_sequence_origin': self._clean_text(nucleic_acid.sequenceOrigin) or None,
            'nucleic_acid_sequence_type': self._clean_text(nucleic_acid.sequenceType) or None,
            'has_nucleic_acid_modifications': bool(nucleic_acid.modifications),
        }

    # =========================================================================
    # PolymerSubstance methods
    # =========================================================================

    def _polymer_summary_definitional_sentence(self) -> str:
        """Generate definitional sentence for PolymerSubstance."""
        polymer = self.substance.polymer
        if polymer is None:
            return ''

        classification = polymer.classification
        parts: list[str] = []

        polymer_class = self._clean_text(classification.polymerClass) if classification and classification.polymerClass else ''
        if polymer_class:
            parts.append(f'Polymer class {polymer_class}')

        monomer_count = len(polymer.monomers or [])
        if monomer_count:
            label = 'monomer' if monomer_count == 1 else 'monomers'
            parts.append(f'{monomer_count} {label}')

        structural_unit_count = len(polymer.structuralUnits or [])
        if structural_unit_count:
            label = 'structural unit' if structural_unit_count == 1 else 'structural units'
            parts.append(f'{structural_unit_count} {label}')

        polymer_geometry = self._clean_text(classification.polymerGeometry) if classification and classification.polymerGeometry else ''
        if polymer_geometry:
            parts.append(f'geometry {polymer_geometry}')
        if not parts:
            return ''
        return f"{', '.join(parts)}."

    def _polymer_substance_class_metadata(self) -> dict[str, object]:
        """Get PolymerSubstance specific metadata."""
        polymer = self.substance.polymer
        if not polymer:
            return {}
        classification = polymer.classification
        parent = classification.parentSubstance if classification else None
        return {
            'polymer_monomer_count': len(polymer.monomers or []),
            'polymer_structural_unit_count': len(polymer.structuralUnits or []),
            'polymer_class': self._clean_text(classification.polymerClass) if classification else None,
            'polymer_geometry': self._clean_text(classification.polymerGeometry) if classification else None,
            'polymer_subclass': self._clean_list(classification.polymerSubclass) if classification else None,
            'polymer_source_type': self._clean_text(classification.sourceType) if classification else None,
            'polymer_parent_substance': self._get_refPname(parent) if parent else None,
            'polymer_parent_substance_id': self._get_refuuid(parent) if parent else None,
            'has_display_structure': bool(polymer.displayStructure),
            'has_idealized_structure': bool(polymer.idealizedStructure),
        }

    # =========================================================================
    # StructurallyDiverseSubstance methods
    # =========================================================================

    def _structurally_diverse_summary_definitional_sentence(self) -> str:
        """Generate definitional sentence for StructurallyDiverseSubstance."""
        details = self.substance.structurallyDiverse
        if details is None:
            return ''

        parts: list[str] = []
        species = self._clean_text(details.organismSpecies) if details.organismSpecies else ''
        if species:
            parts.append(f'organism species {species}')

        source_material_class = self._clean_text(details.sourceMaterialClass) if details.sourceMaterialClass else ''
        if source_material_class:
            parts.append(f'source material class {source_material_class}')

        source_material_type = self._clean_text(details.sourceMaterialType) if details.sourceMaterialType else ''
        if source_material_type:
            parts.append(f'source material type {source_material_type}')

        organism_parts = self._clean_list(details.part) if details.part else []
        if organism_parts:
            parts.append(f'parts {self._oxford_join(organism_parts)}')
        if not parts:
            return ''
        return f"Structurally diverse material with {', '.join(parts)}."

    def _structurally_diverse_substance_class_metadata(self) -> dict[str, object]:
        """Get StructurallyDiverseSubstance specific metadata."""
        details = self.substance.structurallyDiverse
        if not details:
            return {}

        paternal = details.hybridSpeciesPaternalOrganism
        maternal = details.hybridSpeciesMaternalOrganism
        parent = details.parentSubstance
        return {
            'source_material_class': self._clean_text(details.sourceMaterialClass) or None,
            'source_material_state': self._clean_text(details.sourceMaterialState) or None,
            'source_material_type': self._clean_text(details.sourceMaterialType) or None,
            'developmental_stage': self._clean_text(details.developmentalStage) or None,
            'fraction_name': self._clean_text(details.fractionName) or None,
            'fraction_material_type': self._clean_text(details.fractionMaterialType) or None,
            'organism_family': self._clean_text(details.organismFamily) or None,
            'organism_genus': self._clean_text(details.organismGenus) or None,
            'organism_species': self._clean_text(details.organismSpecies) or None,
            'organism_author': self._clean_text(details.organismAuthor) or None,
            'part': self._clean_list(details.part) or None,
            'part_location': self._clean_text(details.partLocation) or None,
            'infra_specific_type': self._clean_text(details.infraSpecificType) or None,
            'infra_specific_name': self._clean_text(details.infraSpecificName) or None,
            'hybrid_species_paternal_organism': self._get_refPname(paternal) if paternal else None,
            'hybrid_species_paternal_organism_id': self._get_refuuid(paternal) if paternal else None,
            'hybrid_species_maternal_organism': self._get_refPname(maternal) if maternal else None,
            'hybrid_species_maternal_organism_id': self._get_refuuid(maternal) if maternal else None,
            'parent_substance': self._get_refPname(parent) if parent else None,
            'parent_substance_id': self._get_refuuid(parent) if parent else None,
        }

    # =========================================================================
    # SpecifiedSubstanceG1Substance methods
    # =========================================================================

    def _specified_substance_g1_summary_definitional_sentence(self) -> str:
        """Generate definitional sentence for SpecifiedSubstanceG1Substance."""
        specified_substance = self.substance.specifiedSubstance
        if specified_substance is None:
            return ''
        constituent_count = len(specified_substance.constituents or [])
        if not constituent_count:
            return ''
        label = 'constituent' if constituent_count == 1 else 'constituents'
        return f'Specified substance with {constituent_count} {label}.'

    def _specified_substance_g1_substance_class_metadata(self) -> dict[str, object]:
        """Get SpecifiedSubstanceG1Substance specific metadata."""
        specified_substance = self.substance.specifiedSubstance
        if not specified_substance:
            return {}
        return {
            'specified_substance_constituent_count': len(specified_substance.constituents or []),
        }

    def _substance_class_value(self) -> str:
        """Get substance class value as string."""
        substance_class = self.substance.substanceClass
        if isinstance(substance_class, Enum):
            return substance_class.value
        return self._clean_text(substance_class) or 'unknown'

    def _summary_title_name(self) -> str:
        """Generate formatted title name for summary."""
        name = self._clean_text(self._stable_name())
        letters = ''.join(character for character in name if character.isalpha())
        if letters and letters == letters.upper():
            return name.title()
        return name

    def _summary_name_with_languages(self, item: Any) -> str:
        """Format name with languages for summary."""
        name = item.name.strip() if item.name else ''
        languages = [language.strip() for language in (item.languages or []) if str(language).strip()]
        if not languages:
            return name
        return f"{name} [{'|'.join(languages)}]"

    def _summary_names_sentence(self) -> str:
        """Generate names summary sentence."""
        unique_names: list[str] = []
        display_name = ''
        preferred_names = []
        official_names = {}
        for item in self.substance.names or []:
            name = self._clean_text(item.name)
            if not name or name in unique_names:
                continue
            unique_names.append(name)
            formatted_name = self._summary_name_with_languages(item)
            if item.displayName and not display_name:
                display_name = formatted_name
            if item.preferred:
                preferred_names.append(formatted_name)
            if self._clean_text(item.type) == 'of' and item.nameOrgs:
                official_names[formatted_name] = ', '.join([no.nameOrg for no in item.nameOrgs])

        details: list[str] = []
        if display_name:
            details.append(f'{display_name} as the display name{" and as the preferred name as well" if display_name in preferred_names else ""}')
            if display_name in official_names:
                details[-1] = details[-1] + f' and is registered by {official_names[display_name]} naming organizations as the official name'
        for preferred_name in preferred_names:
            if preferred_name != display_name:
                details.append(f'{preferred_name} as the preferred name')
            if preferred_name in official_names:
                details[-1] = details[-1] + f' and is registered by {official_names[preferred_name]} naming organizations as the official name'
        for official_name, name_orgs in official_names.items():
            if official_name != display_name and official_name not in preferred_names:
                role = 'as the official name' if official_name != display_name else 'as the official name as well'
                details.append(f'{official_name} is registered by {name_orgs} naming organizations as the official name')
        if not details:
            return ''
        return f'The record includes official and alternative names, including {self._oxford_join(details)}.'

    def _summary_primary_identifiers_sentence(self) -> str:
        """Generate primary identifiers summary sentence."""
        preferred_order = [
            'FDA UNII',
            'SMS_ID',
            'SMSID',
            'ASK',
            'ASKP',
            'SVGID',
            'EVMPD',
            'xEVMPD',
            'CAS',
            'DRUG BANK',
            'RXCUI',
            'CHEMBL',
            'PUBCHEM',
        ]
        primary_identifiers: list[tuple[tuple[int, int], str]] = []
        seen: set[tuple[str, str]] = set()
        for index, item in enumerate(self.substance.codes or []):
            if self._clean_text(item.type) != 'PRIMARY' or item.isClassification:
                continue
            system = self._clean_text(item.codeSystem)
            code = self._clean_text(item.code)
            if not system or not code:
                continue
            key = (system.upper(), code)
            if key in seen:
                continue
            seen.add(key)
            try:
                order = preferred_order.index(system.upper())
            except ValueError:
                order = len(preferred_order) + index
            primary_identifiers.append(((order, index), f"{system}: {code}"))

        if not primary_identifiers:
            return ''
        labels = [label for _, label in sorted(primary_identifiers)[:8]]
        return f'It also includes primary identifiers such as {self._oxford_join(labels)}.'

    def _summary_classifications_sentence(self) -> str:
        """Generate classifications summary sentence."""
        preferred_order = [
            'WHO-ATC',
            'WHO-VATC',
            'NCI_THESAURUS',
            'EMA ASSESSMENT REPORTS',
            'WHO-ESSENTIAL MEDICINES LIST',
            'NDF-RT',
            'LIVERTOX',
            'FDA ORPHAN DRUG',
            'EU-ORPHAN DRUG',
        ]
        classifications: list[tuple[tuple[int, int], str]] = []
        seen: set[str] = set()
        for index, item in enumerate(self.substance.codes or []):
            if self._clean_text(item.type) != 'PRIMARY':
                continue
            system = self._clean_text(item.codeSystem)
            if not system or system.upper() in seen:
                continue
            if not item.isClassification and system.upper() not in preferred_order:
                continue
            seen.add(system.upper())
            try:
                order = preferred_order.index(system.upper())
            except ValueError:
                order = len(preferred_order) + index
            classifications.append(((order, index), system))
        if not classifications:
            return ''
        labels = [label for _, label in sorted(classifications)[:9]]
        return f'And classifications such as {self._oxford_join(labels)}.'

    def _summary_content_topics(self) -> list[str]:
        """Get list of content topics for summary."""
        topics: list[str] = []
        if any(self._clean_text(item.name) for item in (self.substance.properties or [])):
            topics.append('properties')
        if any(self._clean_text(item.type) for item in (self.substance.relationships or [])):
            topics.append('relationships')
        modifications = self.substance.modifications
        if modifications and any([
            modifications.agentModifications,
            modifications.physicalModifications,
            modifications.structuralModifications,
        ]):
            topics.append('modifications')
        if self.substance.references:
            topics.append('references')
        if self.substance.notes:
            topics.append('notes')
        return topics

    def _summary_content_sentence(self) -> str:
        """Generate content summary sentence."""
        topics = self._summary_content_topics()
        if not topics:
            return ''
        return f'Content covers {self._oxford_join(topics)}.'

    def _summary_text(self) -> str:
        """Generate full summary text for embedding."""
        document_name = self._summary_title_name()
        substance_class = self._substance_class_value()
        approval_id_display = self._clean_text(self.substance.approvalIDDisplay or self.substance.approvalID)
        definition_type = self._clean_text(self.substance.definitionType)
        definition_level = self._clean_text(self.substance.definitionLevel)
        status = self._clean_text(self.substance.status) or 'approved' if approval_id_display else None
        parts = [f'{document_name} is a']
        parts.append('protected from access' if self.substance.access else 'for publicly accessible')
        if self.substance.deprecated:
            parts.append('deprecated')
        parts.append(f'{substance_class} substance.')
        if status:
            parts.append(f'Current status is')
            if approval_id_display:
                parts.append(f'{status} with approval ID {approval_id_display}.')
            else:
                parts.append(f'{status}.')
        if definition_type or definition_level:
            parts.append('Definition')
            if definition_type:
                parts.append(f'type {definition_type}{"" if definition_level else "."}')
            if definition_level:
                parts.append(f'and definition level {definition_level}.' if definition_type else f'level {definition_level}.')
        for sentence in [
            self._summary_definitional_sentence(),
            self._summary_names_sentence(),
            self._summary_primary_identifiers_sentence(),
            self._summary_classifications_sentence(),
            self._summary_content_sentence(),
        ]:
            if sentence:
                parts.append(sentence)
        return ' '.join(parts)

    # =========================================================================
    # to_embedding_chunks methods for all model classes
    # =========================================================================

    def to_embedding_chunks(self) -> list[dict[str, object]]:
        """Generate embedding chunks for the substance."""
        document_id = self._clean_text(self.substance.uuid)
        name = self._stable_name()
        substance_class = self._substance_class_value()
        approval_id = self._clean_text(self.substance.approvalID)
        definition_type = self._clean_text(self.substance.definitionType)
        definition_level = self._clean_text(self.substance.definitionLevel)
        status = self._clean_text(self.substance.status)
        tags = self._clean_list(self.substance.tags)
        parts = [self._summary_text()]

        rows = [
            {
                'chunk_id': f'root_uuid:{self.substance.uuid}',
                'document_id': document_id,
                'source_url': self._embedding_source_name(self.substance),
                'section': 'summary',
                'text': ' '.join(parts),
                'metadata': {
                    **self._chunk_metadata(self.substance),
                    **self._hierarchy_metadata('root'),
                    'json_path': '$',
                    'canonical_name': name,
                    'system_name': self._clean_text(self.substance.systemName) or None,
                    'substance_class': substance_class,
                    'approval_id': approval_id or None,
                    'status': status or None,
                    'definition_type': definition_type or None,
                    'definition_level': definition_level or None,
                    'version': self._clean_text(self.substance.version) or None,
                    'tags': tags or None,
                    'name_count': len(self.substance.names or []),
                    'code_count': len(self.substance.codes or []),
                    'property_count': len(self.substance.properties or []),
                    'relationship_count': len(self.substance.relationships or []),
                    'note_count': len(self.substance.notes or []),
                    'reference_count': len(self.substance.references or []),
                    **self._substance_class_metadata(),
                },
            }
        ]

        for item in self.substance.names or []:
            rows.extend(self.name_to_embedding_chunks(item))

        for item in self.substance.codes or []:
            rows.extend(self.code_to_embedding_chunks(item))

        for item in self.substance.properties or []:
            rows.extend(self.property_to_embedding_chunks(item))
        for item in self.substance.relationships or []:
            rows.extend(self.relationship_to_embedding_chunks(item))
        for item in self.substance.notes or []:
            rows.extend(self.note_to_embedding_chunks(item))
        for item in self.substance.references or []:
            rows.extend(self.reference_to_embedding_chunks(item))

        modifications = self.substance.modifications
        if modifications is not None:
            rows.extend(self.modifications_to_embedding_chunks(modifications))

        return rows

    def name_to_embedding_chunks(self, item: Any) -> list[dict[str, object]]:
        """Generate embedding chunks for a Name object."""
        raw_name = self._clean_text(item.name)
        name_type = self._clean_text(item.type)
        name_type_label = self._name_type_label(name_type)
        std_name = self._clean_text(self._safe_get(item, 'stdName'))
        if not raw_name:
            return []

        subject = self._embedding_root_name(item)
        domains = self._clean_list(self._safe_get(item, 'domains'))
        languages = self._clean_list(self._safe_get(item, 'languages'))
        name_jurisdiction = self._clean_list(self._safe_get(item, 'nameJurisdiction'))
        name_orgs = self._clean_list([no.nameOrg for no in (self._safe_get(item, 'nameOrgs') or []) if no.nameOrg])
        access = 'protected' if self._safe_get(item, 'access') else 'public'
        parts = [f'{raw_name} is a {access} {name_type_label}']
        display_name = self._safe_get(item, 'displayName')
        preferred = self._safe_get(item, 'preferred')
        if display_name or preferred:
            parts.append('that is used as')
            if display_name and preferred:
                parts.append('both a display and preferred')
            elif display_name:
                parts.append('a display')
            else:
                parts.append('a preferred')
            parts.append('name')
        parts.append(f'for {subject}.')
        if name_orgs:
            parts.append(f'It is registered by {", ".join(name_orgs)} naming organizations as the official name.')
        if std_name and std_name != raw_name:
            parts.append(f'Standardized name {std_name}.')

        document_id = self._embedding_document_id(item)

        return [
            {
                'chunk_id': f'root_names_uuid:{item.uuid}',
                'document_id': document_id,
                'source_url': self._embedding_source_name(item),
                'section': 'names',
                'text': ' '.join(parts),
                'metadata': {
                    **self._chunk_metadata(item),
                    **self._hierarchy_metadata('root', 'names'),
                    'json_path': self._embedding_json_path(item, '$.names[*]'),
                    'name_value': raw_name,
                    'name_type': name_type or None,
                    'name_type_label': name_type_label or None,
                    'std_name': std_name or None,
                    'preferred': bool(preferred),
                    'display_name': bool(display_name),
                    'domains': domains or None,
                    'languages': languages or None,
                    'name_jurisdiction': name_jurisdiction or None,
                    'name_orgs': name_orgs or None,
                    'references': self._embedding_references(item) or None,
                },
            }
        ]

    @classmethod
    def _name_type_label(cls, value: str) -> str:
        """Get label for name type."""
        cleaned = cls._clean_text(value)
        if not cleaned:
            return 'synonym'
        _NAME_TYPE_LABELS = {
            'bn': 'Brand Name',
            'cd': 'Code',
            'cn': 'Common Name',
            'of': 'Official Name',
            'sci': 'Scientific Name',
            'sys': 'Systematic Name',
            'syn': 'Synonym',
        }
        return _NAME_TYPE_LABELS.get(cleaned.lower(), '%s type name' % cleaned)

    def code_to_embedding_chunks(self, item: Any) -> list[dict[str, object]]:
        """Generate embedding chunks for a Code object."""
        code_system = self._clean_text(item.codeSystem)
        code = self._clean_text(item.code)
        code_type = self._clean_text(item.type)
        code_text = self._clean_text(item.codeText)
        comments = self._clean_text(item.comments)
        url = self._clean_text(item.url)
        access = 'protected' if item.access else 'public'
        if not code:
            return []

        subject = self._embedding_root_name(item)
        document_id = self._embedding_document_id(item)
        text_parts = [f"{subject} {access} {code_type.lower()}"]
        class_parts = []
        class_metadata = {}
        if item.isClassification:
            text_parts.append(f"classification code {code} in {code_system or 'unknown'} code system:")
            class_parts = [self._clean_text(part) for part in (comments or '').split('|')]
            class_parts = [part for part in class_parts if part]
            if class_parts:
                class_metadata = {
                    'classification_hierarchy': class_parts,
                    'classification_path': ' > '.join(class_parts),
                }
                text_parts.append(f"{class_metadata['classification_path']}.")
        else:
            text_parts.append(f"Identifier code {code} in {code_system or 'unknown'} code system: {code}.")
        if code_text and code_text != code:
            text_parts.append(f'Code text: {code_text}.')
        return [
            {
                'chunk_id': f'root_codes_uuid:{item.uuid}',
                'document_id': document_id,
                'source_url': self._embedding_source_name(item),
                'section': 'codes',
                'text': ' '.join(text_parts),
                'metadata': {
                    **self._chunk_metadata(item),
                    **self._hierarchy_metadata('root', 'codes'),
                    **class_metadata,
                    'json_path': self._embedding_json_path(item, '$.codes[*]'),
                    'code_system': code_system or None,
                    'code': code,
                    'code_type': code_type or None,
                    'code_text': code_text or None,
                    'comments': comments or None,
                    'url': url or None,
                    'references': self._embedding_references(item) or None,
                },
            }
        ]

    def property_to_embedding_chunks(self, item: Any) -> list[dict[str, object]]:
        """Generate embedding chunks for a Property object."""
        prop_name = self._clean_text(item.name)
        value_text = self._render_property_value(item)
        property_type = self._clean_text(item.propertyType)
        value_type = self._clean_text(item.type)
        ref_substance = item.referencedSubstance
        referenced_name = self._get_refPname(ref_substance) if ref_substance else ''
        referenced_id = self._get_refuuid(ref_substance) if ref_substance else ''
        parameter_names = self._clean_list([p.name for p in (item.parameters or []) if p.name])
        if not prop_name and not value_text:
            return []

        subject = self._embedding_root_name(item)
        document_id = self._embedding_document_id(item)
        access = 'protected' if item.access else 'public'

        parts = [f'{subject} {access} property {prop_name}.']
        if property_type:
            parts.append(f'Property type {property_type}.')
        if value_type:
            parts.append(f'Value type {value_type}.')
        if value_text:
            parts.append(f'Value {value_text}.')

        return [
            {
                'chunk_id': f'root_properties_uuid:{item.uuid}',
                'document_id': document_id,
                'source_url': self._embedding_source_name(item),
                'section': 'properties',
                'text': ' '.join(parts),
                'metadata': {
                    **self._chunk_metadata(item),
                    **self._hierarchy_metadata('root', 'properties'),
                    'json_path': self._embedding_json_path(item, '$.properties[*]'),
                    'property_name': prop_name or None,
                    'property_type': property_type or None,
                    'value_type': value_type or None,
                    'value_text': value_text or None,
                    'defining': bool(item.defining),
                    'referenced_name': referenced_name or None,
                    'referenced_id': referenced_id or None,
                    'parameter_names': parameter_names or None,
                    'references': self._embedding_references(item) or None,
                },
            }
        ]

    def _render_property_value(self, item: Any) -> str:
        """Render property value as string."""
        parts: list[str] = []
        value = item.value
        value_text = value.as_string() if value else ''
        if value_text:
            parts.append(value_text)
        ref_substance = item.referencedSubstance
        ref_name = self._get_refPname(ref_substance) if ref_substance else ''
        if ref_name:
            parts.append(f'referenced substance {ref_name}')
        param_bits = []
        for parameter in item.parameters or []:
            pname = self._clean_text(parameter.name)
            ptype = self._clean_text(parameter.type)
            pvalue = parameter.value
            pvalue_text = pvalue.as_string() if pvalue else ''
            bit = pname
            if ptype:
                bit = f'{bit} ({ptype})' if bit else ptype
            if pvalue_text:
                bit = f'{bit}: {pvalue_text}' if bit else pvalue_text
            if bit:
                param_bits.append(bit)
        if param_bits:
            parts.append('parameters ' + '; '.join(param_bits))
        return '. '.join(parts).strip('. ')

    def relationship_to_embedding_chunks(self, item: Any) -> list[dict[str, object]]:
        """Generate embedding chunks for a Relationship object."""
        rel_type = self._clean_text(item.type)
        related_substance = item.relatedSubstance
        related_name = self._get_refPname(related_substance) if related_substance else ''
        related_id = self._get_refuuid(related_substance) if related_substance else ''
        qualification = self._clean_text(item.qualification)
        interaction_type = self._clean_text(item.interactionType)
        mediator_substance = item.mediatorSubstance
        mediator_name = self._get_refPname(mediator_substance) if mediator_substance else ''
        mediator_id = self._get_refuuid(mediator_substance) if mediator_substance else ''
        amount = item.amount
        amount_text = amount.as_string() if amount else ''
        comments = self._clean_text(item.comments)
        if not rel_type and not related_name:
            return []

        subject = self._embedding_root_name(item)
        document_id = self._embedding_document_id(item)
        access = 'protected' if item.access else 'public'
        parts = [f'{subject} has {access} relationship {rel_type} with {related_name}.']
        if qualification:
            parts.append(f'Qualification {qualification}.')
        if interaction_type:
            parts.append(f'Interaction type {interaction_type}.')
        if mediator_name:
            parts.append(f'Mediator substance {mediator_name}.')
        if amount_text:
            parts.append(f'Amount {amount_text}.')
        if comments:
            parts.append(f'Comments {comments}.')

        return [
            {
                'chunk_id': f'root_relationships_uuid:{item.uuid}',
                'document_id': document_id,
                'source_url': self._embedding_source_name(item),
                'section': 'relationships',
                'text': ' '.join(parts).strip(),
                'metadata': {
                    **self._chunk_metadata(item),
                    **self._hierarchy_metadata('root', 'relationships'),
                    'json_path': self._embedding_json_path(item, '$.relationships[*]'),
                    'relationship_type': rel_type or None,
                    'related_name': related_name or None,
                    'related_id': related_id or None,
                    'qualification': qualification or None,
                    'interaction_type': interaction_type or None,
                    'mediator_name': mediator_name or None,
                    'mediator_id': mediator_id or None,
                    'amount_text': amount_text or None,
                    'comments': comments or None,
                    'references': self._embedding_references(item) or None,
                },
            }
        ]

    def note_to_embedding_chunks(self, item: Any) -> list[dict[str, object]]:
        """Generate embedding chunks for a Note object."""
        note = self._clean_text(item.note)
        if not note:
            return []

        subject = self._embedding_root_name(item)
        document_id = self._embedding_document_id(item)
        access = 'protected' if item.access else 'public'

        return [
            {
                'chunk_id': f'root_notes_uuid:{item.uuid}',
                'document_id': document_id,
                'source_url': self._embedding_source_name(item),
                'section': 'notes',
                'text': f'{subject} {access} note: {note}',
                'metadata': {
                    **self._chunk_metadata(item),
                    **self._hierarchy_metadata('root', 'notes'),
                    'json_path': self._embedding_json_path(item, '$.notes[*]'),
                    'note_length': len(note),
                    'references': self._embedding_references(item) or None,
                },
            }
        ]

    def reference_to_embedding_chunks(self, item: Any) -> list[dict[str, object]]:
        """Generate embedding chunks for a Reference object."""
        citation = self._clean_text(item.citation)
        doc_type = self._clean_text(item.docType)
        tags = self._clean_list(item.tags)
        reference_url = self._clean_text(item.url)
        uploaded_file = self._clean_text(item.uploadedFile)
        reference_id = self._clean_text(item.id or item.uuid)
        reference_text = self._embedding_reference_text(item)
        access = 'Protected' if item.access else 'Public'
        if not citation and not doc_type:
            return []

        subject = self._embedding_root_name(item)
        parts = [f'{access} reference for {subject}.']
        if doc_type:
            parts.append(f'Document type {doc_type}.')
        if citation:
            parts.append(f'Citation: {citation}.')
        if reference_url:
            parts.append(f'URL: {reference_url}.')

        document_id = self._embedding_document_id(item)

        return [
            {
                'chunk_id': f'root_references_uuid:{item.uuid}',
                'document_id': document_id,
                'source_url': self._embedding_source_name(item),
                'section': 'references',
                'text': ' '.join(parts),
                'metadata': {
                    **self._chunk_metadata(item),
                    **self._hierarchy_metadata('root', 'references'),
                    'json_path': self._embedding_json_path(item, '$.references[*]'),
                    'references': [reference_text] if reference_text else None,
                    'doc_type': doc_type or None,
                    'citation': citation or None,
                    'reference_url': reference_url or None,
                    'reference_id': reference_id or None,
                    'uploaded_file': uploaded_file or None,
                    'public_domain': bool(item.publicDomain),
                    'tags': tags or None,
                },
            }
        ]

    def modifications_to_embedding_chunks(self, item: Any) -> list[dict[str, object]]:
        """Generate embedding chunks for a Modifications object."""
        rows: list[dict[str, object]] = []

        for mod_item in item.agentModifications or []:
            rows.extend(self.agent_modification_to_embedding_chunks(mod_item))
        for mod_item in item.physicalModifications or []:
            rows.extend(self.physical_modification_to_embedding_chunks(mod_item))
        for mod_item in item.structuralModifications or []:
            rows.extend(self.structural_modification_to_embedding_chunks(mod_item))

        return rows

    def agent_modification_to_embedding_chunks(self, item: Any) -> list[dict[str, object]]:
        """Generate embedding chunks for an AgentModification object."""
        subject = self._embedding_root_name(item)
        document_id = self._embedding_document_id(item)

        return [
            {
                'chunk_id': f'root_modifications_agentModifications_uuid:{item.uuid}',
                'document_id': document_id,
                'source_url': self._embedding_source_name(item),
                'section': 'agentModifications',
                'text': f'{subject} agent modification type {self._clean_text(item.agentModificationType)}.',
                'metadata': {
                    **self._chunk_metadata(item),
                    **self._hierarchy_metadata('root', 'modifications', 'agentModifications'),
                    'modification_kind': 'agent',
                },
            }
        ]

    def physical_modification_to_embedding_chunks(self, item: Any) -> list[dict[str, object]]:
        """Generate embedding chunks for a PhysicalModification object."""
        subject = self._embedding_root_name(item)
        document_id = self._embedding_document_id(item)
        access = 'protected' if item.access else 'public'

        return [
            {
                'chunk_id': f'root_modifications_physicalModifications_uuid:{item.uuid}',
                'document_id': document_id,
                'source_url': self._embedding_source_name(item),
                'section': 'physicalModifications',
                'text': f'{subject} {access} physical modification role {self._clean_text(item.physicalModificationRole)}.',
                'metadata': {
                    **self._chunk_metadata(item),
                    **self._hierarchy_metadata('root', 'modifications', 'physicalModifications'),
                    'modification_kind': 'physical',
                },
            }
        ]

    def structural_modification_to_embedding_chunks(self, item: Any) -> list[dict[str, object]]:
        """Generate embedding chunks for a StructuralModification object."""
        subject = self._embedding_root_name(item)
        document_id = self._embedding_document_id(item)
        access = 'protected' if item.access else 'public'

        return [
            {
                'chunk_id': f'root_modifications_structuralModifications_uuid:{item.uuid}',
                'document_id': document_id,
                'source_url': self._embedding_source_name(item),
                'section': 'structuralModifications',
                'text': f'{subject} {access} structural modification type {self._clean_text(item.structuralModificationType)}.',
                'metadata': {
                    **self._chunk_metadata(item),
                    **self._hierarchy_metadata('root', 'modifications', 'structuralModifications'),
                    'modification_kind': 'structural',
                },
            }
        ]

    def protein_to_embedding_chunks(self, item: Any) -> list[dict[str, object]]:
        """Generate embedding chunks for a Protein object."""
        rows: list[dict[str, object]] = []

        for subitem in item.subunits or []:
            rows.extend(self.subunit_to_embedding_chunks(subitem))
        for subitem in item.disulfideLinks or []:
            rows.extend(self.disulfide_link_to_embedding_chunks(subitem))
        for subitem in item.otherLinks or []:
            rows.extend(self.other_link_to_embedding_chunks(subitem))
        glycosylation = item.glycosylation
        if glycosylation:
            rows.extend(self.glycosylation_to_embedding_chunks(glycosylation))
        modifications = item.modifications
        if modifications:
            rows.extend(self.modifications_to_embedding_chunks(modifications))

        return rows

    def nucleic_acid_to_embedding_chunks(self, item: Any) -> list[dict[str, object]]:
        """Generate embedding chunks for a NucleicAcid object."""
        rows: list[dict[str, object]] = []

        for subitem in item.subunits or []:
            rows.extend(self.subunit_to_embedding_chunks(subitem))
        for subitem in item.linkages or []:
            rows.extend(self.linkage_to_embedding_chunks(subitem))
        for subitem in item.sugars or []:
            rows.extend(self.sugar_to_embedding_chunks(subitem))
        modifications = item.modifications
        if modifications:
            rows.extend(self.modifications_to_embedding_chunks(modifications))

        return rows

    def mixture_to_embedding_chunks(self, item: Any) -> list[dict[str, object]]:
        """Generate embedding chunks for a Mixture object."""
        rows: list[dict[str, object]] = []

        for subitem in item.components or []:
            rows.extend(self.component_to_embedding_chunks(subitem))

        return rows

    def polymer_to_embedding_chunks(self, item: Any) -> list[dict[str, object]]:
        """Generate embedding chunks for a Polymer object."""
        rows: list[dict[str, object]] = []

        classification = item.classification
        if classification:
            rows.extend(self.polymer_classification_to_embedding_chunks(classification))
        for subitem in item.monomers or []:
            rows.extend(self.material_to_embedding_chunks(subitem))
        for subitem in item.structuralUnits or []:
            rows.extend(self.unit_to_embedding_chunks(subitem))

        return rows

    def structurally_diverse_to_embedding_chunks(self, item: Any) -> list[dict[str, object]]:
        """Generate embedding chunks for a StructurallyDiverse object."""
        organism_parts = []
        if item.organismFamily:
            organism_parts.append(f"family {self._clean_text(item.organismFamily)}")
        if item.organismGenus:
            organism_parts.append(f"genus {self._clean_text(item.organismGenus)}")
        if item.organismSpecies:
            organism_parts.append(f"species {self._clean_text(item.organismSpecies)}")

        source_parts = []
        if item.sourceMaterialClass:
            source_parts.append(f"class {self._clean_text(item.sourceMaterialClass)}")
        if item.sourceMaterialType:
            source_parts.append(f"type {self._clean_text(item.sourceMaterialType)}")
        if item.sourceMaterialState:
            source_parts.append(f"state {self._clean_text(item.sourceMaterialState)}")

        has_content = organism_parts or source_parts or item.part or item.fractionName
        if not has_content:
            return []

        subject = self._embedding_root_name(item)
        document_id = self._embedding_document_id(item)
        access = 'protected' if item.access else 'public'

        content_parts = [f"{subject} {access} structurally diverse substance"]
        if organism_parts:
            content_parts.append("organism " + ', '.join(organism_parts))
        if source_parts:
            content_parts.append("source material " + ', '.join(source_parts))
        part_list = [self._clean_text(p) for p in (item.part or []) if self._clean_text(p)]
        if part_list:
            content_parts.append(f"parts {', '.join(part_list)}")
        if item.fractionName:
            content_parts.append(f"fraction {self._clean_text(item.fractionName)}")

        return [
            {
                'chunk_id': f'root_structurally_diverse_uuid:{item.uuid}',
                'document_id': document_id,
                'source_url': self._embedding_source_name(item),
                'section': 'structurally_diverse',
                'text': '. '.join(content_parts) + '.',
                'metadata': {
                    **self._chunk_metadata(item),
                    **self._hierarchy_metadata('root', 'structurally_diverse'),
                    'organism_family': self._clean_text(item.organismFamily) or None,
                    'organism_genus': self._clean_text(item.organismGenus) or None,
                    'organism_species': self._clean_text(item.organismSpecies) or None,
                    'source_material_class': self._clean_text(item.sourceMaterialClass) or None,
                    'source_material_type': self._clean_text(item.sourceMaterialType) or None,
                    'fraction_name': self._clean_text(item.fractionName) or None,
                },
            }
        ]

    def specified_substance_g1_to_embedding_chunks(self, item: Any) -> list[dict[str, object]]:
        """Generate embedding chunks for a SpecifiedSubstanceG1 object."""
        rows: list[dict[str, object]] = []

        for subitem in item.constituents or []:
            rows.extend(self.specified_substance_component_to_embedding_chunks(subitem))

        return rows

    def component_to_embedding_chunks(self, item: Any) -> list[dict[str, object]]:
        """Generate embedding chunks for a Component object."""
        component_type = item.type.value if item.type else None
        substance = item.substance
        substance_name = self._get_refPname(substance) if substance else ''
        if not component_type and not substance_name:
            return []

        subject = self._embedding_root_name(item)
        document_id = self._embedding_document_id(item)
        access = 'protected' if item.access else 'public'

        return [
            {
                'chunk_id': f'root_components_uuid:{item.uuid}',
                'document_id': document_id,
                'source_url': self._embedding_source_name(item),
                'section': 'components',
                'text': f"{subject} {access} component {component_type or 'unspecified'}: {substance_name}.".strip(),
                'metadata': {
                    **self._chunk_metadata(item),
                    **self._hierarchy_metadata('root', 'components'),
                    'component_type': component_type or None,
                    'substance_name': substance_name or None,
                    'substance_id': self._get_refuuid(substance) if substance else None,
                },
            }
        ]

    def subunit_to_embedding_chunks(self, item: Any) -> list[dict[str, object]]:
        """Generate embedding chunks for a Subunit object."""
        sequence = self._clean_text(item.sequence)
        if not sequence:
            return []

        subject = self._embedding_root_name(item)
        document_id = self._embedding_document_id(item)
        access = 'protected' if item.access else 'public'

        return [
            {
                'chunk_id': f'root_subunits_uuid:{item.uuid}',
                'document_id': document_id,
                'source_url': self._embedding_source_name(item),
                'section': 'subunits',
                'text': f"{subject} {access} subunit {int(item.subunitIndex) if item.subunitIndex else 'unspecified'}: sequence length {item.length or len(sequence)} residues.",
                'metadata': {
                    **self._chunk_metadata(item),
                    **self._hierarchy_metadata('root', 'subunits'),
                    'subunit_index': item.subunitIndex or None,
                    'sequence_length': item.length or len(sequence) if sequence else None,
                    'sequence': sequence[:500] if len(sequence) > 500 else sequence,
                },
            }
        ]

    def sugar_to_embedding_chunks(self, item: Any) -> list[dict[str, object]]:
        """Generate embedding chunks for a Sugar object."""
        sugar_name = self._clean_text(item.sugar)
        sites_shorthand = self._clean_text(item.sitesShorthand)
        if not sugar_name:
            return []

        subject = self._embedding_root_name(item)
        document_id = self._embedding_document_id(item)
        access = 'protected' if item.access else 'public'

        return [
            {
                'chunk_id': f'root_sugars_uuid:{item.uuid}',
                'document_id': document_id,
                'source_url': self._embedding_source_name(item),
                'section': 'sugars',
                'text': f"{subject} {access} nucleic acid sugar {sugar_name} at {sites_shorthand or 'unspecified sites'}.".strip(),
                'metadata': {
                    **self._chunk_metadata(item),
                    **self._hierarchy_metadata('root', 'sugars'),
                    'sugar_name': sugar_name or None,
                    'sites': sites_shorthand or None,
                },
            }
        ]

    def linkage_to_embedding_chunks(self, item: Any) -> list[dict[str, object]]:
        """Generate embedding chunks for a Linkage object."""
        linkage_type = self._clean_text(item.linkage)
        sites_shorthand = self._clean_text(item.sitesShorthand)
        if not linkage_type and not sites_shorthand:
            return []

        subject = self._embedding_root_name(item)
        document_id = self._embedding_document_id(item)
        access = 'protected' if item.access else 'public'

        return [
            {
                'chunk_id': f'root_linkages_uuid:{item.uuid}',
                'document_id': document_id,
                'source_url': self._embedding_source_name(item),
                'section': 'linkages',
                'text': f"{subject} {access} nucleic acid linkage {linkage_type or 'unspecified'} at {sites_shorthand or 'unspecified sites'}.".strip(),
                'metadata': {
                    **self._chunk_metadata(item),
                    **self._hierarchy_metadata('root', 'linkages'),
                    'linkage_type': linkage_type or None,
                    'sites': sites_shorthand or None,
                },
            }
        ]

    def glycosylation_to_embedding_chunks(self, item: Any) -> list[dict[str, object]]:
        """Generate embedding chunks for a Glycosylation object."""
        glyco_type = self._clean_text(item.glycosylationType)
        has_content = glyco_type or item.CGlycosylationSites or item.NGlycosylationSites or item.OGlycosylationSites
        if not has_content:
            return []

        subject = self._embedding_root_name(item)
        document_id = self._embedding_document_id(item)
        access = 'protected' if item.access else 'public'

        content_parts = [f"{subject} {access} glycosylation"]
        if glyco_type:
            content_parts.append(f"type {glyco_type}")
        site_info = []
        c_sites = item.CGlycosylationSites
        n_sites = item.NGlycosylationSites
        o_sites = item.OGlycosylationSites
        if c_sites:
            site_info.append(f"C-glycosylation at {len(c_sites)} sites")
        if n_sites:
            site_info.append(f"N-glycosylation at {len(n_sites)} sites")
        if o_sites:
            site_info.append(f"O-glycosylation at {len(o_sites)} sites")
        if site_info:
            content_parts.append(', '.join(site_info))

        return [
            {
                'chunk_id': f'root_glycosylation_uuid:{item.uuid}',
                'document_id': document_id,
                'source_url': self._embedding_source_name(item),
                'section': 'glycosylation',
                'text': '. '.join(content_parts) + '.',
                'metadata': {
                    **self._chunk_metadata(item),
                    **self._hierarchy_metadata('root', 'glycosylation'),
                    'glycosylation_type': glyco_type or None,
                    'c_sites_count': len(c_sites) if c_sites else None,
                    'n_sites_count': len(n_sites) if n_sites else None,
                    'o_sites_count': len(o_sites) if o_sites else None,
                },
            }
        ]

    def disulfide_link_to_embedding_chunks(self, item: Any) -> list[dict[str, object]]:
        """Generate embedding chunks for a DisulfideLink object."""
        sites_shorthand = self._clean_text(item.sitesShorthand)
        if not sites_shorthand:
            return []

        subject = self._embedding_root_name(item)
        document_id = self._embedding_document_id(item)
        access = 'protected' if item.access else 'public'

        return [
            {
                'chunk_id': f'root_disulfide_links_uuid:{item.uuid}',
                'document_id': document_id,
                'source_url': self._embedding_source_name(item),
                'section': 'disulfide_links',
                'text': f"{subject} {access} disulfide bond at {sites_shorthand}.",
                'metadata': {
                    **self._chunk_metadata(item),
                    **self._hierarchy_metadata('root', 'disulfide_links'),
                    'sites': sites_shorthand or None,
                },
            }
        ]

    def other_link_to_embedding_chunks(self, item: Any) -> list[dict[str, object]]:
        """Generate embedding chunks for an OtherLink object."""
        linkage_type = self._clean_text(item.linkageType)
        sites_shorthand = self._clean_text(item.sitesShorthand)
        if not linkage_type and not sites_shorthand:
            return []

        subject = self._embedding_root_name(item)
        document_id = self._embedding_document_id(item)
        access = 'protected' if item.access else 'public'

        return [
            {
                'chunk_id': f'root_other_links_uuid:{item.uuid}',
                'document_id': document_id,
                'source_url': self._embedding_source_name(item),
                'section': 'other_links',
                'text': f"{subject} {access} linkage type {linkage_type or 'unspecified'} at {sites_shorthand or 'unspecified sites'}.".strip(),
                'metadata': {
                    **self._chunk_metadata(item),
                    **self._hierarchy_metadata('root', 'other_links'),
                    'linkage_type': linkage_type or None,
                    'sites': sites_shorthand or None,
                },
            }
        ]

    def material_to_embedding_chunks(self, item: Any) -> list[dict[str, object]]:
        """Generate embedding chunks for a Material object."""
        material_type = self._clean_text(item.type)
        monomer_substance = item.monomerSubstance
        monomer_name = self._get_refPname(monomer_substance) if monomer_substance else ''
        amount = item.amount
        amount_text = amount.as_string() if amount else ''
        if not material_type and not monomer_name:
            return []

        subject = self._embedding_root_name(item)
        document_id = self._embedding_document_id(item)
        access = 'protected' if item.access else 'public'

        content_parts = [f"{subject} {access} polymer material"]
        if material_type:
            content_parts.append(f"role {material_type}")
        if monomer_name:
            content_parts.append(f"monomer {monomer_name}")
        if amount_text:
            content_parts.append(f"amount {amount_text}")

        return [
            {
                'chunk_id': f'root_materials_uuid:{item.uuid}',
                'document_id': document_id,
                'source_url': self._embedding_source_name(item),
                'section': 'materials',
                'text': '. '.join(content_parts) + '.',
                'metadata': {
                    **self._chunk_metadata(item),
                    **self._hierarchy_metadata('root', 'materials'),
                    'material_type': material_type or None,
                    'monomer_name': monomer_name or None,
                    'monomer_id': self._get_refuuid(monomer_substance) if monomer_substance else None,
                    'defining': bool(item.defining),
                },
            }
        ]

    def unit_to_embedding_chunks(self, item: Any) -> list[dict[str, object]]:
        """Generate embedding chunks for a Unit object."""
        unit_type = self._clean_text(item.type)
        label = self._clean_text(item.label)
        amount = item.amount
        amount_text = amount.as_string() if amount else ''
        if not unit_type and not label and not amount_text:
            return []

        subject = self._embedding_root_name(item)
        document_id = self._embedding_document_id(item)
        access = 'protected' if item.access else 'public'

        content_parts = [f"{subject} {access} polymer unit"]
        if unit_type:
            content_parts.append(f"type {unit_type}")
        if label:
            content_parts.append(f"label {label}")
        if amount_text:
            content_parts.append(f"amount {amount_text}")

        return [
            {
                'chunk_id': f'root_units_uuid:{item.uuid}',
                'document_id': document_id,
                'source_url': self._embedding_source_name(item),
                'section': 'units',
                'text': '. '.join(content_parts) + '.',
                'metadata': {
                    **self._chunk_metadata(item),
                    **self._hierarchy_metadata('root', 'units'),
                    'unit_type': unit_type or None,
                    'label': label or None,
                    'attachment_count': item.attachmentCount or None,
                },
            }
        ]

    def polymer_classification_to_embedding_chunks(self, item: Any) -> list[dict[str, object]]:
        """Generate embedding chunks for a PolymerClassification object."""
        polymer_class = self._clean_text(item.polymerClass)
        polymer_geometry = self._clean_text(item.polymerGeometry)
        source_type = self._clean_text(item.sourceType)
        parent_substance = item.parentSubstance
        parent_name = self._get_refPname(parent_substance) if parent_substance else ''
        if not polymer_class and not polymer_geometry and not source_type:
            return []

        subject = self._embedding_root_name(item)
        document_id = self._embedding_document_id(item)
        access = 'protected' if item.access else 'public'

        content_parts = [f"{subject} {access} polymer classification"]
        if polymer_class:
            content_parts.append(f"class {polymer_class}")
        if polymer_geometry:
            content_parts.append(f"geometry {polymer_geometry}")
        if source_type:
            content_parts.append(f"source type {source_type}")
        if parent_name:
            content_parts.append(f"parent {parent_name}")

        return [
            {
                'chunk_id': f'root_polymer_classification_uuid:{item.uuid}',
                'document_id': document_id,
                'source_url': self._embedding_source_name(item),
                'section': 'polymer_classification',
                'text': '. '.join(content_parts) + '.',
                'metadata': {
                    **self._chunk_metadata(item),
                    **self._hierarchy_metadata('root', 'polymer_classification'),
                    'polymer_class': polymer_class or None,
                    'polymer_geometry': polymer_geometry or None,
                    'source_type': source_type or None,
                    'parent_substance': parent_name or None,
                    'polymer_subclass': item.polymerSubclass or None,
                },
            }
        ]

    def parameter_to_embedding_chunks(self, item: Any) -> list[dict[str, object]]:
        """Generate embedding chunks for a Parameter object."""
        param_name = self._clean_text(item.name)
        param_type = self._clean_text(item.type)
        value = item.value
        value_text = value.as_string() if value else ''
        if not param_name and not value_text:
            return []

        subject = self._embedding_root_name(item)
        document_id = self._embedding_document_id(item)
        access = 'protected' if item.access else 'public'

        return [
            {
                'chunk_id': f'root_parameters_uuid:{item.uuid}',
                'document_id': document_id,
                'source_url': self._embedding_source_name(item),
                'section': 'parameters',
                'text': f"{subject} {access} parameter {param_name}{f' ({param_type})' if param_type else ''}: {value_text}.".strip(),
                'metadata': {
                    **self._chunk_metadata(item),
                    **self._hierarchy_metadata('root', 'parameters'),
                    'parameter_name': param_name or None,
                    'parameter_type': param_type or None,
                },
            }
        ]

    def physical_parameter_to_embedding_chunks(self, item: Any) -> list[dict[str, object]]:
        """Generate embedding chunks for a PhysicalParameter object."""
        param_name = self._clean_text(item.parameterName)
        amount = item.amount
        amount_text = amount.as_string() if amount else ''
        if not param_name and not amount_text:
            return []

        subject = self._embedding_root_name(item)
        document_id = self._embedding_document_id(item)
        access = 'protected' if item.access else 'public'

        return [
            {
                'chunk_id': f'root_physical_parameters_uuid:{item.uuid}',
                'document_id': document_id,
                'source_url': self._embedding_source_name(item),
                'section': 'physical_parameters',
                'text': f"{subject} {access} physical parameter {param_name}: {amount_text}.".strip(),
                'metadata': {
                    **self._chunk_metadata(item),
                    **self._hierarchy_metadata('root', 'physical_parameters'),
                    'parameter_name': param_name or None,
                },
            }
        ]

    def substance_reference_to_embedding_chunks(self, item: Any) -> list[dict[str, object]]:
        """Generate embedding chunks for a SubstanceReference object."""
        ref_name = self._get_refPname(item)
        approval_id = self._clean_text(item.approvalID)
        linking_id = self._clean_text(item.linkingID)
        if not ref_name and not approval_id:
            return []

        subject = self._embedding_root_name(item)
        document_id = self._embedding_document_id(item)
        access = 'protected' if item.access else 'public'

        content_parts = [f"{subject} {access} substance reference"]
        if ref_name:
            content_parts.append(ref_name)
        if approval_id:
            content_parts.append(f"approval ID {approval_id}")

        return [
            {
                'chunk_id': f'root_substance_references_uuid:{item.uuid}',
                'document_id': document_id,
                'source_url': self._embedding_source_name(item),
                'section': 'substance_references',
                'text': '. '.join(content_parts) + '.',
                'metadata': {
                    **self._chunk_metadata(item),
                    **self._hierarchy_metadata('root', 'substance_references'),
                    'json_path': self._embedding_json_path(item, '$.substanceReferences[*]'),
                    'referenced_name': ref_name or None,
                    'referenced_id': self._get_refuuid(item) or None,
                    'approval_id': approval_id or None,
                    'linking_id': linking_id or None,
                    'references': self._embedding_references(item) or None,
                },
            }
        ]

    def specified_substance_component_to_embedding_chunks(self, item: Any) -> list[dict[str, object]]:
        """Generate embedding chunks for a SpecifiedSubstanceComponent object."""
        component_type = item.type.value if item.type else None
        substance = item.substance
        substance_name = self._get_refPname(substance) if substance else ''
        role = self._clean_text(item.role)
        amount = item.amount
        amount_text = amount.as_string() if amount else ''
        if not component_type and not substance_name and not role:
            return []

        subject = self._embedding_root_name(item)
        document_id = self._embedding_document_id(item)
        access = 'protected' if item.access else 'public'

        content_parts = [f"{subject} {access} constituent"]
        if component_type:
            content_parts.append(f"type {component_type}")
        if substance_name:
            content_parts.append(f"substance {substance_name}")
        if role:
            content_parts.append(f"role {role}")
        if amount_text:
            content_parts.append(f"amount {amount_text}")

        return [
            {
                'chunk_id': f'root_constituents_uuid:{item.uuid}',
                'document_id': document_id,
                'source_url': self._embedding_source_name(item),
                'section': 'constituents',
                'text': '. '.join(content_parts) + '.',
                'metadata': {
                    **self._chunk_metadata(item),
                    **self._hierarchy_metadata('root', 'constituents'),
                    'component_type': component_type or None,
                    'substance_name': substance_name or None,
                    'substance_id': self._get_refuuid(substance) if substance else None,
                    'role': role or None,
                },
            }
        ]

    def name_org_to_embedding_chunks(self, item: Any) -> list[dict[str, object]]:
        """Generate embedding chunks for a NameOrg object."""
        org_name = self._clean_text(item.nameOrg)
        if not org_name:
            return []

        subject = self._embedding_root_name(item)
        document_id = self._embedding_document_id(item)
        access = 'protected' if item.access else 'public'

        content = f"{subject} {access} naming organization: {org_name}."
        deprecated_date = item.deprecatedDate
        if deprecated_date:
            content += f" Deprecated since {deprecated_date}."

        return [
            {
                'chunk_id': f'root_name_orgs_uuid:{item.uuid}',
                'document_id': document_id,
                'source_url': self._embedding_source_name(item),
                'section': 'name_orgs',
                'text': content,
                'metadata': {
                    **self._chunk_metadata(item),
                    **self._hierarchy_metadata('root', 'name_orgs'),
                    'organization': org_name or None,
                    'deprecated_date': str(deprecated_date) if deprecated_date else None,
                },
            }
        ]
