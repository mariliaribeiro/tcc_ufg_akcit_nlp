from langchain_core.output_parsers import StrOutputParser
from src.connection.chat_model import LLMModel
from src.agents.tools.city_lookup import GetCityCode
from src.agents.prompt_templates.extract_parameters import CONTEXT, SYSTEM_TEMPLATE
import json

from dataclasses import dataclass

from langchain.prompts import (
    PromptTemplate,
)

@dataclass
class EntityExtractor:
    """
    Classe responsável por extrair entidades de uma pergunta e gerar contexto com base nos dados extraídos.
    """

    llm: LLMModel

    def extract_entities(self, question: str) -> dict:
        prompt = PromptTemplate(input_variables=["question"], template=SYSTEM_TEMPLATE)
        output_parser = StrOutputParser()
        chain = prompt | self.llm | output_parser

        try:
            result = chain.invoke({"question": question}).strip()
            if result.startswith("```"):
                result = result.split("```")[1].strip()
            if result.lower().startswith("json"):
                result = result[4:].strip()
            data = json.loads(result)

            # Preenche código do município
            nome_municipio = data.get("nome_municipio", "")
            uf = data.get("uf", "")
            if nome_municipio and uf:
                data["codigo_municipio"] = GetCityCode(nome_municipio, uf) or ""

            return {
                "medicamento": data.get("medicamento", ""),
                "nome_municipio": nome_municipio,
                "codigo_municipio": data.get("codigo_municipio", ""),
                "uf": uf
            }
        except Exception as e:
            print("Erro ao fazer parsing do JSON:", e)
            return {
                "medicamento": "",
                "nome_municipio": "",
                "codigo_municipio": "",
                "uf": ""
            }
