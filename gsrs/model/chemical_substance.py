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

    def _class_summary_chunks(self) -> list[dict[str, object]]:
        document_id = self._clean_text(self.uuid)
        formula = self._clean_text(self.structure.formula if self.structure else None)
        molecular_weight = self.structure.mwt if self.structure else None
        smiles = self._clean_text(self.structure.smiles if self.structure else None)
        inchi_key = self._clean_text(self.structure.inchiKey if self.structure else None)
        inchi = self._clean_text(self.structure.inchi if self.structure else None)
        stereochemistry = self._clean_text(self.structure.stereochemistry if self.structure else None)
        optical_activity = self._clean_text(self.structure.opticalActivity if self.structure else None)
        atropisomerism = self._clean_text(self.structure.atropisomerism if self.structure else None)
        moiety_count = len(self.moieties or [])
        parts = [f'{self._stable_name()} belongs to substance class chemical.']
        if formula:
            parts.append(f'Formula {formula}.')
        if molecular_weight is not None:
            parts.append(f'Molecular weight {molecular_weight}.')
        if smiles:
            parts.append(f'SMILES {smiles}.')
        if inchi_key:
            parts.append(f'InChIKey {inchi_key}.')
        if stereochemistry:
            parts.append(f'Stereochemistry {stereochemistry}.')
        if optical_activity:
            parts.append(f'Optical activity {optical_activity}.')
        if moiety_count:
            parts.append(f'Moiety count {moiety_count}.')

        return [
            {
                'chunk_id': f'root_structure_uuid:{document_id}',
                'document_id': document_id,
                'source_url': self._embedding_source_name(),
                'section': 'structure',
                'text': ' '.join(parts),
                'metadata': {
                    **self._chunk_metadata(self),
                    **self._hierarchy_metadata('root', 'structure'),
                    'json_path': '$.structure',
                    'substance_class': 'chemical',
                    'formula': formula or None,
                    'molecular_weight': molecular_weight,
                    'smiles': smiles or None,
                    'inchi_key': inchi_key or None,
                    'inchi': inchi or None,
                    'structure_digest': self._clean_text(self.structure.digest if self.structure else None) or None,
                    'structure_hash': self._clean_text(self.structure.hash if self.structure else None) or None,
                    'stereochemistry': stereochemistry or None,
                    'optical_activity': optical_activity or None,
                    'atropisomerism': atropisomerism or None,
                    'stereo_centers': self.structure.stereoCenters if self.structure else None,
                    'defined_stereo': self.structure.definedStereo if self.structure else None,
                    'ez_centers': self.structure.ezCenters if self.structure else None,
                    'charge': self.structure.charge if self.structure else None,
                    'references': self._embedding_references(
                        self.structure.references if self.structure else None
                    ) or None,
                    'has_molfile': bool(self.structure.molfile) if self.structure else False,
                    'moiety_count': moiety_count,
                },
            }
        ]
