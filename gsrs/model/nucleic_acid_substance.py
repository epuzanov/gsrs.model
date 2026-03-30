from pydantic import Field, ConfigDict
from typing import Union

from .nucleic_acid import NucleicAcid
from .substance import Substance


class NucleicAcidSubstance(Substance):
    """Nucleic Acid Substance model."""

    model_config = ConfigDict(extra='forbid')

    nucleicAcid: Union[NucleicAcid, None] = Field(
        default=None,
        alias='nucleicAcid',
        title='Nucleic Acid',
        description='Nucleic Acid definition for this substance.',
    )

    def _summary_definitional_sentence(self) -> str:
        details = self.nucleicAcid
        if details is None:
            return ''

        parts: list[str] = []
        nucleic_acid_type = self._clean_text(details.nucleicAcidType)
        if nucleic_acid_type:
            parts.append(f'Nucleic acid type {nucleic_acid_type}')

        subtypes = self._clean_list(details.nucleicAcidSubType)
        if subtypes:
            parts.append(f'subtypes {self._oxford_join(subtypes)}')

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
        if not parts:
            return ''
        return f"{', '.join(parts)}."

    def _substance_class_metadata(self) -> dict[str, object]:
        details = self.nucleicAcid
        return {
            'na_subunit_count': len(details.subunits or []) if details else 0,
            'na_linkage_count': len(details.linkages or []) if details else 0,
            'na_sugar_count': len(details.sugars or []) if details else 0,
            'nucleic_acid_type': self._clean_text(details.nucleicAcidType if details else None) or None,
            'nucleic_acid_subtypes': self._clean_list(details.nucleicAcidSubType if details else None) or None,
            'nucleic_acid_sequence_origin': self._clean_text(details.sequenceOrigin if details else None) or None,
            'nucleic_acid_sequence_type': self._clean_text(details.sequenceType if details else None) or None,
            'has_nucleic_acid_modifications': bool(details.modifications) if details else False,
        }
