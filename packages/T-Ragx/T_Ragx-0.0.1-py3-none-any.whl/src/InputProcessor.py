import json
import typing

import datasets
import pandas as pd
import torch
from elasticsearch import client as elastic_client
from jinja2 import Template as JinjaTemplate
import unicodedata
from elasticsearch import Elasticsearch
from tqdm.autonotebook import tqdm


DEFAULT_PROMPT_TEMPLATE = """[INST] <|system|> Translate the given text to {{target_language}}:
<|user|> 
{{source_text}}
[/INST]
<|context|> [CON]
Glossary: {{glossary_data}}
Reference translations: {{ref_trans_data}}
[/CON]
<|assistant|>"""


def serialize_str(s):
    return json.dumps(s, ensure_ascii=False)


def clean_text(text):
    return unicodedata.normalize('NFKD', text)


# heuristic glossary retrieval
def get_glossary(text, glossary_index, max_k=10, lang_code='en'):
    text = clean_text(text)
    out_dict = {}
    count = 0
    for k in glossary_index:
        if k in text:
            if lang_code not in glossary_index[k]:
                continue

            skip_flag = False
            # check for glossary word being a component of a longer glossary word
            for ek in out_dict:
                if k in ek:
                    skip_flag = True
                    break
            if skip_flag:
                continue

            out_dict[k] = glossary_index[k][lang_code].tolist()
            count += 1
            if count >= max_k:
                break

    return out_dict


class InputProcessor:
    def __init__(self,
                 device=None,
                 prompt_template: typing.Optional[typing.Union[str, JinjaTemplate]] = None
                 ):
        self.device = device
        if device is None:
            self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        if prompt_template is None:
            self.prompt_template = JinjaTemplate(DEFAULT_PROMPT_TEMPLATE)
        else:
            if isinstance(prompt_template, str):
                self.prompt_template = JinjaTemplate(prompt_template)
            elif isinstance(prompt_template, JinjaTemplate):
                self.prompt_template = prompt_template
            else:
                raise ValueError()

        self.es_client = None
        self.general_memory_index_key = None
        self.general_memory: typing.Optional[datasets.Dataset] = None
        self.task_memory: dict = {}

        self.general_glossary: dict = {}
        self.task_glossary: dict = {}

    def load_general_translation(self,
                                 parquet_path,
                                 index_key='ja',
                                 elasticsearch_host: str = "localhost",
                                 elasticsearch_port: int = 9200,
                                 es_client: elastic_client = None,
                                 dataset_args={},
                                 elastic_args={},
                                 elastic_client_args={}
                                 ):
        """
        Load the general translation examples
        """
        self.general_memory = datasets.Dataset.from_pandas(pd.read_parquet(parquet_path), **dataset_args)
        hasher = datasets.fingerprint.Hasher()
        memory_fingerprint = hasher.hash(self.general_memory)

        es_index_name = f"hf_{index_key}_{memory_fingerprint}"

        # initiate the elastic index
        if es_client is None:
            es_client = Elasticsearch(
                elasticsearch_host,  # Elasticsearch endpoint
                port=elasticsearch_port,
                **elastic_client_args
            )

        self.es_client = es_client

        if es_client.indices.exists(index=es_index_name):
            self.general_memory.load_elasticsearch_index(index_key, es_index_name=es_index_name)
        else:
            self.general_memory.add_elasticsearch_index(index_key, es_index_name=es_index_name,
                                                        es_client=es_client, **elastic_args)

        self.general_memory_index_key = index_key

        return

    def load_task_translation(self):
        """
        Load the general translation examples
        """
        raise NotImplementedError()
        pass

    def search_general_memory(self, text, search_index: str = None, k=4, max_item_len=500, **search_kwargs):
        """
        search general translation examples using elasticsearch
        """
        if search_index is None:
            search_index = self.general_memory_index_key

        mem_scores, mem_indices = self.general_memory.search_batch(search_index, text, k=k, **search_kwargs)

        ref_trans_data = [self.general_memory[midx] for midx in mem_indices]

        # truncate in case the example translations are too long
        processed_output = []
        for rtd, score_list in zip(ref_trans_data, mem_scores):
            wide_output = []
            key_list = list(rtd.keys())
            for i in range(len(rtd[key_list[0]])):
                wide_output.append({
                    k: rtd[k][i][:max_item_len] for k in key_list
                })
                wide_output[-1]['score'] = score_list[i]
            processed_output.append(wide_output)

        return processed_output

    def get_task_memory(self, client=None):
        """
        search in-task translation examples using elasticsearch
        """
        raise NotImplementedError()

    def load_general_glossary(self, glossary_parquet_path, encoding="utf8"):
        """
        Load the general glossary (i.e. wikidata title pair/ dictionary entries )
        format: {
            "original text" : ["translation 1", "translation 2"],
            "original text2" : ["translation 3", "translation 4"],
        }
        """
        self.general_glossary = pd.read_parquet(glossary_parquet_path).to_dict("index")

        return

    def load_task_glossary(self, glossary_parquet_path, glossary_index):
        # raise NotImplementedError()

        glossary_dict = pd.read_parquet(glossary_parquet_path).to_dict("index")

        self.task_glossary[glossary_index] = glossary_dict

        return

    # def search_glossary(self, text, max_k=10, task_index=None, search_general_glossary=True):
    #     found_glossary = []
    #     task_glossary = {}
    #
    #     if task_index is not None:
    #         task_glossary = self.task_glossary[task_index]
    #
    #     for word in self.hanlp_model(text)['tok']:
    #         # search in task glossary first
    #         if word in task_glossary:
    #             found_glossary.append((word, self.general_glossary[word]))
    #         elif word in self.general_glossary and search_general_glossary:
    #             found_glossary.append((word, self.general_glossary[word]))
    #
    #     return found_glossary[:max_k]

    def batch_search_glossary(self, text_list, max_k=10, task_index=None, search_general_glossary=True, max_workers=8,
                              chunksize=1, k=None):
        def _temp_search_glossary(text, max_k=max_k, task_index=task_index,
                                  search_general_glossary=search_general_glossary):
            return self.search_glossary(text, max_k=max_k, task_index=task_index,
                                        search_general_glossary=search_general_glossary)
            pass

        # return process_map(_temp_search_glossary, text_list, max_workers=max_workers, chunksize=chunksize)
        return [_temp_search_glossary(t) for t in tqdm(text_list)]

    def search_glossary(self, text, max_k=10, task_index=None, search_general_glossary=True, k=None):
        if k is not None:
            max_k = k
        text = clean_text(text)

        found_glossary = {}

        if task_index is not None:
            task_glossary = self.task_glossary[task_index]
            found_glossary.update(self.search_task_glossary(text, task_glossary, max_k=max_k))

        if len(found_glossary) < max_k:
            general_glossary = self.search_general_glossary(text, max_k=max_k - len(found_glossary))
            for k in general_glossary:
                if k in found_glossary:
                    found_glossary[k] = found_glossary[k] | general_glossary[k]
                else:
                    found_glossary[k] = general_glossary[k]

        return found_glossary

    def search_general_glossary(self, text, max_k=10):
        return get_glossary(clean_text(text), self.general_glossary, max_k=max_k)
        # raise NotImplementedError()

    def search_task_glossary(self, text, glossary_index, max_k=10):
        return get_glossary(clean_text(text), glossary_index, max_k=max_k)
        # raise NotImplementedError()

    def render_prompt(self,
                      source_text,
                      glossary_data: list = [],
                      ref_trans_data: list = [],
                      target_language='English',
                      **kwargs):

        return self.prompt_template.render(
            source_text=source_text,
            glossary_data=serialize_str(glossary_data),
            ref_trans_data=serialize_str(ref_trans_data),
            target_language=target_language,
            **kwargs
        )
