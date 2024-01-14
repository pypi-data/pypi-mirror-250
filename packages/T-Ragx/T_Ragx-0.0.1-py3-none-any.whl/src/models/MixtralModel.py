from transformers import AutoTokenizer, AutoModelForCausalLM
import re


def glossary_to_text(glossary):
    out_text = "Relevant Dictionary records:\n"
    for d in glossary:
        for source_text in d:
            out_text += f"  {source_text}: {', '.join(d[source_text])}\n"
    return out_text


def trans_mem_to_text(source_text_list: list, trans_text_list: list):
    out_text = "Examples translations:\n"
    count = 1
    for st, tt in zip(source_text_list, trans_text_list):
        out_text += f""" {count}. \n   {st}\n   {tt}\n"""
        count += 1
    return out_text


class MixtralModel:
    tokenizer = None
    model = None

    def __init__(self, model_id="mistralai/Mistral-7B-Instruct-v0.2", adapter=None, tokenizer=None, model=None):

        if tokenizer is None:
            tokenizer = AutoTokenizer.from_pretrained(
                model_id,
                padding_side='left',
                truncation_side='left',
            )
            tokenizer.pad_token_id = tokenizer.unk_token_id
            tokenizer.pad_token = tokenizer.unk_token

        if model is None:
            model = AutoModelForCausalLM.from_pretrained(model_id, device_map="auto")
            if adapter is not None:
                if isinstance(adapter, list):
                    for a in adapter:
                        model.load_adapter(a)
                elif isinstance(adapter, str):
                    model.load_adapter(adapter)
                else:
                    ValueError("the adapter parameter must be either string or a list of strings")

            model = model.eval()

        self.model = model
        self.tokenizer = tokenizer

    def tokenize(self,
                 text_list=None,
                 tokenize_config=None
                 ):

        if text_list is None:
            text_list = []
        if tokenize_config is None:
            tokenize_config = {}

        default_tokenize_config = {
            'pad_to_multiple_of': 8,
            'padding': True,
            'truncation': True,
            'max_length': 2000,
            'return_tensors': 'pt',
            'add_special_tokens': False
        }
        for k in default_tokenize_config:
            if k not in tokenize_config:
                tokenize_config[k] = default_tokenize_config[k]

        return self.tokenizer.batch_encode_plus(text_list, **tokenize_config).to(self.model.device)

    def generate(self, tokenized_input, generation_config=None):
        if generation_config is None:
            generation_config = {
                'max_new_tokens': 100,
                'early_stopping': True,
                'eos_token_id': [self.tokenizer.eos_token_id]
            }

        return self.model.generate(**tokenized_input, **generation_config)

    @staticmethod
    def clean_output(text):
        special_tok_q = " ?/[//INST/] ?"
        return re.sub(special_tok_q, "", text.replace("//", "")).strip()

    def process_output(self, model_output, tokenized_input):
        translation_outputs = [
            o[len(i):]
            for o, i in zip(model_output.cpu().numpy(), tokenized_input['input_ids'].cpu().numpy())
        ]

        decoded_outputs = self.tokenizer.batch_decode(translation_outputs, skip_special_tokens=True)
        decoded_outputs = [
            self.clean_output(o) for o in decoded_outputs
        ]
        return decoded_outputs

    def translate(self, text: list,
                  source_lang="Japanese",
                  target_lang="English",
                  translation_history: list = None,
                  search_result: list = None,
                  tokenize_config=None,
                  generation_config=None
                  ):

        query_prompts = self.batch_build_prompt(
            text=text,
            source_lang=source_lang,
            target_lang=target_lang,
            translation_history=translation_history,
            search_result=search_result
        )

        token_data = self.tokenize(query_prompts, tokenize_config)
        generation_output = self.generate(token_data, generation_config)
        translated_output = self.process_output(generation_output, token_data)
        return translated_output

    def batch_build_prompt(self,
                           text: list,
                           source_lang="Japanese",
                           target_lang="English",
                           translation_history: list = None,
                           search_result: list = None):

        if translation_history is not None:
            assert len(translation_history) == len(text)
        else:
            translation_history = [None] * len(text)

        if search_result is not None:
            assert len(search_result) == len(text)
        else:
            search_result = [None] * len(text)

        return [
            self.build_prompt(
                t,
                source_lang=source_lang,
                target_lang=target_lang,
                translation_history=th,
                search_result=sr
            )
            for t, th, sr in zip(text, translation_history, search_result)
        ]

    def build_prompt(self,
                     text,
                     source_lang="Japanese",
                     target_lang="English",
                     translation_history=None,
                     search_result=None
                     ):
        # translation_history = [
        #     ("some source text", "some translated text"),
        #     ("some source text", "some translated text"),
        # ]

        if translation_history is None:
            translation_history = []
        if search_result is None:
            search_result = {'glossary': [], 'memory': []}

        translation_history_context = ""
        if len(translation_history) > 0:
            translation_history_context = "Previous context:\n"
            for source_text, trans_text in translation_history:
                translation_history_context += f"  {source_lang}: {source_text}\n"
                translation_history_context += f"  {target_lang}: {trans_text}\n"
                translation_history_context += "\n"

        chat = [
            {
                "role": "user",
                "content": (
                    f"{translation_history_context}"
                    "As a large language model, you are a trained expert in multiple languages. "
                    "These are some references that might help you:\n"
                    f"{glossary_to_text(search_result['glossary'])}"
                    f"{trans_mem_to_text(*search_result['memory'])}"
                    f"Translate this {source_lang} passage to {target_lang} without additional questions, "
                    "disclaimer, or explanations, but accurately and completely:\n"
                    f"{text}"
                )
            },
        ]
        return self.tokenizer.apply_chat_template(chat, tokenize=False, )
