from dataclasses import dataclass, field

from langchain.agents import AgentType, initialize_agent
from langchain.agents.agent import AgentExecutor
from langchain.memory import ConversationSummaryMemory

from src.agents.tools.tools import MyTools
from src.config import EMBEDDING_PROVIDER, LLM_MAX_TOKENS, LLM_PROVIDER, LLM_TEMPERATURE
from src.connetion.chat_model import LLMModel
from src.connetion.embeddings import EmbeddingsModel


@dataclass
class MyAgent:
    """
    Classe responsável pela orquestração do agente.
    """

    llm_provider: str = LLM_PROVIDER
    llm_temperature: float = LLM_TEMPERATURE
    llm_max_tokens: int = LLM_MAX_TOKENS
    embedding_provider: str = EMBEDDING_PROVIDER

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

        # Criando uma instância de ConversationBufferMemory para criar a memória
        memory = ConversationSummaryMemory(
            llm=llm, memory_key="chat_history", return_messages=True
        )

        # Intanciando o agente e passando os recursos necessários
        self.agent = initialize_agent(
            tools,
            llm,
            agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
            memory=memory,
            verbose=True,
        )

    def invoke(self, question: str) -> str:
        return self.agent.run(question)
