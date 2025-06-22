from dataclasses import dataclass, field
from typing import Dict, List, Tuple

from langchain_community.graphs.graph_document import GraphDocument
from langchain_core.documents import Document
from langchain_neo4j import GraphCypherQAChain, Neo4jGraph, Neo4jVector

from src.config import NEO4J_PASSWORD, NEO4J_URI, NEO4J_USERNAME
from src.connetion.chat_model import LLMModel
from src.connetion.embeddings import EmbeddingsModel


@dataclass
class Graph:
    """
    Classe responsável pelas operações do grafo.
    """

    graph: Neo4jGraph = field(init=False, default=None)

    def __post_init__(self):
        self.connection()

    def connection(self):
        """
        Estabelece a conexão com o Neo4J
        """
        self.graph = Neo4jGraph(
            url=NEO4J_URI,
            username=NEO4J_USERNAME,
            password=NEO4J_PASSWORD,
            refresh_schema=True,
            enhanced_schema=True,
        )
        return self

    def save(self, graph_documents: List[GraphDocument]):
        """
        Salva o grafo de conhecimento no banco de dados incluindo o índice e embeddings dos chunks
        textuais identificados pelo Nó Document.
        O parâmetro include_source igual a True, faz com que o texto original também seja salvo no banco.
        O parâmetro baseEntityLabel é utilizado na indexação e cria um rótulo secundário __Entity__.

        Args:
            graph_documents (List[GraphDocument]): Documentos no formato de grafos.
        """

        self.graph.add_graph_documents(graph_documents, baseEntityLabel=True, include_source=True)
        return self


@dataclass
class QAChain:
    """
    Classe responsável pelas operações da chain question ansewering.
    """

    llm: LLMModel
    graph: Neo4jGraph
    qa_chain: GraphCypherQAChain = field(init=False, default=None)

    def __post_init__(self):
        self.connection()

    def connection(self):
        """
        Estabele conexão coma a chian de question and answering que transforma a pergunta em
        consulta Cypher.
        """

        self.qa_chain = GraphCypherQAChain.from_llm(
            self.llm,
            graph=self.graph,
            verbose=True,
            top_k=10,
            return_intermediate_steps=True,
            return_direct=False,
            allow_dangerous_requests=True,
        )
        return self

    def search(self, question: str) -> List:
        """
        Método responsável por fazer a consulta no grafo de conhecimento.

        Args:
            question (str): Pergunta do usuário.

        Returns:
            List: Lista com os nós e relacionamentos relevantes para a consulta do grafo.
        """
        response = self.qa_chain.invoke({"query": question})
        print("** QA chain results **")
        print(response)

        # Resposta em texto
        result = response.get("result", "")

        # Resposta com nós e relacionamentos do grafo
        intermediate_steps = response.get("intermediate_steps", [])
        context = []
        for i in intermediate_steps:
            context.extend(i.get("context", []))
        print(context)
        if not context:
            context = ["Não sei responder com base nos dados estruturados."]
        return context


@dataclass
class Vector:
    """
    Classe responsável pelas operações do vetor de embeddings do grafo.
    """

    embedding: EmbeddingsModel
    vector: Neo4jVector = field(init=False, default=None)

    def __post_init__(self):
        self.connection()

    def connection(self):
        """
        Função que cria a conexão com o vector stor do Neo4j.
        """

        self.vector = Neo4jVector(
            embedding=self.embedding,
            url=NEO4J_URI,
            username=NEO4J_USERNAME,
            password=NEO4J_PASSWORD,
        )
        return self

    def save_embeddings_from_existing_graph(self):
        """
        Salva os embeddings do texto do nó Documentos (contém o conteúdo do chunk) no vector store
        para um grafo existente.
        """
        self.vector.from_existing_graph(
            embedding=self.embedding,
            search_type="hybrid",
            node_label="Document",
            text_node_properties=["text"],
            embedding_node_property="embedding",
        )
        return self

    def save_embeddings_from_documents(self, documents: List[Document]):
        """
        Salva os embeddings do texto do nó Documentos (contém o conteúdo do chunk) no vector store
        para documentos passados como parâmetro.

        Args:
            documents (List[Document]): Documentos de texto.
        """
        self.vector.from_documents(
            documents,
            self.embedding,
            index_name="vector",  # vector by default
            node_label="Document",  # Chunk by default
            text_node_property="text",  # text by default
            embedding_node_property="embedding",  # embedding by default
            create_id_index=True,  # True by default
        )
        return self

    def add_documents_embeddings(self, documents: List[Document]):
        """
        Salva os embeddings do texto do nó Documentos (contém o conteúdo do chunk) no vector store
        para documentos passados como parâmetro.

        Args:
            documents (List[Document]): Documentos de texto.
        """
        self.vector.add_documents(
            documents,
            # ids=[ "langchain" ],
        )
        return self

    def show_vector_constraints_and_indexes(self) -> Tuple[List[Dict], List[Dict]]:
        """
        Retorna as constraints e índices criados no vetor do grafo.
        """

        constraints = self.vector.query("SHOW CONSTRAINTS")
        indexes = self.vector.query(
            """SHOW INDEXES
            YIELD name, type, labelsOrTypes, properties, options
            WHERE type = 'VECTOR'
            """
        )

        return constraints, indexes

    def similarity_search(self, question: str, threshold: float = 0.7) -> List[str]:
        """
        Retorna uma lista de documentos mais similares.
        Retorna somente o conteúdo do page_content.

        Args:
            question (str): Pergunta.

            threshold (float, optional): Define limite de corte para a busca de similaridade.
            Defaults to 0.5.

        Returns:
            List[str]: Lista de texto similares.
        """
        similarity_results = self.vector.similarity_search(
            question, similarity_score_threshold=threshold
        )
        print("** Vector similarity results **")
        print(similarity_results)

        context = [i.page_content for i in similarity_results]
        if not context:
            context = ["Não sei responder com base nos dados não estruturados."]
        return context


@dataclass
class KgDatabaseConnetion:
    """
    Classe responsável pela conexão com o banco de dados que armazena o grafo de conhecimento.
    """

    llm: LLMModel
    embedding: EmbeddingsModel
    vector: Vector = field(init=False, default=None)
    graph: Graph = field(init=False, default=None)
    qa_chain: QAChain = field(init=False, default=None)

    def __post_init__(self):
        self.vector = Vector(embedding=self.embedding)
        self.graph = Graph()
        self.qa_chain = QAChain(llm=self.llm, graph=self.graph.graph)
