import unittest
import torch
import havina.entity_finding as ef
import havina.language_model as lm
import havina.filters as ff


class FiltersTest(unittest.TestCase):
    def test_filter_branches(self):
        model = lm.get_model('bert', torch.device('cpu'))
        text = "Rihanna is a famous singer."
        sentence_test = ef.Sentence(text, model, False, False)
        _, noun_chunks = sentence_test.prepare()
        pair = ef.HtPair(
            head=noun_chunks[0],
            tail=noun_chunks[1]
        )
        filter = ff.IndividualFilter(sentence_test, False, 0.5)
        cand1 = ef.SearchBeam(2)
        cand1.add(1, 0.2)
        cand2 = ef.SearchBeam(4)
        cand2.add(2, 0.4)
        candidates = [cand1, cand2]
        res = filter.filter(candidates, pair)
        self.assertEqual(len(res.relations), 0)

        cand1.add(2, 0.1)
        cand2.add(4, 0.4)
        filter = ff.IndividualFilter(sentence_test, True, 0.2)
        candidates = [cand1, cand2]
        res = filter.filter(candidates, pair)
        self.assertEqual(len(res.relations), 0)

        cand1 = ef.SearchBeam(1)
        cand1.add(1, 0.9)
        cand2 = ef.SearchBeam(1)
        cand2.add(5, 0.9)
        res = filter.filter([cand1, cand2], pair)
        self.assertEqual(len(res.relations), 0)

    def test_filter_complete(self):
        text = "Alice considers John a friend."
        model = lm.get_model("bert", torch.device('cpu'))
        sentence_test = ef.Sentence(text, model, False, True)
        model_input, noun_chunks = sentence_test.prepare()
        attention = model.inference_attention(model_input).to('cpu').detach()
        ht_pairs = ef.create_ht_pairs(noun_chunks, sentence_test, False)

        test_filter = ff.IndividualFilter(sentence_test, True, 0.015)
        rels = []
        for pair in ht_pairs:
            candidates = ef.search_pass(attention, pair, 6, False, 4, 1)
            rels.append(test_filter.filter(candidates, pair))
        expected = [ff.HeadTailRelations(head=ff.Entity(text='alice', wikidata_id=None),
                                         tail=ff.Entity(text='john', wikidata_id=None),
                                         relations=['consider', 'friend', 'friend', 'friend', 'friend']),
                    ff.HeadTailRelations(head=ff.Entity(text='john', wikidata_id=None),
                                         tail=ff.Entity(text='alice', wikidata_id=None),
                                         relations=['friend', 'consider', 'friend', 'friend', 'friend'])]
        self.assertEqual(expected, rels)

    def test_lemmatize(self):
        text = "Alice considers John a friend."
        model = lm.get_model("bert", torch.device('cpu'))
        sentence_test = ef.Sentence(text, model, False, True)
        _, _ = sentence_test.prepare()
        ind_filter = ff.IndividualFilter(sentence_test, False, 0.001)

        res = ind_filter.lemmatize('2021', [])
        self.assertEqual(res, '')

        res = ind_filter.lemmatize('', [4, 5, 5])
        self.assertEqual(res, 'friend')

    def test_frequency_cutoff(self):
        et1 = ff.Entity('1', None)
        et2 = ff.Entity('2', None)
        et3 = ff.Entity('3', None)

        rels1 = ff.HeadTailRelations(
            head=et1,
            tail=et2,
            relations=['1', '2']
        )
        rels2 = ff.HeadTailRelations(
            head=et2,
            tail=et3,
            relations=['2', '3']
        )

        relations = [rels1, rels2]
        ff.frequency_cutoff(relations, 2)

        truth_1 = ff.HeadTailRelations(
            head=et1,
            tail=et2,
            relations=['2']
        )
        truth_2 = ff.HeadTailRelations(
            head=et2,
            tail=et3,
            relations=['2']
        )
        self.assertEqual(relations, [truth_1, truth_2])


if __name__ == '__main__':
    unittest.main()
