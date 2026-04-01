from pydantic import Field, ConfigDict
from typing import Union
from enum import Enum

from .ginas_common_sub_data import GinasCommonSubData
from .substance_reference import SubstanceReference

class Type(Enum):
    """Type model."""

    MUST_BE_PRESENT = 'MUST_BE_PRESENT'
    MAY_BE_PRESENT_ONE_OF = 'MAY_BE_PRESENT_ONE_OF'
    MAY_BE_PRESENT_ANY_OF = 'MAY_BE_PRESENT_ANY_OF'

class Component(GinasCommonSubData):
    """Component model."""

    model_config = ConfigDict(extra='forbid')

    type: Union[Type, None] = Field(
        default=None,
        alias='type',
        title='Type',
        description='Type',
    )

    substance: Union[SubstanceReference, None] = Field(
        default=None,
        alias='substance',
        title='Substance',
        description='Substance',
    )

    def to_embedding_chunks(self) -> list[dict[str, object]]:
        component_type = self.type.value if self.type else None
        substance_name = self.substance.get_refPname() if self.substance else ''
        if not component_type and not substance_name:
            return []

        subject = self._embedding_root_name()
        document_id = self._embedding_document_id()
        access = 'protected' if getattr(self, 'access', None) else 'public'

        return [
            {
                'chunk_id': f'root_components_uuid:{self.uuid}',
                'document_id': document_id,
                'source_url': self._embedding_source_name(),
                'section': 'components',
                'text': f"{subject} {access} component {component_type or 'unspecified'}: {substance_name}.".strip(),
                'metadata': {
                    **self._chunk_metadata(),
                    **self._hierarchy_metadata('root', 'components'),
                    'component_type': component_type or None,
                    'substance_name': substance_name or None,
                    'substance_id': self.substance.get_refuuid() if self.substance else None,
                },
            }
        ]
