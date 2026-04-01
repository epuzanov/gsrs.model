from pydantic import Field, ConfigDict
from typing import Union

from .amount import Amount
from .ginas_common_sub_data import GinasCommonSubData
from .substance_reference import SubstanceReference

class Material(GinasCommonSubData):
    """Material model for polymer starting materials or monomer inputs."""

    model_config = ConfigDict(extra='forbid')

    amount: Union[Amount, None] = Field(
        default=None,
        alias='amount',
        title='Amount',
        description='Relative amount of the starting material, often expressed as a percentage or ratio.',
    )

    monomerSubstance: Union[SubstanceReference, None] = Field(
        default=None,
        alias='monomerSubstance',
        title='Monomer Substance',
        description='Referenced substance used as a monomer or starting material.',
    )

    type: Union[str, None] = Field(
        default=None,
        alias='type',
        title='Material Role',
        description='Type or role of the starting material within the polymer description.',
    )

    defining: Union[bool, None] = Field(
        default=None,
        alias='defining',
        title='Defining',
        description='Whether this starting material is a defining element for uniquely identifying the polymer.',
    )

    def to_embedding_chunks(self) -> list[dict[str, object]]:
        material_type = self._clean_text(self.type)
        monomer_name = self.monomerSubstance.get_refPname() if self.monomerSubstance else ''
        amount_text = self.amount.as_string() if self.amount else ''
        if not material_type and not monomer_name:
            return []

        subject = self._embedding_root_name()
        document_id = self._embedding_document_id()
        access = 'protected' if getattr(self, 'access', None) else 'public'

        content_parts = [f"{subject} {access} polymer material"]
        if material_type:
            content_parts.append(f"role {material_type}")
        if monomer_name:
            content_parts.append(f"monomer {monomer_name}")
        if amount_text:
            content_parts.append(f"amount {amount_text}")

        return [
            {
                'chunk_id': f'root_materials_uuid:{self.uuid}',
                'document_id': document_id,
                'source_url': self._embedding_source_name(),
                'section': 'materials',
                'text': '. '.join(content_parts) + '.',
                'metadata': {
                    **self._chunk_metadata(),
                    **self._hierarchy_metadata('root', 'materials'),
                    'material_type': material_type or None,
                    'monomer_name': monomer_name or None,
                    'monomer_id': self.monomerSubstance.get_refuuid() if self.monomerSubstance else None,
                    'defining': bool(self.defining),
                },
            }
        ]
