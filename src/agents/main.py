from dataclasses import dataclass, field

from langchain.agents import AgentType, initialize_agent
from langchain.agents.agent import AgentExecutor

from src.agents.tools.tools import MyTools
from src.connetion.chat_model import LLMModel
from src.connetion.embeddings import EmbeddingsModel


@dataclass
class MyAgent:
    """
    Classe responsável pela orquestração do agente.
    """

    llm_provider: str = "google"
    llm_temperature: float = 0
    llm_max_tokens: int = None
    embedding_provider: str = "hf"

    agent: AgentExecutor = field(init=False, default=None)

    def __post_init__(self):
        llm = LLMModel(
            provider=self.llm_provider,
            temperature=self.llm_temperature,
            max_tokens=self.llm_max_tokens,
        ).llm
        embedding = EmbeddingsModel(
            provider=self.embedding_provider,
        ).embeddings

        tools = MyTools(llm=llm, embedding=embedding).tools

        self.agent = initialize_agent(
            tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
        )

    def invoke(self, question: str) -> str:
        return self.agent.run(question)
