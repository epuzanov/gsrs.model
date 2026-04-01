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
        property_type = self._clean_text(self.propertyType)
        value_type = self._clean_text(self.type)
        referenced_name = self.referencedSubstance.get_refPname() if self.referencedSubstance else ''
        referenced_id = self.referencedSubstance.get_refuuid() if self.referencedSubstance else ''
        parameter_names = self._clean_list([parameter.name for parameter in (self.parameters or []) if parameter.name])
        if not prop_name and not value_text:
            return []

        subject = self._embedding_root_name()
        document_id = self._embedding_document_id()
        access = 'protected' if getattr(self, 'access', None) else 'public'

        parts = [f'{subject} {access} property {prop_name}.']
        if property_type:
            parts.append(f'Property type {property_type}.')
        if value_type:
            parts.append(f'Value type {value_type}.')
        if value_text:
            parts.append(f'Value {value_text}.')

        return [
            {
                'chunk_id': f'root_properties_uuid:{self.uuid}',
                'document_id': document_id,
                'source_url': self._embedding_source_name(),
                'section': 'properties',
                'text': ' '.join(parts),
                'metadata': {
                    **self._chunk_metadata(),
                    **self._hierarchy_metadata('root', 'properties'),
                    'json_path': self._embedding_json_path('$.properties[*]'),
                    'property_name': prop_name or None,
                    'property_type': property_type or None,
                    'value_type': value_type or None,
                    'value_text': value_text or None,
                    'defining': bool(self.defining),
                    'referenced_name': referenced_name or None,
                    'referenced_id': referenced_id or None,
                    'parameter_names': parameter_names or None,
                    'references': self._embedding_references() or None,
                },
            }
        ]
