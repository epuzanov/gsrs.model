from pydantic import Field, ConfigDict
from typing import List, Union

from .ginas_chemical_structure import GinasChemicalStructure
from .ginas_common_sub_data import GinasCommonSubData
from .material import Material
from .polymer_classification import PolymerClassification
from .unit import Unit

class Polymer(GinasCommonSubData):
    """Polymer model capturing properties specific to substances that are polymers."""

    model_config = ConfigDict(extra='forbid')

    classification: Union[PolymerClassification, None] = Field(
        default=None,
        alias='classification',
        title='Classification',
        description='Classification of the polymer, including high-level polymer category or subtype.',
    )

    displayStructure: Union[GinasChemicalStructure, None] = Field(
        default=None,
        alias='displayStructure',
        title='Display Structure',
        description='Representative displayed structure for the polymer.',
    )

    idealizedStructure: Union[GinasChemicalStructure, None] = Field(
        default=None,
        alias='idealizedStructure',
        title='Idealized Structure',
        description='Idealized structural representation of the polymer.',
    )

    monomers: Union[List[Material], None] = Field(
        default=None,
        alias='monomers',
        title='Starting Materials',
        description='Starting materials or monomers used in synthesis of the polymer.',
    )

    structuralUnits: Union[List[Unit], None] = Field(
        default=None,
        alias='structuralUnits',
        title='Structural Units',
        description='Structural repeat units that define the polymer and their configuration.',
    )

    def to_embedding_chunks(self) -> list[dict[str, object]]:
        rows: list[dict[str, object]] = []

        if self.classification:
            rows.extend(self.classification.to_embedding_chunks())
        for item in self.monomers or []:
            rows.extend(item.to_embedding_chunks())
        for item in self.structuralUnits or []:
            rows.extend(item.to_embedding_chunks())

        return rows
