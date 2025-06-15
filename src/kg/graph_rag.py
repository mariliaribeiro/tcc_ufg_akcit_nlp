from dataclasses import dataclass, field

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough

from src.connetion.chat_model import LLMModel
from src.connetion.graph_db import KgDatabaseConnetion


@dataclass
class GraphRAG:
    """
    Classe responsável pelo GraphRAG.
    """

    llm: LLMModel
    db: KgDatabaseConnetion
    template: str = """Answer the question based only on the following context:
    {context}

    Question: {question}
    """

    def retriever(self, question: str) -> str:
        """
        Método responsável pelo fluxo de execussão do GraphRAG.

        Args:
            question (str):  Pergunta a ser respondida.

        Returns:
            str: Resposta da pergunta.
        """

        structured_data = self.db.qa_chain.search(question=question)
        unstructured_data = self.db.vector.similarity_search(question=question)

        final_data = f"""Structured data:
            {structured_data}
            Unstructured data:
            {"#Document ".join(unstructured_data)}
        """
        print(f"\n\n Final data in context: {final_data}")

        prompt = ChatPromptTemplate.from_template(self.template)
        chain = (
            RunnableParallel(
                {
                    "context": self.retriever,
                    "question": RunnablePassthrough(),
                }
            )
            | prompt
            | self.llm
            | StrOutputParser()
        )
        response = chain.invoke(question)
        return response
