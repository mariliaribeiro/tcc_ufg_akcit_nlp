from src.api.schemas.request.horus import HorusMedicineStockRequest
from src.api.schemas.response.horus import HorusMedicineStockResponse
from src.config import API_DADOS_ABERTOS, HORUS_ROUTE
import requests

def get_horus_medicine_stock(request: HorusMedicineStockRequest):
    url = f"{API_DADOS_ABERTOS}{HORUS_ROUTE}"
    params = request.model_dump(exclude_none=True)
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return f"Failed: {response.status_code}" 