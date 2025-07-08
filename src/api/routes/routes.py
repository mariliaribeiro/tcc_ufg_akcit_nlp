from fastapi import APIRouter, Depends, Body
from pydantic import BaseModel
import requests

from src.api.schemas.request.horus import HorusMedicineStockRequest
from src.api.schemas.response.horus import HorusMedicineStockResponse
from src.config import API_DADOS_ABERTOS, HORUS_ROUTE
from src.agents.main import MyAgent
from src.api.routes.horus_utils import get_horus_medicine_stock

router = APIRouter()


@router.get(HORUS_ROUTE, tags=["BNAFAR"], response_model=HorusMedicineStockResponse)
def get_horus_medicine_stock_route(request: HorusMedicineStockRequest = Depends()):
    return get_horus_medicine_stock(request)


class AgentChatRequest(BaseModel):
    message: str

class AgentChatResponse(BaseModel):
    response: str

@router.post("/api/chat", response_model=AgentChatResponse)
def agent_chat(request: AgentChatRequest):
    agent = MyAgent()
    resposta = agent.invoke(request.message)
    return AgentChatResponse(response=resposta)
