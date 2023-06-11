import os
import json

from .utils import xstr

from langchain.document_loaders import ApifyDatasetLoader
from langchain.document_loaders.base import Document
from langchain.indexes import VectorstoreIndexCreator
from langchain.utilities import ApifyWrapper
from langchain.document_loaders import CSVLoader
from langchain.chat_models import ChatOpenAI


class LLMWrapper():
    def __init__(self):
        with open("data/tokens.json", 'rb') as file:
            tokens = json.load(file)

        os.environ["OPENAI_API_KEY"] = tokens["openai"]
        os.environ["APIFY_API_TOKEN"] = tokens["apify_token"]

        self.apify = ApifyWrapper()
        self.apify_data_indices = {}
        self.apify_dataset = {}

        self.osm_data_indices = {}
        self.osm_dataset = {}

        self.llm = ChatOpenAI(temperature=0.0, model_name='gpt-3.5-turbo')

    def load_osm(self, data_id):
        if "dataset" not in self.osm_dataset:
            with open(f"data/{data_id}.json", 'rb') as file:
                self.osm_dataset["dataset"] = json.load(file)

        if data_id not in self.osm_data_indices:
            loader = CSVLoader(file_path=f'data/{data_id}.csv', source_column='name')

            self.osm_data_indices[data_id] = VectorstoreIndexCreator().from_loaders([loader])

    def answer_osm(self, data_id, question):
        result = self.osm_data_indices[data_id].query_with_sources(question, llm=self.llm)

        result_sources = []
        sources = result['sources'].split(",")
        for source in sources:
            if source in result['answer']:
                formatted_source = source.strip()
                if formatted_source in self.osm_dataset["dataset"]:
                    result_sources.append(self.osm_dataset["dataset"][formatted_source])

        return result_sources

    def load_apify(self, data_id):
        if "dataset" not in self.apify_dataset:
            with open("data/apify_result.json", 'rb') as file:
                self.apify_dataset["dataset"] = json.load(file)

        if data_id not in self.apify_data_indices:
            loader = CSVLoader(file_path=f'data/{data_id}.csv', source_column='title')

            self.apify_data_indices[data_id] = VectorstoreIndexCreator().from_loaders([loader])

    def answer_apify(self, data_id, question):
        result = self.apify_data_indices[data_id].query_with_sources(question, llm=self.llm)

        result_sources = []
        sources = result['sources'].split(",")
        for source in sources:
            if source.strip() in result['answer']:
                formatted_source = source.strip()
                if formatted_source in self.apify_dataset["dataset"]:
                    result_sources.append(self.apify_dataset["dataset"][formatted_source])

        return result_sources
