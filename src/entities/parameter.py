from pydantic import BaseModel

class ExtractParametersInput(BaseModel):
    question: str

class ExtractParametersOutput(BaseModel):
    city_name: str = ""
    city_code: str = ""
    uf: str = ""
    medicine: str = ""
