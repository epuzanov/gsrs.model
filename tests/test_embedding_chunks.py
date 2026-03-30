import unittest

from gsrs.model import ChemicalSubstance, Code, Substance


class EmbeddingChunkTests(unittest.TestCase):
    def test_subelement_document_id_uses_parent_uuid(self):
        substance = Substance.model_validate(
            {
                'substanceClass': 'concept',
                'uuid': '11111111-1111-1111-1111-111111111111',
                'approvalID': 'APP-1',
                'names': [{'name': 'Example Concept', 'type': 'cn', 'languages': ['en']}],
                'references': [{'docType': 'SYSTEM'}],
                '_self': 'https://example.test/gsrs',
                'version': '1',
            }
        )
        substance._assign_parent(substance, substance)
        chunk = substance.names[0].to_embedding_chunks()[0]
        self.assertEqual(chunk['document_id'], '11111111-1111-1111-1111-111111111111')
        self.assertEqual(chunk['chunk_id'], f'root_names_uuid:{substance.names[0].uuid}')
        self.assertEqual(chunk['section'], 'names')
        self.assertEqual(chunk['metadata']['hierarchy'], ['root', 'names'])
        self.assertEqual(chunk['metadata']['hierarchy_path'], 'root > names')
        self.assertEqual(chunk['metadata']['hierarchy_level'], 2)

    def test_substance_to_embedding_chunks_returns_root_and_subelements(self):
        substance = Substance.model_validate(
            {
                'substanceClass': 'concept',
                'uuid': '11111111-1111-1111-1111-111111111111',
                'approvalID': 'APP-1',
                'names': [
                    {
                        'name': 'Example Concept',
                        'type': 'cn',
                        'languages': ['en'],
                        'preferred': True,
                        'references': ['aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'],
                    }
                ],
                'codes': [
                    {
                        'code': 'ABC-123',
                        'codeSystem': 'CAS',
                        'references': ['bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb'],
                    }
                ],
                'properties': [{'name': 'Molecular Weight'}],
                'relationships': [{'type': 'ACTIVE MOIETY', 'relatedSubstance': {'name': 'Related', 'refuuid': '33333333-3333-3333-3333-333333333333'}}],
                'notes': [{'note': 'Important note'}],
                'references': [
                    {
                        'uuid': 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
                        'docType': 'SYSTEM',
                        'citation': 'generated',
                    },
                    {
                        'uuid': 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb',
                        'docType': 'MANUAL',
                        'citation': 'registry import',
                    },
                ],
                'modifications': {'agentModifications': [{'agentModificationType': 'CHEMICAL', 'agentSubstance': {'refuuid': '22222222-2222-2222-2222-222222222222'}}]},
                '_self': 'https://example.test/gsrs',
                'version': '1',
            }
        )
        chunks = substance.to_embedding_chunks()
        sections = [chunk['section'] for chunk in chunks]
        self.assertIn('root', sections)
        self.assertIn('names', sections)
        self.assertIn('codes', sections)
        self.assertIn('properties', sections)
        self.assertIn('relationships', sections)
        self.assertIn('notes', sections)
        self.assertIn('references', sections)
        self.assertIn('agentModifications', sections)
        mod_chunk = next(chunk for chunk in chunks if chunk['section'] == 'agentModifications')
        self.assertEqual(mod_chunk['metadata']['hierarchy'], ['root', 'modifications', 'agentModifications'])
        self.assertEqual(chunks[0]['metadata']['approval_id'], 'APP-1')
        self.assertEqual(chunks[0]['metadata']['name_count'], 1)
        self.assertEqual(chunks[0]['source_url'], 'https://example.test/gsrs')
        self.assertEqual(chunks[0]['metadata']['hierarchy'], ['root'])
        self.assertEqual(chunks[0]['metadata']['json_path'], '$')
        name_chunk = next(chunk for chunk in chunks if chunk['section'] == 'names')
        self.assertEqual(name_chunk['metadata']['references'], ['SYSTEM: generated'])
        self.assertNotIn('reference_ids', name_chunk['metadata'])
        code_chunk = next(chunk for chunk in chunks if chunk['section'] == 'codes')
        self.assertEqual(code_chunk['metadata']['references'], ['MANUAL: registry import'])
        self.assertNotIn('reference_ids', code_chunk['metadata'])

    def test_classification_code_adds_classification_chunk(self):
        substance = Substance.model_validate(
            {
                'substanceClass': 'concept',
                'uuid': '11111111-1111-1111-1111-111111111111',
                'approvalID': 'APP-1',
                'names': [{'name': 'Example Concept', 'type': 'cn', 'languages': ['en']}],
                'references': [{'docType': 'SYSTEM'}],
                '_self': 'https://example.test/gsrs',
                'version': '1',
            }
        )
        code = Code.model_validate(
            {
                'code': 'ABC-123',
                'codeSystem': 'ATC',
                '_isClassification': True,
                'comments': 'Level 1|Level 2|Level 3',
            }
        )
        code._set_parent(substance)

        chunks = code.to_embedding_chunks()

        self.assertEqual(len(chunks), 2)
        class_chunk = next(chunk for chunk in chunks if chunk['section'] == 'classifications')
        self.assertEqual(class_chunk['chunk_id'], f'root_classifications_uuid:{code.uuid}')
        self.assertEqual(class_chunk['text'], 'Example Concept classification in ATC: Level 1 > Level 2 > Level 3.')
        self.assertEqual(class_chunk['metadata']['classification_hierarchy'], ['Level 1', 'Level 2', 'Level 3'])
        self.assertEqual(class_chunk['metadata']['hierarchy'], ['root', 'classifications'])
        self.assertEqual(class_chunk['metadata']['json_path'], '$.codes[*]')

    def test_code_chunk_matches_adapter_style(self):
        substance = Substance.model_validate(
            {
                'substanceClass': 'concept',
                'uuid': '11111111-1111-1111-1111-111111111111',
                'approvalID': 'APP-1',
                'names': [{'name': 'Example Concept', 'type': 'cn', 'languages': ['en']}],
                'references': [{'docType': 'SYSTEM'}],
                '_self': 'https://example.test/gsrs',
                'version': '1',
            }
        )
        code = Code.model_validate({'code': 'ABC-123', 'codeSystem': 'CAS'})
        code._set_parent(substance)
        chunk = code.to_embedding_chunks()[0]
        self.assertEqual(chunk['text'], 'Example Concept identifier in CAS: ABC-123.')
        self.assertEqual(chunk['document_id'], '11111111-1111-1111-1111-111111111111')
        self.assertEqual(chunk['chunk_id'], f'root_codes_uuid:{code.uuid}')
        self.assertEqual(chunk['source_url'], 'https://example.test/gsrs')
        self.assertEqual(chunk['metadata']['hierarchy'], ['root', 'codes'])
        self.assertEqual(chunk['metadata']['json_path'], '$.codes[*]')


    def test_embedding_root_name_falls_back_to_substance_uuid(self):
        code = Code.model_validate({'code': 'ABC-123', 'codeSystem': 'CAS'})
        parent = Substance.model_construct(
            substanceClass='concept',
            uuid='11111111-1111-1111-1111-111111111111',
            names=[],
            references=[],
            version='1',
        )
        code._set_parent(parent)
        chunk = code.to_embedding_chunks()[0]
        self.assertEqual(chunk['text'], 'Substance 11111111-1111-1111-1111-111111111111 identifier in CAS: ABC-123.')

    def test_chemical_substance_adds_class_summary_chunk(self):
        substance = ChemicalSubstance.model_validate(
            {
                'substanceClass': 'chemical',
                'uuid': '11111111-1111-1111-1111-111111111111',
                'names': [{'name': 'Example Chemical', 'type': 'cn', 'languages': ['en']}],
                'references': [
                    {
                        'uuid': 'cccccccc-cccc-cccc-cccc-cccccccccccc',
                        'docType': 'SYSTEM',
                        'citation': 'structure source',
                    }
                ],
                '_self': 'https://example.test/gsrs',
                'version': '1',
                'structure': {
                    'stereochemistry': 'ACHIRAL',
                    'opticalActivity': 'NONE',
                    'atropisomerism': 'No',
                    'formula': 'H2O',
                    'references': ['cccccccc-cccc-cccc-cccc-cccccccccccc'],
                },
                'moieties': [{'stereochemistry': 'ACHIRAL', 'opticalActivity': 'NONE', 'atropisomerism': 'No'}],
            }
        )
        class_chunks = [chunk for chunk in substance.to_embedding_chunks() if chunk['section'] == 'structure']
        self.assertEqual(len(class_chunks), 1)
        self.assertIn('Formula H2O.', class_chunks[0]['text'])
        self.assertEqual(class_chunks[0]['metadata']['hierarchy'], ['root', 'structure'])
        self.assertEqual(class_chunks[0]['metadata']['json_path'], '$.structure')
        self.assertEqual(class_chunks[0]['metadata']['references'], ['SYSTEM: structure source'])
        self.assertNotIn('reference_ids', class_chunks[0]['metadata'])


if __name__ == '__main__':
    unittest.main()
