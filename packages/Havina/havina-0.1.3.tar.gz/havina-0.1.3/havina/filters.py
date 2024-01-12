import havina.entity_finding as ef
from dataclasses import dataclass
from typing import Optional


@dataclass
class Entity:
    text: str
    wikidata_id: Optional[str]


@dataclass
class HeadTailRelations:
    head: Entity
    tail: Entity
    relations: list[str]


class IndividualFilter:
    def __init__(self, sentence: ef.Sentence, forward_relations: bool, threshold: float):
        self.token_idx_2_word_doc_idx = sentence.token_idx_2_word_doc_idx
        self.doc = sentence.doc
        self.forward_relations = forward_relations
        self.threshold = threshold

    def filter(self, candidates: list[ef.SearchBeam], ht_pair: ef.HtPair) -> HeadTailRelations:
        response = HeadTailRelations(
            head=Entity(
                text=ht_pair.head.text.lower(),
                wikidata_id=ht_pair.head.wikidata_id,
            ),
            tail=Entity(
                text=ht_pair.tail.text.lower(),
                wikidata_id=ht_pair.tail.wikidata_id,
            ),
            relations=[]
        )

        for candidate in candidates:
            if candidate.mean_score() < self.threshold:
                continue
            rel_txt = ''
            rel_idx = []
            last_index = None
            valid = True
            for token_id in candidate.rel_tokens:
                word, word_id = self.token_idx_2_word_doc_idx[token_id]
                # "John considers Anne a friend"
                # "considers a friend" would be eliminated here
                if self.forward_relations and last_index is not None and word_id - last_index != 1:
                    valid = False
                    break
                last_index = word_id

                if len(rel_txt) > 0:
                    rel_txt += ' '
                lowered_word = word.lower()
                if lowered_word not in ht_pair.head.text and lowered_word not in ht_pair.tail.text:
                    rel_txt += word.lower()
                    rel_idx.append(word_id)

            if valid:
                rel_txt = self.lemmatize(rel_txt, rel_idx)
                if len(rel_txt) == 0:
                    continue

                response.relations.append(rel_txt)
        return response

    def lemmatize(self, relation: str, indexes: list[int]) -> str:
        if relation.isnumeric():
            return ''

        new_text = ''
        # Another option would be including 'AUX'
        remove_morpho = {'ADJ', 'ADV', 'SYM', 'OTHER', 'PUNCT',
                         'NUM', 'INTJ', 'DET', 'ADP', 'PRON',
                         'CONJ', 'CCONJ', 'SCONJ', 'PART'}
        last_word = ' '
        for item_idx in indexes:
            if not self.doc[item_idx].pos_ in remove_morpho:
                new_word = self.doc[item_idx].lemma_.lower()
                if last_word != new_word:
                    new_text += new_word
                    new_text += ' '
                    last_word = new_word

        new_text = new_text[:-1]

        return new_text


def frequency_cutoff(ht_relations: list[HeadTailRelations], frequency: int):
    if frequency == 1:
        return
    counter: dict[str, int] = {}
    for ht_item in ht_relations:
        for relation in ht_item.relations:
            if relation in counter:
                counter[relation] += 1
            else:
                counter[relation] = 1

    for ht_item in ht_relations:
        ht_item.relations = [rel for rel in ht_item.relations if counter[rel] >= frequency]
