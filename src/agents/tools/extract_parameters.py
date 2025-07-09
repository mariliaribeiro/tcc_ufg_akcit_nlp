from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from src.entities.parameter import ExtractParametersOutput
from src.connection.chat_model import LLMModel
from src.config import LLM_MAX_TOKENS, LLM_PROVIDER, LLM_TEMPERATURE
from src.agents.tools.city_lookup import GetCityCode
import json


llm_provider = LLM_PROVIDER
llm_temperature = LLM_TEMPERATURE
llm_max_tokens = LLM_MAX_TOKENS

llm = LLMModel(
    provider=llm_provider,
    temperature=llm_temperature,
    max_tokens=llm_max_tokens,
).llm

def extract_parameters_from_question(question: str) -> dict:
    prompt = PromptTemplate(
        input_variables=["question"],
        template=(
            "Extraia da pergunta abaixo o nome do medicamento, o nome do municipio(ou nome da cidade) e a sigla da UF (estado brasileiro). "
            "Retorne um JSON com as chaves: 'medicamento', 'nome_municipio', 'codigo_municipio', 'uf'. "
            "Se não encontrar algum valor, retorne string vazia para aquele campo.\n"
            "Pergunta: {question}"
        )
    )

    chain = prompt | llm | StrOutputParser()
    result = chain.invoke({"question": question})

    try:
        result = result.strip()
        if result.startswith("```"):
            result = result.split("```")[1].strip()
 
        if result.startswith("json"):
            result = result[len("json"):].strip()
        
        data = json.loads(result)

        if (data.get("nome_municipio") != ""):
            if (data.get("uf") != ""):
                codigo_municipio = GetCityCode(data.get("nome_municipio"), data.get("uf"))
                if codigo_municipio:
                    data["codigo_municipio"] = codigo_municipio

        return ExtractParametersOutput(**data)
    except Exception as e:
        print("Erro ao fazer o parsing do JSON:", e)
        return {"medicamento": "", "nome_municipio": "", "codigo_municipio": "", "uf": ""}
    