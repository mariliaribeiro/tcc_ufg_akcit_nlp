from pydantic import BaseModel

class ExtractParametersInput(BaseModel):
    question: str

class ExtractParametersOutput(BaseModel):
    medicamento: str = ""
    nome_municipio: str = ""
    codigo_municipio: str = ""
    uf: str = ""

