from pydantic import Field, ConfigDict
from typing import List

from .ginas_chemical_structure import GinasChemicalStructure
from .moiety import Moiety
from .substance import Substance, SubstanceClass


class ChemicalSubstance(Substance):
    """Chemical Substance model."""

    model_config = ConfigDict(extra='forbid')

    substanceClass: SubstanceClass = Field(
        SubstanceClass.chemical,
        alias='substanceClass',
        title='Substance Type',
        description='Substance Type',
    )
    structure: GinasChemicalStructure = Field(
        default=...,
        alias='structure',
        title='Chemical Structure',
        description='Chemical Structure definition for this substance.',
    )
    moieties: List[Moiety] = Field(
        default=...,
        alias='moieties',
        title='Chemical Moieties',
        description='Chemical Moieties',
        min_length=1,
    )

    def _summary_definitional_sentence(self) -> str:
        structure = self.structure
        if structure is None:
            return ''

        formula = self._clean_text(structure.formula)
        molecular_weight = structure.mwt
        stereochemistry = self._clean_text(structure.stereochemistry).lower()
        smiles = self._clean_text(structure.smiles)
        inchi_key = self._clean_text(structure.inchiKey)
        moieties = self._clean_list([getattr(m, 'formula', None) for m in self.moieties or []])

        descriptors: list[str] = []
        if formula:
            descriptors.append(f'Molecular formula {formula}')
        if molecular_weight is not None:
            descriptors.append(f'molecular weight {molecular_weight}')
        if stereochemistry:
            descriptors.append('racemic' if stereochemistry == 'racemic' else stereochemistry)
        if smiles and inchi_key:
            descriptors.append(f'with SMILES {smiles} and InChIKey {inchi_key}')
        elif smiles:
            descriptors.append(f'with SMILES {smiles}')
        elif inchi_key:
            descriptors.append(f'with InChIKey {inchi_key}')
        if moieties:
            descriptors.append(f'and moieties {", ".join(moieties)}')
        if not descriptors:
            return ''
        return f"{', '.join(descriptors)}."

    def _substance_class_metadata(self) -> dict[str, object]:
        structure = self.structure
        return {
            'formula': self._clean_text(structure.formula if structure else None) or None,
            'molecular_weight': structure.mwt if structure else None,
            'smiles': self._clean_text(structure.smiles if structure else None) or None,
            'inchi_key': self._clean_text(structure.inchiKey if structure else None) or None,
            'inchi': self._clean_text(structure.inchi if structure else None) or None,
            'structure_digest': self._clean_text(structure.digest if structure else None) or None,
            'structure_hash': self._clean_text(structure.hash if structure else None) or None,
            'stereochemistry': self._clean_text(structure.stereochemistry if structure else None) or None,
            'optical_activity': getattr(structure.opticalActivity, 'value', None) if structure else None,
            'atropisomerism': getattr(structure.atropisomerism, 'value', None) if structure else None,
            'stereo_centers': structure.stereoCenters if structure else None,
            'defined_stereo': structure.definedStereo if structure else None,
            'ez_centers': structure.ezCenters if structure else None,
            'charge': structure.charge if structure else None,
            'structure_references': self._embedding_references(
                structure.references if structure else None
            ) or None,
            'has_molfile': bool(structure.molfile) if structure else False,
            'moieties': self._clean_list([getattr(m, 'formula', None) for m in self.moieties or []]) or [],
        }
