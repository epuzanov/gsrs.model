import json
import unittest

from pydantic import AnyUrl

from gsrs.model import Amount, Substance
from gsrs.model.substance import SubstanceClass


class JsonSerializationTests(unittest.TestCase):
    def test_model_dump_json_excludes_nulls_by_default(self):
        amount = Amount(type="MOL RATIO", average=1.0)
        data = json.loads(amount.model_dump_json())

        self.assertNotIn("high", data)
        self.assertEqual(data["type"], "MOL RATIO")

    def test_substance_dump_json_excludes_nulls_by_default(self):
        substance = Substance.model_construct(
            substanceClass=SubstanceClass.concept,
            names=[],
            references=[],
            version="1",
            approved=None,
            selfLink=AnyUrl("https://example.test/substances/1"),
        )
        data = json.loads(substance.model_dump_json())

        self.assertNotIn("approved", data)
        self.assertEqual(data["substanceClass"], "concept")
        self.assertEqual(data["_self"], "https://example.test/substances/1")
        self.assertNotIn("selfLink", data)


if __name__ == "__main__":
    unittest.main()
