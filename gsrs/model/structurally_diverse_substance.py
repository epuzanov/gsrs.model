from pydantic import Field, ConfigDict

from .structurally_diverse import StructurallyDiverse
from .substance import Substance


class StructurallyDiverseSubstance(Substance):
    """Structurally Diverse Substance model."""

    model_config = ConfigDict(extra='forbid')

    structurallyDiverse: StructurallyDiverse = Field(
        default=...,
        alias='structurallyDiverse',
        title='Structurally Diverse',
        description='Structurally Diverse definition for this substance.',
    )

    def _summary_definitional_sentence(self) -> str:
        details = self.structurallyDiverse
        if details is None:
            return ''

        parts: list[str] = []
        species = self._clean_text(details.organismSpecies)
        if species:
            parts.append(f'organism species {species}')

        source_material_class = self._clean_text(details.sourceMaterialClass)
        if source_material_class:
            parts.append(f'source material class {source_material_class}')

        source_material_type = self._clean_text(details.sourceMaterialType)
        if source_material_type:
            parts.append(f'source material type {source_material_type}')

        organism_parts = self._clean_list(details.part)
        if organism_parts:
            parts.append(f'parts {self._oxford_join(organism_parts)}')
        if not parts:
            return ''
        return f"Structurally diverse material with {', '.join(parts)}."

    def _substance_class_metadata(self) -> dict[str, object]:
        details = self.structurallyDiverse
        paternal = details.hybridSpeciesPaternalOrganism if details else None
        maternal = details.hybridSpeciesMaternalOrganism if details else None
        parent = details.parentSubstance if details else None
        return {
            'source_material_class': self._clean_text(details.sourceMaterialClass if details else None) or None,
            'source_material_state': self._clean_text(details.sourceMaterialState if details else None) or None,
            'source_material_type': self._clean_text(details.sourceMaterialType if details else None) or None,
            'developmental_stage': self._clean_text(details.developmentalStage if details else None) or None,
            'fraction_name': self._clean_text(details.fractionName if details else None) or None,
            'fraction_material_type': self._clean_text(details.fractionMaterialType if details else None) or None,
            'organism_family': self._clean_text(details.organismFamily if details else None) or None,
            'organism_genus': self._clean_text(details.organismGenus if details else None) or None,
            'organism_species': self._clean_text(details.organismSpecies if details else None) or None,
            'organism_author': self._clean_text(details.organismAuthor if details else None) or None,
            'part': self._clean_list(details.part if details else None) or None,
            'part_location': self._clean_text(details.partLocation if details else None) or None,
            'infra_specific_type': self._clean_text(details.infraSpecificType if details else None) or None,
            'infra_specific_name': self._clean_text(details.infraSpecificName if details else None) or None,
            'hybrid_species_paternal_organism': paternal.get_refPname() if paternal else None,
            'hybrid_species_paternal_organism_id': paternal.get_refuuid() if paternal else None,
            'hybrid_species_maternal_organism': maternal.get_refPname() if maternal else None,
            'hybrid_species_maternal_organism_id': maternal.get_refuuid() if maternal else None,
            'parent_substance': parent.get_refPname() if parent else None,
            'parent_substance_id': parent.get_refuuid() if parent else None,
        }
