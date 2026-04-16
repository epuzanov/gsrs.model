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
            access=[],
            names=[],
            references=[],
            version="1",
            approved=None,
            selfLink=AnyUrl("https://example.test/substances/1"),
        )
        data = json.loads(substance.model_dump_json())

        self.assertNotIn("approved", data)
        self.assertEqual(data["substanceClass"], "concept")
        self.assertEqual(data["names"], [])
        self.assertEqual(data["references"], [])
        self.assertEqual(data["_self"], "https://example.test/substances/1")
        self.assertNotIn("selfLink", data)

    def test_substance_dump_excludes_non_public_nested_elements(self):
        substance = Substance.model_validate(
            {
                "substanceClass": "concept",
                "access": [],
                "names": [
                    {
                        "name": "Public Name",
                        "type": "cn",
                        "languages": ["en"],
                        "nameJurisdiction": [],
                        "nameOrgs": [],
                        "references": [],
                        "access": [],
                    },
                    {
                        "name": "Private Name",
                        "type": "cn",
                        "languages": ["en"],
                        "nameJurisdiction": [],
                        "nameOrgs": [],
                        "references": [],
                        "access": ["protected"],
                    },
                ],
                "codes": [
                    {
                        "code": "PUBLIC-CODE",
                        "codeSystem": "SYS",
                        "access": [],
                    },
                    {
                        "code": "PRIVATE-CODE",
                        "codeSystem": "SYS",
                        "access": ["protected"],
                    },
                    {
                        "code": "UNSET-CODE",
                        "codeSystem": "SYS",
                    },
                ],
                "notes": [
                    {
                        "note": "Visible note",
                        "access": [],
                    },
                    {
                        "note": "Hidden note",
                        "access": ["protected"],
                    },
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
        )

        data = substance.model_dump(exclude_non_public=True)

        self.assertEqual([item["name"] for item in data["names"]], ["Public Name"])
        self.assertEqual([item["code"] for item in data["codes"]], ["PUBLIC-CODE", "UNSET-CODE"])
        self.assertEqual([item["note"] for item in data["notes"]], ["Visible note"])

    def test_substance_dump_preserves_empty_lists_with_exclude_non_public(self):
        substance = Substance.model_validate(
            {
                "substanceClass": "concept",
                "access": [],
                "names": [
                    {
                        "name": "Public Name",
                        "type": "cn",
                        "languages": ["en"],
                        "nameJurisdiction": [],
                        "nameOrgs": [],
                        "references": [],
                        "access": [],
                    }
                ],
                "codes": [],
                "notes": [],
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
        )

        data = substance.model_dump(exclude_non_public=True)

        self.assertIn("codes", data)
        self.assertIn("notes", data)
        self.assertIn("references", data["names"][0])
        self.assertEqual(data["codes"], [])
        self.assertEqual(data["notes"], [])
        self.assertEqual(data["names"][0]["references"], [])

    def test_substance_dump_json_excludes_non_public_nested_elements(self):
        substance = Substance.model_validate(
            {
                "substanceClass": "concept",
                "access": [],
                "names": [
                    {
                        "name": "Public Name",
                        "type": "cn",
                        "languages": ["en"],
                        "nameJurisdiction": [],
                        "nameOrgs": [],
                        "references": [],
                        "access": [],
                    },
                    {
                        "name": "Private Name",
                        "type": "cn",
                        "languages": ["en"],
                        "nameJurisdiction": [],
                        "nameOrgs": [],
                        "references": [],
                        "access": ["protected"],
                    },
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
        )

        data = json.loads(substance.model_dump_json(exclude_non_public=True))

        self.assertEqual([item["name"] for item in data["names"]], ["Public Name"])
        self.assertEqual(data["access"], [])
        self.assertEqual(data["names"][0]["references"], [])

    def test_substance_dump_json_preserves_empty_lists_with_exclude_non_public(self):
        substance = Substance.model_validate(
            {
                "substanceClass": "concept",
                "access": [],
                "names": [
                    {
                        "name": "Public Name",
                        "type": "cn",
                        "languages": ["en"],
                        "nameJurisdiction": [],
                        "nameOrgs": [],
                        "references": [],
                        "access": [],
                    }
                ],
                "codes": [],
                "notes": [],
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
        )

        data = json.loads(substance.model_dump_json(exclude_non_public=True))

        self.assertIn("codes", data)
        self.assertIn("notes", data)
        self.assertIn("references", data["names"][0])
        self.assertEqual(data["codes"], [])
        self.assertEqual(data["notes"], [])
        self.assertEqual(data["names"][0]["references"], [])


if __name__ == "__main__":
    unittest.main()
