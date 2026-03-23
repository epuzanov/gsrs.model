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
                '_self': 'gsrs',
                'version': '1',
            }
        )
        substance._assign_parent_context(substance, substance.uuid, substance._stable_name(), substance.selfLink)
        chunk = substance.names[0].to_embedding_chunks()[0]
        self.assertEqual(chunk['document_id'], '11111111-1111-1111-1111-111111111111')
        self.assertEqual(chunk['chunk_id'], 'root_names_uuid:11111111-1111-1111-1111-111111111111')
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
                'names': [{'name': 'Example Concept', 'type': 'cn', 'languages': ['en'], 'preferred': True}],
                'codes': [{'code': 'ABC-123', 'codeSystem': 'CAS'}],
                'properties': [{'name': 'Molecular Weight'}],
                'relationships': [{'type': 'ACTIVE MOIETY', 'relatedSubstance': {'name': 'Related'}}],
                'notes': [{'note': 'Important note'}],
                'references': [{'docType': 'SYSTEM', 'citation': 'generated'}],
                'modifications': {'agentModifications': [{'agentModificationType': 'CHEMICAL', 'agentSubstance': {'refuuid': '22222222-2222-2222-2222-222222222222'}}]},
                '_self': 'gsrs',
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
        self.assertIn('raw_json', sections)
        self.assertNotIn('approval_id', chunks[0]['metadata'])
        self.assertEqual(chunks[0]['source'], 'gsrs')
        self.assertEqual(chunks[0]['metadata']['hierarchy'], ['root'])

    def test_classification_code_adds_classification_chunk(self):
        substance = Substance.model_validate(
            {
                'substanceClass': 'concept',
                'uuid': '11111111-1111-1111-1111-111111111111',
                'approvalID': 'APP-1',
                'names': [{'name': 'Example Concept', 'type': 'cn', 'languages': ['en']}],
                'references': [{'docType': 'SYSTEM'}],
                '_self': 'gsrs',
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
        code._set_parent_context(substance.uuid, substance._stable_name(), substance.selfLink)

        chunks = code.to_embedding_chunks()

        self.assertEqual(len(chunks), 2)
        class_chunk = next(chunk for chunk in chunks if chunk['section'] == 'classification')
        self.assertEqual(class_chunk['chunk_id'], 'root_classification_uuid:11111111-1111-1111-1111-111111111111')
        self.assertEqual(class_chunk['content'], 'Example Concept classification in ATC: Level 1 > Level 2 > Level 3.')
        self.assertEqual(class_chunk['metadata']['classification_hierarchy'], ['Level 1', 'Level 2', 'Level 3'])
        self.assertEqual(class_chunk['metadata']['hierarchy'], ['root', 'classification'])

    def test_code_chunk_matches_adapter_style(self):
        substance = Substance.model_validate(
            {
                'substanceClass': 'concept',
                'uuid': '11111111-1111-1111-1111-111111111111',
                'approvalID': 'APP-1',
                'names': [{'name': 'Example Concept', 'type': 'cn', 'languages': ['en']}],
                'references': [{'docType': 'SYSTEM'}],
                '_self': 'gsrs',
                'version': '1',
            }
        )
        code = Code.model_validate({'code': 'ABC-123', 'codeSystem': 'CAS'})
        code._set_parent_context(substance.uuid, substance._stable_name(), substance.selfLink)
        chunk = code.to_embedding_chunks()[0]
        self.assertEqual(chunk['content'], 'Example Concept identifier in CAS: ABC-123.')
        self.assertEqual(chunk['document_id'], '11111111-1111-1111-1111-111111111111')
        self.assertEqual(chunk['chunk_id'], 'root_codes_uuid:11111111-1111-1111-1111-111111111111')
        self.assertEqual(chunk['source'], 'gsrs')
        self.assertEqual(chunk['metadata']['hierarchy'], ['root', 'codes'])


    def test_embedding_root_name_falls_back_to_substance_uuid(self):
        code = Code.model_validate({'code': 'ABC-123', 'codeSystem': 'CAS'})
        code._set_parent_context('11111111-1111-1111-1111-111111111111', None)
        chunk = code.to_embedding_chunks()[0]
        self.assertEqual(chunk['content'], 'Substance 11111111-1111-1111-1111-111111111111 identifier in CAS: ABC-123.')

    def test_chemical_substance_adds_class_summary_chunk(self):
        substance = ChemicalSubstance.model_validate(
            {
                'substanceClass': 'chemical',
                'uuid': '11111111-1111-1111-1111-111111111111',
                'names': [{'name': 'Example Chemical', 'type': 'cn', 'languages': ['en']}],
                'references': [{'docType': 'SYSTEM'}],
                '_self': 'gsrs',
                'version': '1',
                'structure': {'stereochemistry': 'ACHIRAL', 'opticalActivity': 'NONE', 'atropisomerism': 'No', 'formula': 'H2O'},
                'moieties': [{'stereochemistry': 'ACHIRAL', 'opticalActivity': 'NONE', 'atropisomerism': 'No'}],
            }
        )
        class_chunks = [chunk for chunk in substance.to_embedding_chunks() if chunk['section'] == 'structure']
        self.assertEqual(len(class_chunks), 1)
        self.assertIn('Formula H2O.', class_chunks[0]['content'])
        self.assertEqual(class_chunks[0]['metadata']['hierarchy'], ['root', 'structure'])


if __name__ == '__main__':
    unittest.main()
