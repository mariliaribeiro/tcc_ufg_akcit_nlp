from dataclasses import dataclass

from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    PromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain_core.output_parsers import StrOutputParser

from src.agents.prompt_templates.graph_rag import CONTEXT, SYSTEM_TEMPLATE
from src.connetion.chat_model import LLMModel
from src.connetion.graph_db import KgDatabaseConnetion


@dataclass
class GraphRAG:
    """
    Classe responsável pelo GraphRAG.
    """

    llm: LLMModel
    db: KgDatabaseConnetion

    def get_context(self, question: str) -> str:
        """
        Método responsável pelo fluxo de execussão do GraphRAG.

        Args:
            question (str):  Pergunta a ser respondida.

        Returns:
            str: Resposta da pergunta.
        """

        structured_data = self.db.qa_chain.search(question=question)
        unstructured_data = self.db.vector.similarity_search(question=question)

        context = CONTEXT.format(
            structured_data=structured_data, unstructured_data="\n".join(unstructured_data)
        )
        print(f"\n\n Context:\n {context}")
        return context

    def retriever(self, question: str) -> str:
        system_template = SYSTEM_TEMPLATE

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
        context = self.get_context(question=question)
        prompt_template.format_messages(context=context, question=question)

        output_parser = StrOutputParser()
        review_chain = prompt_template | self.llm | output_parser

        return review_chain.invoke({"context": context, "question": question})
