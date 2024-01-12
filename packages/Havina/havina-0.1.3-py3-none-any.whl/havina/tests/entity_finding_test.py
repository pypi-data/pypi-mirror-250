import unittest
import transformers
import havina.language_model as lm
import havina.entity_finding as ef
import torch


class EntityFindingTest(unittest.TestCase):
    def test_prepare(self):
        tokenizer = transformers.BertTokenizer.from_pretrained('bert-base-uncased')
        model = lm.get_model('bert', torch.device('cpu'))
        text = "Rihanna is a famous singer."
        sentence_test = ef.Sentence(text, model, False, False)
        model_input, noun_chunks = sentence_test.prepare()
        tokenized_sentence = tokenizer(text, max_len=model_input['input_ids'].size(1))
        diff = torch.sum(model_input['input_ids'] - torch.tensor(tokenized_sentence['input_ids']))
        self.assertEqual(diff, 0)
        diff = torch.sum(model_input['token_type_ids'] - torch.tensor(tokenized_sentence['token_type_ids']))
        self.assertEqual(diff, 0)
        diff = torch.sum(model_input['attention_mask'] - torch.tensor(tokenized_sentence['attention_mask']))
        self.assertEqual(diff, 0)
        self.assertEqual(len(tokenized_sentence), len(model_input))

        self.assertEqual(len(noun_chunks), 2)
        expected_chunks = [
            ef.NounChunk(text='rihanna', doc_start_idx=0, doc_end_idx=0, token_start_idx=1, token_end_idx=1,
                         wikidata_id=None),
            ef.NounChunk(text='a famous singer', doc_start_idx=2, doc_end_idx=4, token_start_idx=3, token_end_idx=5,
                         wikidata_id=None)]
        self.assertEqual(noun_chunks, expected_chunks)

    def test_entity_linking(self):
        text = "Rihanna is a famous singer. She sings perfectly. He is not good."
        model = lm.get_model('bert', torch.device('cpu'))
        sentence_test = ef.Sentence(text, model, True, False)
        _, noun_chunks = sentence_test.prepare()

        # Rihanna
        self.assertEqual(noun_chunks[0].text, 'rihanna')
        # She
        self.assertEqual(noun_chunks[2].text, 'rihanna')

        # Link to the same entity
        self.assertEqual(noun_chunks[0].wikidata_id, noun_chunks[2].wikidata_id)

    def test_resolve_references(self):
        text = "Rihanna is a famous singer. She sings perfectly."
        model = lm.get_model('bert', torch.device('cpu'))
        sentence_test = ef.Sentence(text, model, False, True)
        _, noun_chunks = sentence_test.prepare()

        self.assertEqual(noun_chunks[0].text, 'rihanna')
        self.assertEqual(noun_chunks[2].text, 'rihanna')

    def test_should_include(self):
        text = "Rihanna is a famous singer. She sings perfectly."
        model = lm.get_model('bert', torch.device('cpu'))
        sentence_test = ef.Sentence(text, model, False, True)
        _, noun_chunks = sentence_test.prepare()

        self.assertFalse(ef.should_include(noun_chunks[0], noun_chunks[2], sentence_test, False))
        self.assertFalse(ef.should_include(noun_chunks[2], noun_chunks[0], sentence_test, False))
        self.assertFalse(ef.should_include(noun_chunks[0], noun_chunks[2], sentence_test, False))

        sentence_test = ef.Sentence(text, model, True, True)
        _, noun_chunks = sentence_test.prepare()
        self.assertFalse(ef.should_include(noun_chunks[0], noun_chunks[1], sentence_test, True))
        self.assertTrue(ef.should_include(noun_chunks[0], noun_chunks[1], sentence_test, False))

    def test_search_beam(self):
        beam = ef.SearchBeam(2)
        self.assertFalse(beam.has_relation())
        self.assertEqual(beam.mean_score(), 0)
        beam.add(4, 5)
        beam.add(6, 3)
        self.assertTrue(beam.has_relation())
        self.assertEqual(beam.mean_score(), 4)
        self.assertEqual(ef.sort_beam(beam), 4)
        beam.finalize(10)
        self.assertEqual(beam.score, 18)

    def test_can_add(self):
        text = "Rihanna is a famous singer. She sings perfectly."
        model = lm.get_model('bert', torch.device('cpu'))
        sentence_test = ef.Sentence(text, model, False, True)
        _, noun_chunks = sentence_test.prepare()
        beam = ef.SearchBeam(2)

        pair = ef.HtPair(
            head=noun_chunks[0],
            tail=noun_chunks[1]
        )
        print(noun_chunks[1])

        candidates = []
        self.assertFalse(ef.can_add(4, pair, candidates, beam, 5))
        self.assertEqual(len(candidates), 0)
        beam.add(4, 5)
        self.assertFalse(ef.can_add(4, pair, candidates, beam, 1))
        self.assertEqual(len(candidates), 1)
        self.assertEqual(beam.score, 6)

        beam = ef.SearchBeam(2)
        self.assertFalse(ef.can_add(1, pair, candidates, beam, 2))
        self.assertTrue(ef.can_add(0, pair, candidates, beam, 2))


    def test_search_pass(self):
        text = "Rihanna is a famous singer. She sings perfectly."
        model = lm.get_model('bert', torch.device('cpu'))
        sentence_test = ef.Sentence(text, model, False, True)
        model_input, noun_chunks = sentence_test.prepare()
        attention = model.inference_attention(model_input).to('cpu').detach()
        ht_pairs = ef.create_ht_pairs(noun_chunks, sentence_test, False)
        candidates = ef.search_pass(attention, ht_pairs[0], 4, False, 2, 1)
        for item in candidates:
            self.assertTrue(len(item.rel_tokens) <= 2)
        candidates = ef.search_pass(attention, ht_pairs[0], 4, True, 4, 1)
        for item in candidates:
            for i in range(1, len(item.rel_tokens)):
                self.assertTrue(abs(item.rel_tokens[i-1] - item.rel_tokens[i]) == 1)

    def test_search_example(self):
        text = "John considers Anne a friend."
        model = lm.get_model("bert", torch.device('cpu'))
        sentence_test = ef.Sentence(text, model, False, True)
        model_input, noun_chunks = sentence_test.prepare()
        attention = model.inference_attention(model_input).to('cpu').detach()
        ht_pairs = ef.create_ht_pairs(noun_chunks, sentence_test, False)

        rels = []
        for pair in ht_pairs:
            candidates = ef.search_pass(attention, pair, 4, False, 3, 1)
            for item in candidates:
                txt = ''
                for token_id in item.rel_tokens:
                    word, _ = sentence_test.token_idx_2_word_doc_idx[token_id]
                    txt += str(word)
                    txt += ' '
                txt = txt[:-1]
                rels.append(txt)
        truth = ['a', 'considers', '.', 'friend', 'a a', 'a friend', 'a .', 'a considers', 'considers considers',
                 'considers a', 'considers .', 'considers friend', '. .', '. a', '. friend', '. considers',
                 'friend friend', 'friend a', 'friend .', 'friend considers', 'a a a', 'a a friend', 'a a .',
                 'a a considers', 'a friend friend', 'a friend a', 'a friend .', 'a friend considers', 'a . .',
                 'a . a', 'a . friend', 'a . considers', 'a considers considers', 'a considers a', 'a considers .',
                 'a considers friend', 'considers considers considers', 'considers considers a',
                 'considers considers .', 'considers considers friend', 'considers a a', 'considers a friend',
                 'considers a .', 'considers a considers', 'considers . .', 'considers . a', 'considers . friend',
                 'considers . considers', 'considers friend friend', 'considers friend a', 'considers friend .',
                 'considers friend considers', '. . .', '. . a', '. . friend', '. . considers', '. a a', '. a friend',
                 '. a .', '. a considers', '. friend friend', '. friend a', '. friend .', '. friend considers',
                 '. considers considers', '. considers a', '. considers .', '. considers friend',
                 'friend friend friend', 'friend friend a', 'friend friend .', 'friend friend considers', 'friend a a',
                 'friend a friend', 'friend a .', 'friend a considers', 'friend . .', 'friend . a', 'friend . friend',
                 'friend . considers', 'friend considers considers', 'friend considers a', 'friend considers .',
                 'friend considers friend', 'a', 'friend', 'considers', '.', 'a a', 'a friend', 'a considers', 'a .',
                 'friend friend', 'friend a', 'friend considers', 'friend .', 'considers considers', 'considers a',
                 'considers .', 'considers friend', '. .', '. a', '. friend', '. considers', 'a a a', 'a a friend',
                 'a a considers', 'a a .', 'a friend friend', 'a friend a', 'a friend considers', 'a friend .',
                 'a considers considers', 'a considers a', 'a considers .', 'a considers friend', 'a . .', 'a . a',
                 'a . friend', 'a . considers', 'friend friend friend', 'friend friend a', 'friend friend considers',
                 'friend friend .', 'friend a a', 'friend a friend', 'friend a considers', 'friend a .',
                 'friend considers considers', 'friend considers a', 'friend considers .', 'friend considers friend',
                 'friend . .', 'friend . a', 'friend . friend', 'friend . considers', 'considers considers considers',
                 'considers considers a', 'considers considers .', 'considers considers friend', 'considers a a',
                 'considers a friend', 'considers a considers', 'considers a .', 'considers . .', 'considers . a',
                 'considers . friend', 'considers . considers', 'considers friend friend', 'considers friend a',
                 'considers friend considers', 'considers friend .', '. . .', '. . a', '. . friend', '. . considers',
                 '. a a', '. a friend', '. a considers', '. a .', '. friend friend', '. friend a', '. friend considers',
                 '. friend .', '. considers considers', '. considers a', '. considers .', '. considers friend']
        self.assertEqual(rels, truth)


if __name__ == '__main__':
    unittest.main()
