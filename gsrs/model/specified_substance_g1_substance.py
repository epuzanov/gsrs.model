from pydantic import Field, ConfigDict

from .specified_substance_g1 import SpecifiedSubstanceG1
from .substance import Substance


class SpecifiedSubstanceG1Substance(Substance):
    """Specified Substance model."""

    model_config = ConfigDict(extra='forbid')

    specifiedSubstance: SpecifiedSubstanceG1 = Field(
        default=...,
        alias='specifiedSubstance',
        title='specifiedSubstance',
        description='Specified Substance definition for this substance.',
    )

    def _summary_definitional_sentence(self) -> str:
        if self.specifiedSubstance is None:
            return ''
        constituent_count = len(self.specifiedSubstance.constituents or [])
        if not constituent_count:
            return ''
        label = 'constituent' if constituent_count == 1 else 'constituents'
        return f'Specified substance with {constituent_count} {label}.'

    def _substance_class_metadata(self) -> dict[str, object]:
        return {
            'specified_substance_constituent_count': len(
                self.specifiedSubstance.constituents or []
            ) if self.specifiedSubstance else 0,
        }
