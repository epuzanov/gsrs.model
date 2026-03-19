import unittest

from gsrs.model import ChemicalSubstance, Substance


class ImportTests(unittest.TestCase):
    def test_imports_exposed(self):
        self.assertIsNotNone(ChemicalSubstance)
        self.assertIsNotNone(Substance)


if __name__ == "__main__":
    unittest.main()
