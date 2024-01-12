import unittest
import havina.graph_generator as gg
import havina.filters as fs
from havina.language_model import BertModel
import torch


class GraphGeneratorTest(unittest.TestCase):
    def test_worker(self):
        generator = gg.GraphGenerator(top_k=4)
        text = "Rihanna is a famous singer. She sings perfectly."
        result = generator(text, workers=1)
        expected = [
            fs.HeadTailRelations(
                head=fs.Entity(text='rihanna', wikidata_id=None),
                tail=fs.Entity(text='a famous singer', wikidata_id=None),
                relations=['be', 'sing']
            )
        ]
        self.assertEqual(result, expected)

    def test_clean_relations(self):
        input_relations = [
            fs.HeadTailRelations(
                head=fs.Entity(text='HH', wikidata_id=None),
                tail=fs.Entity(text='BB', wikidata_id=None),
                relations=['CC', 'GG', 'CC']
            ),
            fs.HeadTailRelations(
                head=fs.Entity(text='BB', wikidata_id=None),
                tail=fs.Entity(text='HH', wikidata_id=None),
                relations=['CC']
            ),
            fs.HeadTailRelations(
                head=fs.Entity(text='AA', wikidata_id='ss'),
                tail=fs.Entity(text='HH', wikidata_id='ss'),
                relations=['KK']
            ),
            fs.HeadTailRelations(
                head=fs.Entity(text='TT', wikidata_id=None),
                tail=fs.Entity(text='TT', wikidata_id=None),
                relations=['PP']
            ),
        ]
        result = gg.clean_relations(input_relations)
        expected = [
            fs.HeadTailRelations(
                head=fs.Entity(text='HH', wikidata_id=None),
                tail=fs.Entity(text='BB', wikidata_id=None),
                relations=['CC', 'GG']
            ),
            fs.HeadTailRelations(
                head=fs.Entity(text='AA', wikidata_id='ss'),
                tail=fs.Entity(text='HH', wikidata_id='ss'),
                relations=['KK']
            )
        ]
        self.assertEqual(result, expected)


class SplitSentenceTest(unittest.TestCase):
    class Bert1024(BertModel):
        def maximum_tokens(self) -> int:
            return 1024

    class Bert512(BertModel):
        def maximum_tokens(self) -> int:
            return 512

    @staticmethod
    def cmp_key(item: fs.HeadTailRelations):
        return item.head.text + item.tail.text

    def test_trivial_case(self):
        text = "This is a sentence."
        result = gg.split_text(text, 512)
        self.assertEqual(len(result), 1)

    def test_non_trivial_case(self):
        text = "This is the first sentence. This is the second sentence. This is the third sentence."
        result = gg.split_text(text, 11)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], 'This is the first sentence. This is the second sentence.')
        self.assertEqual(result[1], 'This is the third sentence.')

    def test_sanity(self):
        # source: https://en.wikipedia.org/wiki/Amsterdam
        text = ("Amsterdam was founded at the mouth of the Amstel River that was dammed to control flooding; "
                "the city's name derives from a local linguistic variation of the word dam. Originally a small fishing village "
                "in the late 12th century, Amsterdam became a major world port during the Dutch Golden Age of the 17th"
                " century, when the Netherlands was an economic powerhouse. Amsterdam was the leading centre for finance "
                "and trade, as well as a hub of production of secular art. In the 19th and 20th centuries, the city "
                "expanded and many new neighborhoods and suburbs were planned and built. The canals of Amsterdam and the "
                "19-20th century Defence Line of Amsterdam are both on the UNESCO World Heritage List. Sloten, annexed in "
                "1921 by the municipality of Amsterdam, is the oldest part of the city, dating to the 9th century. The city "
                "has a long tradition of openness, liberalism, and tolerance. Cycling is key to the city's modern character,"
                " and there are numerous biking paths and lanes spread throughout the entire city.")

        generator = gg.GraphGenerator(forward_tokens=True, link_entity=False, top_k=6, contiguous_token=True,
                                      relation_length=4, threshold=0.05, device='cpu', model=self.Bert1024)
        relations = generator(text, 2)
        relations.sort(key=SplitSentenceTest.cmp_key)

        generator = gg.GraphGenerator(forward_tokens=True, link_entity=False, top_k=6, contiguous_token=True,
                                      relation_length=4, threshold=0.05, device='cpu', model=self.Bert512)
        relations2 = generator(text, 2)

        relations2.sort(key=SplitSentenceTest.cmp_key)
        self.assertEqual(relations, relations2)


if __name__ == 'main':
    unittest.main()
