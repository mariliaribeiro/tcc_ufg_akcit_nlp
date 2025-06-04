from typing import List

from langchain_community.graphs.graph_document import GraphDocument
import matplotlib.pyplot as plt
import networkx as nx
from pyvis.network import Network

from src.config import REPORTS_HTML_DIR


def plot_graph_documents(graph_docs: List[GraphDocument], figsize=(10, 8), show_node_properties=False):
    """
    Plota grafos de conhecimento a partir de uma lista de objetos GraphDocument.
    Espera-se que cada GraphDocument tenha atributos `.nodes` e `.relationships`
    com objetos Node e Relationship.

    Parâmetros:
    - graph_docs: lista de objetos GraphDocument
    - figsize: tamanho da figura do matplotlib
    - show_node_properties: se True, mostra as propriedades dos nós no rótulo
    """

    G = nx.DiGraph()

    for doc in graph_docs:
        for node in doc.nodes:
            # Cria o rótulo com ou sem as propriedades
            if show_node_properties and node.properties:
                props_str = "\n".join(f"{k}: {v}" for k, v in node.properties.items())
                label = f"{node.id}\n[{node.type}]\n{props_str}"
            else:
                label = f"{node.id}\n[{node.type}]"

            # Adiciona os nós
            G.add_node(node.id, label=label, type=node.type)

        # Adiciona os relacionamentos com os tipos como rótulos de arestas
        for rel in doc.relationships:
            G.add_edge(rel.source.id, rel.target.id, label=rel.type)

    # Layout do grafo
    pos = nx.spring_layout(G, seed=42)

    node_labels = nx.get_node_attributes(G, 'label')

    # Define cores diferentes por tipo de nó
    node_colors = []
    type_color_map = {}
    color_palette = ['skyblue', 'lightgreen', 'salmon', 'violet', 'orange']
    color_index = 0

    for node_id, data in G.nodes(data=True):
        node_type = data.get("type", "default")
        if node_type not in type_color_map:
            type_color_map[node_type] = color_palette[color_index % len(color_palette)]
            color_index += 1
        node_colors.append(type_color_map[node_type])

    # Plot
    plt.figure(figsize=figsize)
    nx.draw(
        G,
        pos,
        labels=node_labels,
        with_labels=True,
        node_color=node_colors,
        node_size=3000,
        font_size=8,
        edge_color='gray'
    )

    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', font_size=8)
    plt.title("Grafo de Conhecimento")
    plt.axis('off')
    plt.show()


def export_graph_documment_to_html(graph_docs: List[GraphDocument], file_name:str):
    """
    Plota grafos de conhecimento em HTML com o networkx a partir de uma lista de objetos GraphDocument.
    Espera-se que cada GraphDocument tenha atributos `.nodes` e `.relationships`
    com objetos Node e Relationship.

    Parâmetros:
    - graph_docs: lista de objetos GraphDocument
    - file_name: nome do arquivo
    """
        
    # Construir grafo com networkx
    G = nx.DiGraph()

    # Adiciona nós e arestas
    for doc in graph_docs:
        for node in doc.nodes:
            G.add_node(node.id, label=node.id, type=node.type)

        for rel in doc.relationships:
            G.add_edge(rel.source.id, rel.target.id, label=rel.type)

    # Criar visualização com PyVis
    # net = Network(notebook=False, directed=True)
    net = Network(notebook=True, cdn_resources="in_line", directed=True)
    net.from_nx(G)

    # Adicionar rótulos aos nós
    for node in net.nodes:
        node['title'] = node['label']
        node['label'] = f"{node['label']} ({G.nodes[node['id']]['type']})"

    # Adicionar rótulos às arestas
    for edge in net.edges:
        edge['title'] = edge['label']
        edge['label'] = edge['label']
        
    net.save_graph(f"{REPORTS_HTML_DIR}/{file_name}.html")