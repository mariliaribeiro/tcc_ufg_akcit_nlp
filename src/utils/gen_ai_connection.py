from dataclasses import dataclass, field
import os
from typing import Any

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_huggingface import ChatHuggingFace
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI

load_dotenv('.env', override=True)


os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')
os.environ["GOOGLE_API_KEY"] = os.getenv('GOOGLE_API_KEY')
os.environ["GROQ_API_KEY"] = os.getenv('GROQ_API_KEY')
os.environ["HUGGINGFACEHUB_API_TOKEN"] = os.getenv('HUGGINGFACEHUB_API_TOKEN')

@dataclass
class LLMModel:
    """
    Classe responsável por instanciar provedores de modelos LLMs.
    """
    
    provider: str = "local"
    temperature: float = 0.7
    max_tokens: int = None
    llm: Any = field(init=False, default=None)

    def __post_init__(self):    
        if self.provider == "local":
            self.llm = self.get_local_llm_model()
        if self.provider == "openai":
            self.llm = self.get_openai_llm_model()
        if self.provider == "google":
            self.llm = self.get_google_llm_model()
        if self.provider == "groq":
            self.llm = self.get_groq_llm_model()
        if self.provider == "hf":
            self.llm = self.get_hf_llm_model()

    
    def get_local_llm_model(self):
        # return OllamaLLM(model="tinyllama:1.1b")
        return ChatOllama(
            model="tinyllama:1.1b",
            temperature=self.temperature,
            num_predict=self.max_tokens
        )
    
    def get_openai_llm_model(self):
        return ChatOpenAI(
            model="gpt-4o-mini", 
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )
    
    def get_google_llm_model(self):
        return ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )
    
    def get_groq_llm_model(self):
        return ChatGroq(
            model="llama3-8b-8192", 
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )
    
    def get_hf_llm_model(self):
        return ChatHuggingFace(
            model="mistralai/Mistral-7B-Instruct-v0.2", 
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )