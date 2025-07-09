from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from src.entities.parameter import ExtractParametersOutput
from src.connection.chat_model import LLMModel
from src.config import LLM_MAX_TOKENS, LLM_PROVIDER, LLM_TEMPERATURE
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
            "Extraia da pergunta abaixo o nome do medicamento(medicine), o nome da cidade(city_name) e a sigla da UF(uf) (estado brasileiro). "
            "Retorne um JSON com as chaves: 'medicine', 'city_name', 'city_code', 'uf'. "
            "Se não encontrar algum valor, retorne string vazia para aquele campo.\n"
            "Pergunta: {question}"
        )
    )

    chain = prompt | llm | StrOutputParser()
    result = chain.invoke({"question": question})
    print("Resposta do LLM:", result)
    try:
        result = result.strip()
        if result.startswith("```"):
            result = result.split("```")[1].strip()
 
        if result.startswith("json"):
            result = result[len("json"):].strip()
        
        data = json.loads(result)

        return ExtractParametersOutput(**data)
    except Exception as e:
        print("Erro ao fazer o parsing do JSON:", e)
        return {"medicine": "", "city_name": "", "city_code": "", "uf": ""}