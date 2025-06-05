from dataclasses import dataclass, field

from langchain_community.graphs import Neo4jGraph

from src.config import NEO4J_PASSWORD, NEO4J_URI, NEO4J_USERNAME


@dataclass
class KgDatabaseConnetion:
    """
    Classe responsável pela conexão com o banco de dados que armazena o grafo de conhecimento.
    """

    graph_conn: Neo4jGraph = field(init=False, default=None)

    def __post_init__(self):
        self.connection()

    def connection(self):
        """
        Estabelece a conexão com o Neo4J
        """
        self.graph_conn = Neo4jGraph(
            url=NEO4J_URI,
            username=NEO4J_USERNAME,
            password=NEO4J_PASSWORD,
            refresh_schema=False,
        )
