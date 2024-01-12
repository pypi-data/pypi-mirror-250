import unittest
import havina.language_model as lm
import havina.graph_generator
import havina.filters as fs
import torch
import transformers
from transformers import AutoTokenizer


class BertModelTest(unittest.TestCase):
    def test_get_model(self):
        with self.assertRaises(Exception) as context:
            _model = lm.get_model("no", torch.device("cpu"))

        self.assertTrue("Model not found" in str(context.exception))

    def test_simple_functions(self):
        model = lm.get_model('bert', torch.device('cpu'))
        self.assertEqual(model.init_token_idx_2_word_doc_idx(), [('CLS', -1)])
        self.assertEqual(model.num_start_tokens(), 1)
        test_list = []
        model.append_last_token(test_list)
        self.assertEqual(test_list[0], ('SEP', 0))

        tokenizer = transformers.BertTokenizer.from_pretrained('bert-base-uncased')
        self.assertEqual(model.tokenize('hello'), tokenizer('hello', add_special_tokens=False)['input_ids'])

        fake_tokens = [1, 2]
        result = model.model_input(fake_tokens)
        fake_tokens = [tokenizer.cls_token_id] + fake_tokens + [tokenizer.sep_token_id]
        device = torch.device('cpu')
        res_dict = {
            'input_ids': torch.tensor(fake_tokens, device=device).long().unsqueeze(0),
            'token_type_ids': torch.zeros(len(fake_tokens), device=device).long().unsqueeze(0),
            'attention_mask': torch.ones(len(fake_tokens), device=device).long().unsqueeze(0),
        }
        sub = torch.sub(result['input_ids'], res_dict['input_ids']).sum()
        sub1 = torch.sub(result['token_type_ids'], res_dict['token_type_ids']).sum()
        sub2 = torch.sub(result['attention_mask'], res_dict['attention_mask']).sum()
        total = sub + sub1 + sub2
        self.assertEqual(total, 0)

        inference_result = model.inference_attention(result)
        # mean of the last attention layers
        bert_model = transformers.BertModel.from_pretrained('bert-base-uncased')
        model_output = bert_model(**result, output_attentions=True).attentions[-1]
        resulting_mean = torch.mean(model_output, dim=1)
        sub = torch.sub(inference_result, resulting_mean).sum()
        self.assertEqual(sub, 0)


class LLama2ModelTest(unittest.TestCase):
    def test_simple_functions(self):
        model = lm.get_model('llama2', torch.device('cpu'))
        self.assertEqual(model.init_token_idx_2_word_doc_idx(), [])
        self.assertEqual(model.num_start_tokens(), 0)
        test_list = []
        model.append_last_token(test_list)
        self.assertEqual(len(test_list), 0)

        tokenizer = tokenizer = AutoTokenizer.from_pretrained('EleutherAI/gpt-neox-20b')
        self.assertEqual(model.tokenize('hello'), tokenizer('hello', add_special_tokens=False)['input_ids'])

        fake_tokens = [1, 2]
        result = model.model_input(fake_tokens)
        device = torch.device('cpu')
        res_dict = {
            'input_ids': torch.tensor(fake_tokens, device=device).long().unsqueeze(0),
            'attention_mask': torch.ones(len(fake_tokens), device=device).long().unsqueeze(0),
        }
        sub = torch.sub(result['input_ids'], res_dict['input_ids']).sum()
        sub2 = torch.sub(result['attention_mask'], res_dict['attention_mask']).sum()
        total = sub + sub2
        self.assertEqual(total, 0)

        inference_result = model.inference_attention(result)
        # mean of the last attention layers
        bert_model = transformers.AutoModelForCausalLM.from_pretrained(
            'mosaicml/mpt-7b',
            trust_remote_code=True)
        model_output = bert_model(**result, output_attentions=True).attentions[-1]
        resulting_mean = torch.mean(model_output, dim=1)
        sub = torch.sub(inference_result, resulting_mean).sum()
        self.assertEqual(sub, 0)

    def test_sanity(self):
        gen = havina.GraphGenerator(model='llama2')
        text = 'John Lennon is a famous singer'
        result = gen(text)
        self.assertEqual(result,
                         [
                             fs.HeadTailRelations(
                                 head=fs.Entity(text='john lennon', wikidata_id=None),
                                 tail=fs.Entity(text='a famous singer', wikidata_id=None), relations=['be'])])


if __name__ == 'main':
    unittest.main()
