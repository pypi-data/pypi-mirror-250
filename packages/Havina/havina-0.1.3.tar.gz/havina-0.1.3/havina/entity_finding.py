import coreferee.errors
import spacy
from dataclasses import dataclass
import copy
import havina.language_model as lm
from typing import Optional


@dataclass
class NounChunk:
    text: str
    doc_start_idx: int
    doc_end_idx: int
    token_start_idx: int
    token_end_idx: int
    wikidata_id: Optional[str]


class Sentence:
    def __init__(self, text: str, model: lm.LanguageModel, link_entities: bool, resolve_references: bool):
        try:
            spacy.load('en_core_web_lg')
            nlp_tool = spacy.load('en_core_web_trf')
        except OSError:
            from spacy.cli import download
            download('en_core_web_trf')
            download('en_core_web_lg')
            nlp_tool = spacy.load('en_core_web_trf')

        try:
            nlp_tool.add_pipe('coreferee')
        except coreferee.errors.ModelNotSupportedError:
            import subprocess
            import sys
            subprocess.check_call([sys.executable, '-m', 'coreferee', 'install', 'en'])
            nlp_tool.add_pipe('coreferee')

        # It is not possible to serialize the entity linker for multiprocessing, so I need to run Spacy twice
        self.doc = nlp_tool(text)
        entity_tool = spacy.load('en_core_web_trf')
        entity_tool.add_pipe("entityLinker", last=True)
        self.entity_doc = entity_tool(text)
        self.doc_idx_2_token_idx: list[int] = []
        self.token_idx_2_word_doc_idx: list[tuple[str, int]] = []
        self.model = model
        self.link_entities = link_entities
        self.resolve_references = resolve_references

    def prepare(self):
        noun_chunks = []
        for chunk in self.doc.noun_chunks:
            noun_chunks.append(
                NounChunk(
                    text=chunk.text.lower(),
                    doc_start_idx=chunk.start,
                    doc_end_idx=chunk.end-1,
                    token_start_idx=0,
                    token_end_idx=0,
                    wikidata_id=None,
                )
            )

        if self.link_entities:
            self.entity_linking(noun_chunks)

        if self.resolve_references:
            self.resolve_chunk_references(noun_chunks)

        tokenized_sentence = []
        self.token_idx_2_word_doc_idx = self.model.init_token_idx_2_word_doc_idx()
        chunk_iter = 0
        state = 0

        start_tokens_no = self.model.num_start_tokens()
        for idx, word in enumerate(self.doc):
            tokenized = self.model.tokenize(word)
            self.doc_idx_2_token_idx.append(len(tokenized_sentence) + start_tokens_no)
            self.token_idx_2_word_doc_idx += [(str(word), idx)] * len(tokenized)
            if chunk_iter < len(noun_chunks):
                if state == 0:
                    if noun_chunks[chunk_iter].doc_start_idx == idx:
                        noun_chunks[chunk_iter].token_start_idx = start_tokens_no + len(tokenized_sentence)
                        state = 1
                    if noun_chunks[chunk_iter].doc_end_idx == idx:
                        noun_chunks[chunk_iter].token_end_idx = start_tokens_no + len(tokenized_sentence)
                        chunk_iter += 1
                        state = 0
                elif state == 1:
                    if noun_chunks[chunk_iter].doc_end_idx == idx:
                        noun_chunks[chunk_iter].token_end_idx = start_tokens_no + len(tokenized_sentence)
                        chunk_iter += 1
                        state = 0
            tokenized_sentence += tokenized

        self.model.append_last_token(self.token_idx_2_word_doc_idx)
        model_input = self.model.model_input(tokenized_sentence)

        return model_input, noun_chunks

    def entity_linking(self, chunks: list[NounChunk]):
        available_entities: dict[str, int] = {}
        for idx, entity in enumerate(self.entity_doc._.linkedEntities):
            available_entities[
                entity.get_span().text.lower()
            ] = idx

        for chunk in chunks:
            self.link_entity(chunk, available_entities)

    def link_entity(self, chunk: NounChunk, available_entities: dict[str, int]):
        if chunk.text.lower() in available_entities:
            idx = available_entities[chunk.text.lower()]
            self.link_entity_idx(idx, chunk)
        else:
            potential_entity = None
            references = self.get_references(chunk)

            for item in references:
                if item in available_entities:
                    if potential_entity is None:
                        potential_entity = available_entities[item]
                    else:
                        print(f"Multiple references found for {chunk.text}")
                        break

            if potential_entity is not None:
                self.link_entity_idx(potential_entity, chunk)

    def link_entity_idx(self, idx: int, chunk: NounChunk):
        chunk.wikidata_id = self.entity_doc._.linkedEntities[idx].get_id()
        chunk.text = self.entity_doc._.linkedEntities[idx].get_span().text.lower()

    def resolve_chunk_references(self, chunks: list[NounChunk]):
        for chunk in chunks:
            new_ids = []
            remove_morpho = {'ADJ', 'ADV', 'SYM', 'OTHER', 'PUNCT', 'DET', 'ADP', 'AUX', 'VERB'}
            for doc_idx in range(chunk.doc_start_idx, chunk.doc_end_idx + 1):
                if not self.doc[doc_idx].pos_ in remove_morpho:
                    new_ids.append(doc_idx)
                    # new_text += sentence.doc[doc_idx].text
                    # new_text += ' '

            resolution = None
            if len(new_ids) == 1:
                doc_id = new_ids[0]
                references = self.doc._.coref_chains.resolve(self.doc[doc_id])
                if self.doc[doc_id].text == 'who':
                    print(f"who: '{references}'")
                if references is not None and (
                        self.doc[doc_id].pos_ == 'PRON' or self.doc[doc_id].pos_ == 'NOUN'):
                    resolution = references[0].text.lower()

            if resolution is not None:
                chunk.text = resolution

    def get_references(self, chunk: NounChunk) -> set[str]:
        result = set()
        for doc_idx in range(chunk.doc_start_idx, chunk.doc_end_idx+1):
            references = self.doc._.coref_chains.resolve(self.doc[doc_idx])
            if references is not None:
                for item in references:
                    result.add(item.text.lower())

        return result

@dataclass
class HtPair:
    head: NounChunk
    tail: NounChunk


def create_ht_pairs(noun_chunks: list[NounChunk], sentence: Sentence, link_entity: bool) -> list[HtPair]:
    ht_pairs = []
    for idx1, chunk1 in enumerate(noun_chunks):
        for idx2, chunk2 in enumerate(noun_chunks):
            if idx1 == idx2 or not should_include(chunk1, chunk2, sentence, link_entity):
                continue

            ht_pairs.append(
                HtPair(
                    head=chunk1,
                    tail=chunk2,
                )
            )
    return ht_pairs


def should_include(head: NounChunk, tail: NounChunk, sentence: Sentence, link_entity: bool) -> bool:
    len1 = head.doc_end_idx - head.doc_start_idx + 1
    len2 = tail.doc_end_idx - tail.doc_start_idx + 1

    both = 0
    if len1 == 1 and sentence.doc[head.doc_start_idx].pos_ == 'PRON':
        both += 1
        if tail.text.lower() in sentence.get_references(head):
            return False
    if len2 == 1 and sentence.doc[tail.doc_start_idx].pos_ == 'PRON':
        both += 1
        if head.text.lower() in sentence.get_references(tail):
            return False

    if both == 2:
        head_ref = sentence.get_references(head)
        tail_ref = sentence.get_references(tail)
        intersection = head_ref.intersection(tail_ref)
        return len(intersection) == 0

    if link_entity and (head.wikidata_id is None or tail.wikidata_id is None):
        return False

    # FIXME: spaCy's reference resolution does not find the anaphoric antecedent of 'that', 'who' and 'which'.
    # The algorithm, though, is clever enough to find the proper relationships between the antecendent and other
    # noun chunks.
    unresolved_anaphoras = {'who', 'which', 'that'}
    if head.text.lower() in unresolved_anaphoras or tail.text.lower() in unresolved_anaphoras:
        return False

    return True


class SearchBeam:
    def __init__(self, initial_id):
        self.last_token = initial_id
        self.score = 0
        self.visited = [initial_id]
        self.rel_tokens = []

    def add(self, token_id, score):
        self.last_token = token_id
        self.visited.append(token_id)
        self.score += score
        self.rel_tokens.append(token_id)

    def has_relation(self) -> bool:
        return len(self.rel_tokens) > 0

    def finalize(self, score):
        self.score += score

    def mean_score(self) -> float:
        if len(self.rel_tokens) == 0:
            return 0
        return self.score / len(self.rel_tokens)


def sort_beam(e: SearchBeam) -> float:
    return e.mean_score()


def search_pass(attention_matrix, ht_pair: HtPair, k: int, contiguous: bool, length: int, start_tokens: int) -> list[SearchBeam]:
    queue = [
        SearchBeam(ht_pair.head.token_start_idx)
    ]

    candidate_facts = []
    visited = set()
    while len(queue) > 0:
        item = queue.pop(0)

        if len(item.rel_tokens) > length:
            continue

        # "John considers Anne a friend"
        # "considers a friend" would be eliminated here
        if contiguous and len(item.rel_tokens) > 1 and abs(item.rel_tokens[-2] - item.rel_tokens[-1]) != 1:
            continue

        beams = []
        attention_scores = attention_matrix[:, item.last_token]
        for i in range(start_tokens, len(attention_scores)-1):
            next_path = tuple(item.visited + [i])
            if can_add(i, ht_pair, candidate_facts, item, attention_scores[i].detach()) and next_path not in visited:
                beams.append(
                    copy.deepcopy(item)
                )
                beams[-1].add(i, attention_scores[i].detach())
                visited.add(next_path)

        beams.sort(key=sort_beam, reverse=True)
        queue += beams[:k]

    return candidate_facts


def can_add(token_id, pair: HtPair, candidates: list[SearchBeam], item: SearchBeam, score: float) -> bool:
    if pair.tail.token_start_idx <= token_id <= pair.tail.token_end_idx:
        if item.has_relation():
            item.finalize(score)
            candidates.append(item)
            return False

    return not (pair.head.token_start_idx <= token_id <= pair.head.token_end_idx or
                pair.tail.token_start_idx <= token_id <= pair.tail.token_end_idx)
