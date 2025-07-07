# https://python.langchain.com/docs/integrations/text_embedding/

from dataclasses import dataclass, field
from typing import Any

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import OllamaEmbeddings
from langchain_openai import OpenAIEmbeddings


@dataclass
class EmbeddingsModel:
    """
    Classe responsável por instanciar o modelo de embeddings de acorodo com o provedor do modelo.
    """

    provider: str = "local"
    temperature: float = 0.7
    max_tokens: int = None
    embeddings: Any = field(init=False, default=None)

    def __post_init__(self):
        if self.provider == "local":
            self.embeddings = self.get_local_llm_model()
        if self.provider == "openai":
            self.embeddings = self.get_openai_llm_model()
        if self.provider == "google":
            self.embeddings = self.get_google_llm_model()
        if self.provider == "hf":
            self.embeddings = self.get_hf_llm_model()

    def get_local_llm_model(self):
        return OllamaEmbeddings(model="llama3")

    def get_openai_llm_model(self):
        return OpenAIEmbeddings(model="text-embedding-3-large")

    def get_google_llm_model(self):
        return GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    def get_hf_llm_model(self):
        return HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
