from pydantic import BaseModel, Field

class CityCodeInput(BaseModel):
    city_name: str = Field(..., description="Name of the city")
    uf: str = Field(..., description="Two-letter state abbreviation (UF), e.g., 'PB', 'SP', 'RJ'")
