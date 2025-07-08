from dataclasses import dataclass, field
from typing import Any, List

from langchain.agents import Tool
from langchain.tools import Tool

from src.agents.tools.graph_rag import GraphRAG
from src.agents.tools.question_to_api import QuestionToAPI
from src.api.routes.horus_utils import get_horus_medicine_stock
from src.api.schemas.request.horus import HorusMedicineStockRequest
from src.connection.graph_db import KgDatabaseConnection
from src.utils.city_lookup import GetCityCode
import ast

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

        def city_tool_adapter(input_str: str) -> str:
            data = ast.literal_eval(input_str.strip().strip("`").strip())
            city_name = data.get("city_name")
            uf = data.get("uf")
            return GetCityCode(city_name, uf)

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

        city_lookup_tool = Tool(
            name="GetCityCode",
            func=city_tool_adapter,
            description=(
                "Exclusively use this tool to answer questions about the IBGE code of Brazilian cities or municipalities. If the user asks about the IBGE code of any city, call this tool without fail. To get the IBGE code of the city, consult the MongoDB 'cities' collection, informing the name of the city and the UF, ALWAYS. Expect a dictionary with 'city_name' and 'uf'. Always consider the UF as an abbreviation (e.g.: 'PE', 'SP', 'GO')."
            )
        )

        self.tools = [medicine_usage_instructions_tools, horus_medicine_stock_tool, city_lookup_tool]
