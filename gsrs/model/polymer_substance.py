from pydantic import Field, ConfigDict
from typing import Union

from .polymer import Polymer
from .substance import Substance


class PolymerSubstance(Substance):
    """Polymer Substance model."""

    model_config = ConfigDict(extra='forbid')

    polymer: Union[Polymer, None] = Field(
        default=None,
        alias='polymer',
        title='Polymer',
        description='Polymer definition for this substance.',
    )

    def _summary_definitional_sentence(self) -> str:
        details = self.polymer
        if details is None:
            return ''

        classification = details.classification
        parts: list[str] = []

        polymer_class = self._clean_text(classification.polymerClass if classification else None)
        if polymer_class:
            parts.append(f'Polymer class {polymer_class}')

        monomer_count = len(details.monomers or [])
        if monomer_count:
            label = 'monomer' if monomer_count == 1 else 'monomers'
            parts.append(f'{monomer_count} {label}')

        structural_unit_count = len(details.structuralUnits or [])
        if structural_unit_count:
            label = 'structural unit' if structural_unit_count == 1 else 'structural units'
            parts.append(f'{structural_unit_count} {label}')

        polymer_geometry = self._clean_text(classification.polymerGeometry if classification else None)
        if polymer_geometry:
            parts.append(f'geometry {polymer_geometry}')
        if not parts:
            return ''
        return f"{', '.join(parts)}."

    def _substance_class_metadata(self) -> dict[str, object]:
        details = self.polymer
        classification = details.classification if details else None
        parent = classification.parentSubstance if classification else None
        return {
            'polymer_monomer_count': len(details.monomers or []) if details else 0,
            'polymer_structural_unit_count': len(details.structuralUnits or []) if details else 0,
            'polymer_class': self._clean_text(classification.polymerClass if classification else None) or None,
            'polymer_geometry': self._clean_text(classification.polymerGeometry if classification else None) or None,
            'polymer_subclass': self._clean_list(classification.polymerSubclass if classification else None) or None,
            'polymer_source_type': self._clean_text(classification.sourceType if classification else None) or None,
            'polymer_parent_substance': parent.get_refPname() if parent else None,
            'polymer_parent_substance_id': parent.get_refuuid() if parent else None,
            'has_display_structure': bool(details.displayStructure) if details else False,
            'has_idealized_structure': bool(details.idealizedStructure) if details else False,
        }
