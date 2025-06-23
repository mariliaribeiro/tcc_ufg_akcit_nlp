from dataclasses import dataclass, field
from typing import Any, List

from langchain.agents import Tool

from src.agents.tools.graph_rag import GraphRAG
from src.agents.tools.question_to_api import QuestionToAPI
from src.api.routes.routes import get_horus_medicine_stock
from src.api.schemas.request.horus import HorusMedicineStockRequest
from src.connetion.graph_db import KgDatabaseConnetion


@dataclass
class MyTools:
    """
    Classe responsável pela definição das tools.
    """

    llm: Any
    embedding: Any

    tools: List[Tool] = field(init=False, default_factory=list)

    def __post_init__(self):
        db = KgDatabaseConnetion(
            llm=self.llm,
            embedding=self.embedding,
        )

        grag = GraphRAG(llm=self.llm, db=db)
        qapi = QuestionToAPI(
            llm=self.llm, schema=HorusMedicineStockRequest, api_func=get_horus_medicine_stock
        )

        medicine_usage_instructions_tools = Tool(
            name="MedicineUsageInstructions",
            func=grag.retriever,
            description="Use this tool to get medicine usage instructions.",
        )
        horus_medicine_stock_tool = Tool(
            name="GetHorusMedicineStock",
            func=qapi.retriever,
            description="Use this tool to get information about medicine stock from Brazilian cities and states.",
        )

        self.tools = [medicine_usage_instructions_tools, horus_medicine_stock_tool]
