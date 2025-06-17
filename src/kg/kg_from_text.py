from dataclasses import dataclass, field
from typing import Any, List, Tuple

from langchain_core.documents import Document
from langchain_experimental.graph_transformers import LLMGraphTransformer

from src.config import BUILD_GRAPH_AUTO
from src.connetion.chat_model import LLMModel
from src.connetion.embeddings import EmbeddingsModel
from src.connetion.graph_db import KgDatabaseConnetion
from src.constants import ALLOWED_NODES, ALLOWED_RELATIONSHIPS, NODE_PROPERTIES
from src.utils.dataviz import export_graph_documment_to_html, plot_graph_documents


@dataclass
class KGFromText:
    """
    Classe responsável pela extração dos grafos de conhecimento de textos.
    """

    llm: LLMModel
    embeddings: EmbeddingsModel
    db: KgDatabaseConnetion = field(init=False, default=None)
    graph_documents: Any = field(init=False, default=None)  #  List[GraphDocument]

    def __post_init__(self):
        self.db = KgDatabaseConnetion(llm=self.llm, embedding=self.embeddings)

    async def get_kg(self, chunk_documents: List[Document]):
        """
        Função que gera os grafos de conhecimento utilizando um modelo LLM.
        Lembrar de chamar essa função com await.

        Args:
            chunk_documents (List[Document]): Chunks de texto no formato de documento do langchain.
        """

        if BUILD_GRAPH_AUTO:
            llm_gt = LLMGraphTransformer(
                llm=self.llm,
            )
        else:
            llm_gt = LLMGraphTransformer(
                llm=self.llm,
                allowed_nodes=ALLOWED_NODES,
                allowed_relationships=ALLOWED_RELATIONSHIPS,
                node_properties=NODE_PROPERTIES,
            )
        self.graph_documents = await llm_gt.aconvert_to_graph_documents(chunk_documents)
        return self

    def plot_and_export_visualization(
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

    def save(self):
        """
        Função responsável por salvar o grafo de conhecimento extraído do texto no banco de dados.
        Salva o grafo e os ebeddings textuais dos chunk documents.
        """

        # Salvando o grafo
        self.db.graph.save(graph_documents=self.graph_documents)

        # Salvando o embedding do texto dos chunks
        # Por hora vamos utilizar este método, mas é possível utilizar os demais métodos do vetor.
        self.db.vector.save_embeddings_from_existing_graph()
        # Outros métodos possíveis
        # self.db.vector.save_embeddings_from_documents(chunk_documents)
        # self.db.vector.add_documents_embeddings(chunk_documents)
        return self
