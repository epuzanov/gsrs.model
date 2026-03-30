from pydantic import Field, ConfigDict
from typing import Union

from .protein import Protein
from .substance import Substance


class ProteinSubstance(Substance):
    """Protein Substance model."""

    model_config = ConfigDict(extra='forbid')

    protein: Union[Protein, None] = Field(
        default=None,
        alias='protein',
        title='Protein',
        description='Protein definition for this substance.',
    )

    def _summary_definitional_sentence(self) -> str:
        details = self.protein
        if details is None:
            return ''

        parts: list[str] = []
        protein_type = self._clean_text(details.proteinType)
        if protein_type:
            parts.append(f'Protein type {protein_type}')

        protein_subtypes = self._clean_list(details.proteinSubType)
        if protein_subtypes:
            parts.append(f'subtypes {self._oxford_join(protein_subtypes)}')

        subunit_count = len(details.subunits or [])
        if subunit_count:
            label = 'subunit' if subunit_count == 1 else 'subunits'
            parts.append(f'{subunit_count} {label}')

        sequence_origin = self._clean_text(details.sequenceOrigin)
        if sequence_origin:
            parts.append(f'sequence origin {sequence_origin}')

        sequence_type = self._clean_text(details.sequenceType)
        if sequence_type:
            parts.append(f'sequence type {sequence_type}')

        glycosylation_type = self._clean_text(details.glycosylation.glycosylationType if details.glycosylation else None)
        if glycosylation_type:
            parts.append(f'glycosylation type {glycosylation_type}')
        if not parts:
            return ''
        return f"{', '.join(parts)}."

    def _substance_class_metadata(self) -> dict[str, object]:
        details = self.protein
        glycosylation = details.glycosylation if details else None
        return {
            'protein_subunit_count': len(details.subunits or []) if details else 0,
            'protein_disulfide_link_count': len(details.disulfideLinks or []) if details else 0,
            'protein_other_link_count': len(details.otherLinks or []) if details else 0,
            'protein_type': self._clean_text(details.proteinType if details else None) or None,
            'protein_subtypes': self._clean_list(details.proteinSubType if details else None) or None,
            'protein_sequence_origin': self._clean_text(details.sequenceOrigin if details else None) or None,
            'protein_sequence_type': self._clean_text(details.sequenceType if details else None) or None,
            'glycosylation_type': self._clean_text(glycosylation.glycosylationType if glycosylation else None) or None,
            'c_sites_count': len(glycosylation.CGlycosylationSites or []) if glycosylation else 0,
            'n_sites_count': len(glycosylation.NGlycosylationSites or []) if glycosylation else 0,
            'o_sites_count': len(glycosylation.OGlycosylationSites or []) if glycosylation else 0,
            'has_protein_modifications': bool(details.modifications) if details else False,
        }
