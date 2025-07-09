from langchain_core.output_parsers import StrOutputParser
from src.entities.parameter import ExtractParametersOutput
from src.connection.chat_model import LLMModel
from src.config import LLM_MAX_TOKENS, LLM_PROVIDER, LLM_TEMPERATURE
from src.agents.tools.city_lookup import GetCityCode
from src.agents.prompt_templates.extract_parameters import CONTEXT, SYSTEM_TEMPLATE
import json

from dataclasses import dataclass

from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    PromptTemplate,
    SystemMessagePromptTemplate,
)

@dataclass
class EntityExtractor:
    """
    Classe responsável por extrair entidades de uma pergunta e gerar contexto com base nos dados extraídos.
    """

    llm_provider = LLM_PROVIDER
    llm_temperature = LLM_TEMPERATURE
    llm_max_tokens = LLM_MAX_TOKENS

    llm = LLMModel(
        provider=llm_provider,
        temperature=llm_temperature,
        max_tokens=llm_max_tokens,
    ).llm   

    def get_context(self, question: str) -> str:
        """
        Extrai entidades e retorna o contexto estruturado.

        Args:
            question (str): Pergunta do usuário.

        Returns:
            str: Texto formatado com os dados extraídos.
        """
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

            structured_data = ExtractParametersOutput(**data)
        except Exception as e:
            print("Erro ao fazer parsing do JSON:", e)
            structured_data = ExtractParametersOutput(
                medicamento="", nome_municipio="", codigo_municipio="", uf=""
            )

        context = CONTEXT.format(structured_data=structured_data)
        print(f"\n\nContext:\n{context}")
        return context

    def retriever(self, question: str) -> str:
        """
        Executa o fluxo de geração de resposta usando o contexto extraído da pergunta.

        Args:
            question (str): Pergunta do usuário.

        Returns:
            str: Resposta final gerada pelo LLM.
        """
        system_prompt = SystemMessagePromptTemplate(
            prompt=PromptTemplate(input_variables=["structured_data"], template=CONTEXT)
        )
        human_prompt = HumanMessagePromptTemplate(
            prompt=PromptTemplate(input_variables=["question"], template="{question}")
        )

        prompt_template = ChatPromptTemplate(
            input_variables=["structured_data", "question"],
            messages=[system_prompt, human_prompt]
        )

        context = self.get_context(question)
        output_parser = StrOutputParser()
        chain = prompt_template | self.llm | output_parser

        return chain.invoke({"question": question, "structured_data": context})
