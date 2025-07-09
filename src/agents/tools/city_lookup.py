from pymongo import MongoClient
from src.config import MONGO_URI, MONGO_DB_NAME, MONGO_CITY_COLLECTION

from pydantic import BaseModel, Field

def GetCityCode(nome_municipio, uf):
    print(f"Consulta no MongoDB: cidade='{nome_municipio}', uf='{uf}'")
    """
    Busca o código do município no MongoDB a partir do nome da cidade e UF.
    """
    client = MongoClient(MONGO_URI)
    db = client[MONGO_DB_NAME]
    collection = db[MONGO_CITY_COLLECTION]
    result = collection.find_one({
        "name": {"$regex": f"^{nome_municipio}$", "$options": "i"},
        "uf": uf
    })
    if result:
        print(f"Resultado: {result.get('horus_city_code')}")
        return result.get("horus_city_code")
    print("Resultado: não encontrado")
    return ""