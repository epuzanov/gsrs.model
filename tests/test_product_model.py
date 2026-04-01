import json
import unittest

from gsrs.model import Product, ProductManufacturer


class ProductModelTests(unittest.TestCase):
    def test_product_model_validates_nested_payload(self):
        payload = {
            'createdBy': 'test-user',
            'modifiedBy': 'test-user',
            'creationDate': 1767860682654,
            'lastModifiedDate': 1767860682654,
            'internalVersion': 0,
            'id': 9,
            'productContainer': 'Sample Container',
            'routeAdmin': 'Topical',
            'unitPresentation': 'UNIT',
            'countryCode': 'Exampleland (EXM)',
            'language': 'English',
            'shelfLife': '24',
            'storageConditions': 'Room temperature',
            'numberOfManufactureItem': '1',
            'manufacturerName': 'Example Manufacturer Ltd.',
            'manufacturerCode': 'MFG-100',
            'manufacturerCodeType': 'INTERNAL',
            'effectiveDate': '01/01/2024',
            'endDate': '01/01/2028',
            'productProvenances': [
                {
                    'createdBy': 'test-user',
                    'modifiedBy': 'test-user',
                    'creationDate': 1767860682710,
                    'lastModifiedDate': 1767860682710,
                    'internalVersion': 0,
                    'id': 9,
                    'provenance': 'SOURCE-A',
                    'productStatus': 'ACTIVE',
                    'productType': 'SAMPLE PRODUCT',
                    'applicationType': 'EXAMPLE TYPE',
                    'applicationNumber': 'APP-001',
                    'publicDomain': 'YES',
                    'isListed': 'Yes',
                    'jurisdictions': 'Exampleland (EXM)',
                    'marketingCategoryName': 'Sample Category',
                    'controlSubstanceCode': 'CTRL-1',
                    'controlSubstanceClass': 'CLASS-A',
                    'controlSubstanceSource': 'Source A',
                    'productUrl': 'https://example.test/products/source-a',
                    'productNames': [
                        {
                            'productName': 'Sample Product Name',
                            'productNameType': 'PRODUCT NAME',
                            'language': 'English',
                            'productTermAndParts': [
                                {'productTerm': 'Sample Term 1', 'productTermPart': 'Device Part'},
                                {'productTerm': 'Sample Term 2', 'productTermPart': 'Flavor Part'},
                            ],
                        }
                    ],
                    'productCodes': [
                        {
                            'productCode': 'CODE-001',
                            'productCodeType': 'INTERNAL CODE',
                            '_dailyMedUrl': 'https://example.test/dailymed/code-001',
                        }
                    ],
                    'productCompanies': [
                        {
                            'companyName': 'Example Company',
                            'companyAddress': '123 Example Street',
                            'companyCity': 'Example City',
                            'companyState': 'EX',
                            'companyZip': '12345',
                            'companyCountry': 'Exampleland (EXM)',
                            'companyRole': 'Manufacturer',
                            'companyPublicDomain': 'YES',
                            'productCompanyCodes': [
                                {'companyCode': 'COMP-001', 'companyCodeType': 'INTERNAL'}
                            ],
                        }
                    ],
                    'productDocumentations': [
                        {
                            'documentId': 'DOC-001',
                            'documentType': 'DOCUMENT TYPE',
                            'setIdVersion': 'SET-1',
                            'effectiveTime': '01/08/2026',
                            'jurisdictions': 'Exampleland (EXM)',
                        }
                    ],
                    'productIndications': [
                        {
                            'indication': 'Sample Indication',
                            'indicationText': 'Sample indication text',
                            'indicationCode': 'IND-001',
                            'indicationCodeType': 'INTERNAL',
                            'indicationGroup': 'GROUP-A',
                            'indicationSource': 'Source A',
                            'indicationSourceType': 'Source Type A',
                            'indicationSourceUrl': 'https://example.test/indications/ind-001',
                        }
                    ],
                }
            ],
            'productManufactureItems': [
                {
                    'charSize': '1',
                    'charImprintText': 'SAMPLE',
                    'charColor': 'BLACK',
                    'charFlavor': 'MINT',
                    'charShape': 'ROUND',
                    'charNumFragments': '1',
                    'dosageForm': 'Cream',
                    'dosageFormCode': 'FORM-1',
                    'dosageFormCodeType': 'INTERNAL',
                    'dosageFormNote': '10 mg/g',
                    'compositionNote': 'Sample composition',
                    'routeOfAdministration': 'TOPICAL',
                    'amount': 1,
                    'unit': 'CC',
                    'provenanceManufactureItemId': 'ITEM-001',
                    'productManufacturers': [
                        {
                            'manufacturerName': 'Example Contract Manufacturer',
                            'manufacturerRole': 'Manufacturer',
                            'manufacturerCode': 'CTR-001',
                            'manufacturerCodeType': 'INTERNAL',
                            'manufacturedItemCode': 'ITEM-CODE-001',
                            'manufacturedItemCodeType': 'INTERNAL',
                        }
                    ],
                    'productLots': [
                        {
                            'lotNo': 'LOT-001',
                            'lotSize': '1',
                            'lotType': 'SAMPLE',
                            'expiryDate': '01/08/2026',
                            'manufactureDate': '01/08/2025',
                            'productIngredients': [
                                {
                                    'applicantIngredName': 'Example Ingredient',
                                    'substanceKey': '00000000-0000-0000-0000-000000000001',
                                    'substanceKeyType': 'UUID',
                                    'basisOfStrengthSubstanceKey': '00000000-0000-0000-0000-000000000001',
                                    'basisOfStrengthSubstanceKeyType': 'UUID',
                                    'average': 1,
                                    'low': 50,
                                    'manufacturer': 'CTR-001',
                                    'ingredLotNo': 'ING-LOT-001',
                                    'ingredientType': 'ACTIVE INGREDIENT',
                                    'ingredientFunction': 'FUNCTION-A',
                                    'unit': 'MG',
                                }
                            ],
                        }
                    ],
                }
            ],
            '_self': 'https://example.test/api/v1/products/9?view=full',
        }

        product = Product.model_validate(payload)
        data = json.loads(product.model_dump_json())

        self.assertEqual(product.productProvenances[0].productNames[0].productTermAndParts[1].productTermPart, 'Flavor Part')
        self.assertEqual(product.productProvenances[0].productCodes[0].dailyMedUrl, 'https://example.test/dailymed/code-001')
        self.assertEqual(product.productManufactureItems[0].productLots[0].productIngredients[0].substanceKeyType, 'UUID')
        self.assertEqual(data['_self'], 'https://example.test/api/v1/products/9?view=full')
        self.assertEqual(data['productProvenances'][0]['productCodes'][0]['_dailyMedUrl'], 'https://example.test/dailymed/code-001')
        self.assertEqual(data['creationDate'], 1767860682654)

    def test_product_manufacturer_accepts_legacy_aliases(self):
        manufacturer = ProductManufacturer.model_validate(
            {
                'manufacturerName': 'Legacy Manufacturer',
                'manufactureItemCode': 'ABC123',
                'manufactureItemCodeType': 'LEGACY',
            }
        )
        data = manufacturer.model_dump()

        self.assertEqual(manufacturer.manufacturedItemCode, 'ABC123')
        self.assertEqual(manufacturer.manufacturedItemCodeType, 'LEGACY')
        self.assertEqual(data['manufacturedItemCode'], 'ABC123')
        self.assertEqual(data['manufacturedItemCodeType'], 'LEGACY')
        self.assertNotIn('manufactureItemCode', data)


if __name__ == '__main__':
    unittest.main()
