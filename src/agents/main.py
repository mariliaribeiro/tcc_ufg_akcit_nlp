from langchain.agents import AgentType, initialize_agent

from src.agents.tools.tools import horus_medicine_stock_tool, medicine_usage_instructions_tools
from src.connetion.chat_model import LLMModel

provider = "google"
temperature = 0
max_tokens = None
llm = LLMModel(provider=provider, temperature=temperature, max_tokens=max_tokens).llm
tools = [horus_medicine_stock_tool, medicine_usage_instructions_tools]

agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
agent.invoke("O que você sabe sobre o estoque de medicamentos?")
