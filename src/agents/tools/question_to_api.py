from dataclasses import dataclass
from typing import Any

from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    PromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain_core.output_parsers import StrOutputParser

from src.agents.prompt_templates.question_to_api import (
    SYSTEM_TEMPLATE_RETRIEVER,
    SYSTEM_TEMPLATE_STRUCTURED_OUTPUT,
)
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

        system_template = SYSTEM_TEMPLATE_STRUCTURED_OUTPUT
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
        print(prompt_template)

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
        system_template = SYSTEM_TEMPLATE_RETRIEVER
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
