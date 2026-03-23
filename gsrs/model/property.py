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
        default=...,
        alias='name',
        title='Property Name',
        description='Property Name',
    )
    type: Union[str, None] = Field(
        default=None,
        alias='type',
        title='Value Type',
        description='Value Type',
    )
    propertyType: Union[str, None] = Field(
        default=None,
        alias='propertyType',
        title='Property Type',
        description='Property Type',
    )
    value: Union[Amount, None] = Field(
        default=None,
        alias='value',
        title='Amount',
        description='Amount',
    )
    referencedSubstance: Union[SubstanceReference, None] = Field(
        default=None,
        alias='referencedSubstance',
        title='Referenced Substance',
        description='Referenced Substance',
    )
    defining: Union[bool, None] = Field(
        default=None,
        alias='defining',
        title='Defining',
        description='Defining',
    )
    parameters: Union[List[Parameter], None] = Field(
        default=None,
        alias='parameters',
        title='Parameters',
        description='Parameters',
    )

    def _render_property_value(self) -> str:
        parts: list[str] = []
        value_text = self.value.as_string() if self.value else ''
        if value_text:
            parts.append(value_text)
        ref_name = self.referencedSubstance.get_refPname() if self.referencedSubstance else ''
        if ref_name:
            parts.append(f'referenced substance {ref_name}')
        param_bits = []
        for parameter in self.parameters or []:
            pname = self._clean_text(parameter.name)
            ptype = self._clean_text(parameter.type)
            pvalue = parameter.value.as_string() if parameter.value else ''
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
