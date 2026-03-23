from pydantic import Field, ConfigDict
from typing import List

from .ginas_common_sub_data import GinasCommonSubData
from .specified_substance_component import SpecifiedSubstanceComponent

class SpecifiedSubstanceG1(GinasCommonSubData):
    """specifiedSubstance model."""

    model_config = ConfigDict(extra='forbid')

    constituents: List[SpecifiedSubstanceComponent] = Field(
        default=...,
        alias='constituents',
        title='constituents',
        description='constituents',
    )

    def to_embedding_chunks(self) -> list[dict[str, object]]:
        rows: list[dict[str, object]] = []

        for item in self.constituents or []:
            rows.extend(item.to_embedding_chunks())

        return rows
