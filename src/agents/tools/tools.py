from dataclasses import dataclass, field
from typing import Any, List

from langchain.agents import Tool
from langchain.tools import Tool

from src.agents.tools.graph_rag import GraphRAG
from src.agents.tools.question_to_api import QuestionToAPI
from src.api.routes.horus_utils import get_horus_medicine_stock
from src.api.schemas.request.horus import HorusMedicineStockRequest
from src.connection.graph_db import KgDatabaseConnection
from src.agents.tools.extract_parameters import EntityExtractor

@dataclass
class MyTools:
    """
    Classe responsável pela definição das tools.
    """

    llm: Any
    embedding: Any

    tools: List[Tool] = field(init=False, default_factory=list)

    def __post_init__(self):
        db = KgDatabaseConnection(
            llm=self.llm,
            embedding=self.embedding,
        )

        grag = GraphRAG(llm=self.llm, db=db)

        qapi = QuestionToAPI(
            llm=self.llm, schema=HorusMedicineStockRequest, api_func=get_horus_medicine_stock
        )

        ee = EntityExtractor(llm=self.llm)

        medicine_usage_instructions_tools = Tool(
            name="MedicineUsageInstructions",
            func=grag.retriever,
            description="Use this tool to get medicine usage instructions.",
        )
        
        horus_medicine_stock_tool = Tool(
            name="GetHorusMedicineStock",
            func=qapi.retriever,
            description="Use this tool to obtain information about medicine stocks in Brazilian cities and states. Only when the city code (codigo_municipio) and the state (uf) are defined, execute this function.",
        )

        extract_parameters_tool = Tool(
            name="ExtractParameters",
            func=ee.retriever,
            description="Use this tool to extract the city, state and medicine entities from the user's question. Expect a dictionary with 'nome_municipio', 'codigo_municipio', 'uf' and 'medicamento'.",
        )

        self.tools = [extract_parameters_tool, horus_medicine_stock_tool, medicine_usage_instructions_tools]
