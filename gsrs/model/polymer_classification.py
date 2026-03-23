from pydantic import Field, ConfigDict
from typing import List, Union

from .ginas_common_sub_data import GinasCommonSubData
from .substance_reference import SubstanceReference

class PolymerClassification(GinasCommonSubData):
    """Polymer Classification model."""

    model_config = ConfigDict(extra='forbid')

    polymerClass: Union[str, None] = Field(
        default=None,
        alias='polymerClass',
        title='Polymer Class',
        description='Polymer Class',
    )

    polymerGeometry: Union[str, None] = Field(
        default=None,
        alias='polymerGeometry',
        title='Polymer Geometry',
        description='Polymer Geometry',
    )

    polymerSubclass: Union[List[str], None] = Field(
        default=None,
        alias='polymerSubclass',
        title='Polymer Subclass',
        description='Polymer Subclass',
    )

    sourceType: Union[str, None] = Field(
        default=None,
        alias='sourceType',
        title='Source Type',
        description='Source Type',
    )


    parentSubstance: Union[SubstanceReference, None] = Field(
        default=None,
        alias='parentSubstance',
        title='Parent Substance',
        description='Referenced parent substance used in classifying the polymer.',
    )

    def to_embedding_chunks(self) -> list[dict[str, object]]:
        polymer_class = self._clean_text(self.polymerClass)
        polymer_geometry = self._clean_text(self.polymerGeometry)
        source_type = self._clean_text(self.sourceType)
        parent_name = self.parentSubstance.get_refPname() if self.parentSubstance else ''
        if not polymer_class and not polymer_geometry and not source_type:
            return []

        subject = self._embedding_root_name()
        document_id = self._embedding_document_id()

        content_parts = [f"{subject} polymer classification"]
        if polymer_class:
            content_parts.append(f"class {polymer_class}")
        if polymer_geometry:
            content_parts.append(f"geometry {polymer_geometry}")
        if source_type:
            content_parts.append(f"source type {source_type}")
        if parent_name:
            content_parts.append(f"parent {parent_name}")

        return [
            {
                'chunk_id': f'root_polymer_classification_uuid:{document_id}',
                'document_id': document_id,
                'source': self._embedding_source_name(),
                'section': 'polymer_classification',
                'content': '. '.join(content_parts) + '.',
                'metadata': {
                    **self._embedding_root_metadata(),
                    **self._hierarchy_metadata('root', 'polymer_classification'),
                    'polymer_class': polymer_class or None,
                    'polymer_geometry': polymer_geometry or None,
                    'source_type': source_type or None,
                    'parent_substance': parent_name or None,
                    'polymer_subclass': self.polymerSubclass or None,
                },
            }
        ]
