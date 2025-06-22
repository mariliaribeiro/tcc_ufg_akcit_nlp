from langchain.agents import Tool

from src.api.routes.routes import get_horus_medicine_stock
from src.connetion.chat_model import LLMModel
from src.connetion.embeddings import EmbeddingsModel
from src.connetion.graph_db import KgDatabaseConnetion
from src.kg.graph_rag import GraphRAG

llm_provider = "google"
temperature = 0
max_tokens = None

llm = LLMModel(provider=llm_provider, temperature=temperature, max_tokens=max_tokens).llm

e_provider = "hf"
embedding = EmbeddingsModel(
    provider=e_provider,
).embeddings

db = KgDatabaseConnetion(
    llm=llm,
    embedding=embedding,
)

grag = GraphRAG(chat_model=llm, db=db)

horus_medicine_stock_tool = Tool(
    name="GetHorusMedicineStock",
    func=get_horus_medicine_stock,
    description="Use this tool to get current weather for a city.",
)

medicine_usage_instructions_tools = Tool(
    name="MedicineUsageInstructions",
    func=grag.retriever,
    description="Use this tool to get medicine usage instructions.",
)
