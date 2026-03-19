import unittest

from gsrs.model import ChemicalSubstance, Substance


class SubstanceDispatchTests(unittest.TestCase):
    def test_substance_init_dispatches_to_chemical_subclass(self):
        payload = {
            "substanceClass": "chemical",
            "names": [
                {
                    "name": "Example Chemical",
                    "type": "cn",
                    "languages": ["en"],
                    "nameJurisdiction": [],
                    "nameOrgs": [],
                    "references": [],
                    "access": [],
                }
            ],
            "references": [
                {
                    "docType": "SYSTEM",
                    "citation": "generated",
                    "publicDomain": True,
                    "tags": [],
                    "access": [],
                }
            ],
            "version": "1",
            "structure": {
                "stereochemistry": "ACHIRAL",
                "opticalActivity": "NONE",
                "atropisomerism": "No",
            },
            "moieties": [
                {
                    "stereochemistry": "ACHIRAL",
                    "opticalActivity": "NONE",
                    "atropisomerism": "No",
                }
            ],
        }

        model = Substance(**payload)

        self.assertIsInstance(model, ChemicalSubstance)
        self.assertEqual(model.substanceClass.value, "chemical")

    def test_substance_model_validate_dispatches_to_base_for_concept(self):
        payload = {
            "substanceClass": "concept",
            "names": [
                {
                    "name": "Example Concept",
                    "type": "cn",
                    "languages": ["en"],
                    "nameJurisdiction": [],
                    "nameOrgs": [],
                    "references": [],
                    "access": [],
                }
            ],
            "references": [
                {
                    "docType": "SYSTEM",
                    "citation": "generated",
                    "publicDomain": True,
                    "tags": [],
                    "access": [],
                }
            ],
            "version": "1",
        }

        model = Substance.model_validate(payload)

        self.assertIs(type(model), Substance)
        self.assertEqual(model.substanceClass.value, "concept")


if __name__ == "__main__":
    unittest.main()
