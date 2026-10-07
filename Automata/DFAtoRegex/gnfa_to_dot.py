from graphviz import Digraph

from RegexToAST.regex_to_string import regex_to_string

from ..automaton_to_dot import (
    ACCEPTING_STATE_COLOR,
    REGULAR_STATE_COLOR,
    START_STATE_COLOR,
    setup_graph_style,
)
from .generalized_nfa import GNFA


def gnfa_to_dot(gnfa: GNFA) -> Digraph:
    graph = Digraph("generalized_nfa")
    setup_graph_style(graph)

    for state in sorted(gnfa.states):
        if state == gnfa.start_state:
            label = "S"
            shape = "circle"
            fill_color = START_STATE_COLOR
        elif state == gnfa.accepting_state:
            label = "F"
            shape = "doublecircle"
            fill_color = ACCEPTING_STATE_COLOR
        else:
            label = f"q{state}"
            shape = "circle"
            fill_color = REGULAR_STATE_COLOR

        graph.node(
            f"state_{state}",
            label,
            shape=shape,
            fillcolor=fill_color,
        )

    graph.node(
        "start_pointer",
        "",
        shape="point",
        width="0.15",
        color="#FFFFFF",
        fillcolor="#FFFFFF",
    )
    graph.edge("start_pointer", f"state_{gnfa.start_state}")

    for source, regex, destination in gnfa.iterEdges():
        graph.edge(
            f"state_{source}",
            f"state_{destination}",
            label=regex_to_string(regex),
        )

    return graph
