"""
Monta o grafo:

    [classificar] --> tem prazo? --sim--> [calcular_prazo] --> FIM
                                 --não--> FIM
"""

from langgraph.graph import END, StateGraph

from src.graph.nodes import (
    node_calcular_prazo,
    node_classificar,
    rotear_apos_classificacao,
)
from src.graph.state import GraphState


def build_graph():
    grafo = StateGraph(GraphState)

    grafo.add_node("classificar", node_classificar)
    grafo.add_node("calcular_prazo", node_calcular_prazo)

    grafo.set_entry_point("classificar")

    grafo.add_conditional_edges(
        "classificar",
        rotear_apos_classificacao,
        {
            "calcular_prazo": "calcular_prazo",
            "fim": END,
        },
    )
    grafo.add_edge("calcular_prazo", END)

    return grafo.compile()