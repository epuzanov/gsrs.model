from pydantic import Field, ConfigDict
from typing import List, Union

from .amount import Amount
from .ginas_common_sub_data import GinasCommonSubData
from .parameter import Parameter
from .substance_reference import SubstanceReference

class Property(GinasCommonSubData):
    """Property model."""

    model_config = ConfigDict(extra='forbid')

    name: str = Field(
        ...,
        alias='name',
        title='Property Name',
        description='Property Name',
        element_property=True,
    )
    type: Union[str, None] = Field(
        None,
        alias='type',
        title='Value Type',
        description='Value Type',
        element_property=True,
    )
    propertyType: Union[str, None] = Field(
        None,
        alias='propertyType',
        title='Property Type',
        description='Property Type',
        element_property=True,
    )
    value: Union[Amount, None] = Field(
        None,
        alias='value',
        title='Amount',
        description='Amount',
        element_property=True,
    )
    referencedSubstance: Union[SubstanceReference, None] = Field(
        None,
        alias='referencedSubstance',
        title='Referenced Substance',
        description='Referenced Substance',
        element_property=True,
    )
    defining: Union[bool, None] = Field(
        None,
        alias='defining',
        title='Defining',
        description='Defining',
        element_property=True,
    )
    parameters: Union[List[Parameter], None] = Field(
        None,
        alias='parameters',
        title='Parameters',
        description='Parameters',
        element_property=True,
    )

    def _render_property_value(self) -> str:
        parts: list[str] = []
        value_text = self._render_amount(self.value)
        if value_text:
            parts.append(value_text)
        ref_name = self._pick_substance_ref_name(self.referencedSubstance)
        if ref_name:
            parts.append(f'referenced substance {ref_name}')
        param_bits = []
        for parameter in self.parameters or []:
            pname = self._clean_text(parameter.name)
            ptype = self._clean_text(parameter.type)
            pvalue = self._render_amount(parameter.value)
            bit = pname
            if ptype:
                bit = f'{bit} ({ptype})' if bit else ptype
            if pvalue:
                bit = f'{bit}: {pvalue}' if bit else pvalue
            if bit:
                param_bits.append(bit)
        if param_bits:
            parts.append('parameters ' + '; '.join(param_bits))
        return '. '.join(parts).strip('. ')

    def to_embedding_chunks(self) -> list[dict[str, object]]:
        prop_name = self._clean_text(self.name)
        value_text = self._render_property_value()
        if not prop_name and not value_text:
            return []

        subject = self._embedding_root_name()
        document_id = self._embedding_document_id()

        return [
            {
                'chunk_id': f'root_properties_uuid:{document_id}',
                'document_id': document_id,
                'source': self._embedding_source_name(),
                'section': 'properties',
                'content': f"{subject} property {prop_name}: {value_text}.".strip(),
                'metadata': {
                    **self._embedding_root_metadata(),
                    **self._hierarchy_metadata('root', 'properties'),
                    'property_name': prop_name or None,
                    'property_type': self._clean_text(self.propertyType) or None,
                    'defining': bool(self.defining),
                },
            }
        ]
