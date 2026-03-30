from pydantic import Field, ConfigDict

from .mixture import Mixture
from .substance import Substance


class MixtureSubstance(Substance):
    """Mixture Substance model."""

    model_config = ConfigDict(extra='forbid')

    mixture: Mixture = Field(
        default=...,
        alias='mixture',
        title='Mixture',
        description='Mixture definition for this substance.',
    )

    def _summary_definitional_sentence(self) -> str:
        if self.mixture is None:
            return ''

        details: list[str] = []
        component_count = len(self.mixture.components or [])
        if component_count:
            label = 'component' if component_count == 1 else 'components'
            details.append(f'Mixture with {component_count} {label}')

        parent_name = self.mixture.parentSubstance.get_refPname() if self.mixture.parentSubstance else ''
        if parent_name:
            details.append(f'parent substance {parent_name}')
        if not details:
            return ''
        return f"{', '.join(details)}."

    def _substance_class_metadata(self) -> dict[str, object]:
        parent = self.mixture.parentSubstance if self.mixture else None
        return {
            'mixture_component_count': len(self.mixture.components or []) if self.mixture else 0,
            'mixture_parent_substance': parent.get_refPname() if parent else None,
            'mixture_parent_substance_id': parent.get_refuuid() if parent else None,
        }
