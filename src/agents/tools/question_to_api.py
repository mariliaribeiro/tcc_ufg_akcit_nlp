from dataclasses import dataclass
from typing import Any

from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    PromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain_core.output_parsers import StrOutputParser

from src.connetion.chat_model import LLMModel


@dataclass
class QuestionToAPI:
    """
    Classe responsável por converter a pergunta do usuário em dados estruturados para realizar uma
    consulta de API.
    """

    llm: LLMModel
    schema: Any
    api_func: Any

    def get_structured_output(self, question: str) -> Any:
        """
        Método responsável por extrair dados estruturados de um texto em linguagem natural.

        Args:
            question (str):  Pergunta a ser respondida.

        Returns:
            Any: Objeto do pydantic representando os dados estruturados.
        """

        system_template = """
        You are an expert extraction algorithm, specialized in extract API request params from user messagem to consult Horus API to get relavant medicine stock information by city and state.
        Only extract relevant information from the text as specified by the provided JSON schema. Do not generate any new information or exrta characters outside of the JSON schema.
        """
        system_prompt = SystemMessagePromptTemplate(
            prompt=PromptTemplate(template=system_template)
        )

        human_prompt = HumanMessagePromptTemplate(
            prompt=PromptTemplate(input_variables=["question"], template="{question}")
        )

        messages = [system_prompt, human_prompt]
        prompt_template = ChatPromptTemplate(
            input_variables=["question"],
            messages=messages,
        )
        prompt_template.format_messages(question=question)

        sllm = self.llm.with_structured_output(schema=self.schema)
        print("Structured LLM tool schema:\n", sllm.first.kwargs)
        chain = prompt_template | sllm

        return chain.invoke({"question": question})

    def call_api(self, question: str) -> dict:
        """
        Método responsável por realizar a consulta da API.

        Args:
            question (str):  Pergunta a ser respondida.

        Returns:
            dict: Resposta da API.
        """
        request = self.get_structured_output(question=question)
        print("Structured output used as API request:\n", request)
        return self.api_func(request)

    def retriever(self, question: str) -> str:
        system_template = """Your job is to answer questions about medicine stock from Brazilian 
        cities and states.
        Use the following context to answer questions. The context is given by structured data from
        from API response.
        Be as detailed as possible, but don't make up any information that's not from the context.
        If you don't know an answer, say you don't know.

        {context}
        """

        system_prompt = SystemMessagePromptTemplate(
            prompt=PromptTemplate(input_variables=["context"], template=system_template)
        )

        human_prompt = HumanMessagePromptTemplate(
            prompt=PromptTemplate(input_variables=["question"], template="{question}")
        )

        messages = [system_prompt, human_prompt]
        prompt_template = ChatPromptTemplate(
            input_variables=["context", "question"],
            messages=messages,
        )
        context = self.call_api(question=question)
        print("API response:\n", context)
        prompt_template.format_messages(context=context, question=question)

        output_parser = StrOutputParser()
        review_chain = prompt_template | self.llm | output_parser

        return review_chain.invoke({"context": context, "question": question})
