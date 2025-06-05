from dataclasses import dataclass, field
from typing import Any, List, Tuple

from langchain_core.documents import Document
from langchain_experimental.graph_transformers import LLMGraphTransformer

from src.connetion.gen_ai_connection import LLMModel
from src.connetion.graph_db import KgDatabaseConnetion
from src.utils.dataviz import export_graph_documment_to_html, plot_graph_documents


@dataclass
class KGFromText:
    """
    Classe responsável pela extração dos grafos de conhecimento de textos.
    """

    llm: LLMModel
    db = KgDatabaseConnetion()
    graph_documents: Any = field(init=False, default=None)

    async def get_kg(self, chunk_documents: List[Document]):
        """
        Função que gera os grafos de conhecimento utilizando um modelo LLM.
        Lembrar de chamar essa função com await.

        Args:
            chunk_documents (List[Document]): Chunks de texto no formato de documento do langchain.
        """

        llm_gt = LLMGraphTransformer(llm=self.llm)
        self.graph_documents = await llm_gt.aconvert_to_graph_documents(chunk_documents)
        return self

    def plot_and_save_graph_visualization(
        self, file_name: str, figsize: Tuple = (10, 8), show_node_properties: bool = False
    ):
        """
        Plota e gera grafos de conhecimento em matplolib e HTML com o networkx a partir de uma lista de objetos GraphDocument.
        Espera-se que cada GraphDocument tenha atributos `.nodes` e `.relationships`
        com objetos Node e Relationship.

        Args:
            file_name (str):  nome do arquivo.
            figsize (tuple, optional): Dimensões da figura do matplotlib. Defaults to (10, 8).
            show_node_properties (bool, optional): Flag que indica se deve mostrar as propriedades do nó na figura do matplotlib. Defaults to False.
        """

        plot_graph_documents(
            graph_docs=self.graph_documents,
            figsize=figsize,
            show_node_properties=show_node_properties,
        )
        export_graph_documment_to_html(graph_docs=self.graph_documents, file_name=file_name)
        return self

    def save_graph_on_db(self):
        self.db.graph_conn.add_graph_documents(self.graph_documents)
        return self
