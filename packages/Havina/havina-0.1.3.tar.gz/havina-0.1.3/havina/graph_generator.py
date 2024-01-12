import multiprocessing

import torch
from spacy.lang.en import English

import havina.entity_finding as ef
import havina.language_model as lm
from multiprocessing import Pool
import havina.filters as fs
import os


class GraphGenerator:
    def __init__(
            self,
            top_k=4,
            threshold=0.015,
            link_entity=False,
            model='bert',
            contiguous_token=True,
            forward_tokens=True,
            frequency=1,
            relation_length=8,
            resolve_reference=True,
            device=None):
        """
        Initialize the graph generator class with the following parameters:
        :param top_k: Number of candidates to select for the next iteration of the beam search
        :param threshold: Discard a relation if its accumulated attention score is below this threshold
        :param link_entity: Link head and tail entities using Wikidata database
        :param model: Language model to extract attention scores from
        :param contiguous_token: When generating relations, consider only those with contiguous tokens
        :param forward_tokens: When filtering relations, remove those whose order of words do not follow that of the
        text. (i.e. if the input is 'I love beautiful cars', a relation like 'beautiful love' would be removed)
        :param frequency: The frequency cutoff. If a relation appears less than 'frequency' in the text corpus, it
        will not be accounted.
        :param relation_length: Maximum quantity of tokens allowed in a relation.
        :param resolve_reference: Resolve cross-references, i.e. replace pronouns (e.g. 'he') by the noun they refer to
        :param device: Pytorch device in which to run the language model

        The word tokens refer not to words but to the items in a tokenized sentence, prepared to be the input of the
        language model.
        """
        self.top_k = top_k
        self.threshold = threshold
        self.link_entity = link_entity
        if isinstance(device, str):
            device = torch.device(device)
        if isinstance(model, str):
            self.model = lm.get_model(model, device)
        elif issubclass(model, lm.LanguageModel):
            self.model = model(device)
        self.contiguous_token = contiguous_token
        self.forward_tokens = forward_tokens
        self.frequency = frequency
        self.relation_length = relation_length
        self.device = device
        self.resolve_reference = resolve_reference

    def __call__(self, text: str, workers=1) -> list[fs.HeadTailRelations]:
        """
        Processes an input sentence and returns a list of head and tails and their corresponding relations.

        :param sentence: A string to be processed
        :param workers: The number of processes to create for splitting the work
        :return: A list of head and tails entities and their corresponding relations
        """

        if len(text) > self.model.maximum_tokens():
            result = []
            for sentence in split_text(text, self.model.maximum_tokens()):
                result += self.process_sentence(sentence, workers)
            return result
        else:
            return self.process_sentence(text, workers)

    def process_sentence(self, sentence: str, workers) -> list[fs.HeadTailRelations]:
        processed_sentence = ef.Sentence(sentence, self.model, self.link_entity, self.resolve_reference)
        model_input, noun_chunks = processed_sentence.prepare()
        attention = self.model.inference_attention(model_input).to('cpu').detach()

        ht_pairs = ef.create_ht_pairs(noun_chunks, processed_sentence, self.link_entity)
        ind_filter = fs.IndividualFilter(processed_sentence, self.forward_tokens, self.threshold)

        worker = WorkerClass(attention, self.top_k, self.contiguous_token, self.relation_length,
                             self.model.num_start_tokens(), ind_filter)

        relations: list[fs.HeadTailRelations] = []
        if workers <= 0:
            raise Exception('Invalid number of workers')
        elif workers == 1:
            for idx, item in enumerate(ht_pairs):
                relations.append(worker.do_work(item))
        else:
            os.environ['TOKENIZERS_PARALLELISM'] = 'true'
            try:
                multiprocessing.set_start_method('fork')
            except RuntimeError:
                pass
            with Pool(workers) as p:
                for item in p.imap_unordered(worker.do_work, ht_pairs):
                    relations.append(item)

        fs.frequency_cutoff(relations, self.frequency)

        return clean_relations(relations)


class WorkerClass:
    def __init__(self, attention, top_k, contiguous_token, relation_length, start_tokens, ind_filter):
        self.attention = attention
        self.top_k = top_k
        self.contiguous_token = contiguous_token
        self.relation_length = relation_length
        self.start_tokens = start_tokens
        self.ind_filter = ind_filter

    def do_work(self, pair: ef.HtPair):
        candidates = ef.search_pass(self.attention, pair, self.top_k, self.contiguous_token, self.relation_length,
                                    self.start_tokens)
        return self.ind_filter.filter(candidates, pair)

def clean_relations(ht_pairs: list[fs.HeadTailRelations]) -> list[fs.HeadTailRelations]:
    unique_relations = set()
    for ht_pair in ht_pairs:
        filtered_relations = []
        for relation in ht_pair.relations:
            unique_key = ht_pair.head.text + "|" + relation + "|" + ht_pair.tail.text
            reverse_key = ht_pair.tail.text + "|" + relation + "|" + ht_pair.head.text
            if unique_key not in unique_relations and reverse_key not in unique_relations:
                filtered_relations.append(relation)
                unique_relations.add(unique_key)
        ht_pair.relations = filtered_relations

    new_list = [pair for pair in ht_pairs if len(pair.relations) > 0 and
                (pair.head.wikidata_id != pair.tail.wikidata_id
                 or pair.head.text != pair.tail.text)]

    return new_list


def split_text(text: str, max_len: int) -> list[str]:
    if len(text.split(' ')) < max_len:
        return [text]

    nlp_tool = English()
    nlp_tool.add_pipe('sentencizer')
    doc = nlp_tool(text)

    result: list[str] = []
    for item in doc.sents:
        item_txt = str(item.text)
        if len(result) > 0 and len(result[-1].split(' ')) + len(item_txt.split(' ')) + 1 <= max_len:
            result[-1] += ' ' + item_txt
        else:
            result.append(item_txt)

    return result

