from dataclasses import dataclass

from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    PromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain_core.output_parsers import StrOutputParser

from src.agents.prompt_templates.city_search import CONTEXT, SYSTEM_TEMPLATE
from src.agents.tools.city_lookup import GetCityCode
import ast

@dataclass
class CitySearch:
    """
    Classe responsável pelo consulta de código de cidade.
    """

    def get_context(self, codigo_municipio: str) -> str:
        """
        Método responsável pelo fluxo de execução do CitySearch.

        Args:
            question (str):  Pergunta com as informações da cidade e estado.

        Returns:
            str: Resposta da pergunta.
        """

        context = CONTEXT.format(
            codigo_municipio=codigo_municipio
        )
        print(f"\n\n Context:\n {context}")
        return context

    def retriever(self, question: str) -> str:
        data = ast.literal_eval(question.strip().strip("`").strip())
        nome_municipio = data.get("nome_municipio")
        codigo_uf = data.get("uf")
        codigo_municipio = GetCityCode(nome_municipio, codigo_uf)
        if not codigo_municipio:
            codigo_municipio = ""

        context = self.get_context(codigo_municipio=codigo_municipio)
       
        system_prompt = SystemMessagePromptTemplate(
            prompt=PromptTemplate(input_variables=["context"], template=SYSTEM_TEMPLATE)
        )

        human_prompt = HumanMessagePromptTemplate(
            prompt=PromptTemplate(input_variables=["question"], template="{question}")
        )

        messages = [system_prompt, human_prompt]
        prompt_template = ChatPromptTemplate(
            input_variables=["context", "question"],
            messages=messages,
        )

        prompt_template.format_messages(context=context, question=question)

        output_parser = StrOutputParser()
        review_chain = prompt_template | self.llm | output_parser

        return review_chain.invoke({"context": context, "question": question})
