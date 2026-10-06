from collections.abc import Hashable
from typing import TypeVar

from graphviz import Digraph

from .finite_automaton import FiniteAutomaton, State


TransitionLabelType = TypeVar("TransitionLabelType", bound=Hashable)
TransitionValueType = TypeVar("TransitionValueType")

REGULAR_STATE_COLOR = "#2962FF"
START_STATE_COLOR = "#AA00FF"
ACCEPTING_STATE_COLOR = "#00C853"
START_ACCEPTING_STATE_COLOR = "#FF6D00"


def setup_graph_style(graph: Digraph) -> None:
    graph.attr(
        bgcolor="#000000",
        rankdir="LR",
        pad="0.25",
        nodesep="0.5",
        ranksep="0.75",
    )
    graph.attr(
        "node",
        shape="circle",
        style="filled",
        color="#FFFFFF",
        fontcolor="#FFFFFF",
        fontname="DejaVu Sans",
        penwidth="2",
    )
    graph.attr(
        "edge",
        color="#FFFFFF",
        fontcolor="#FFFFFF",
        fontname="DejaVu Sans",
        penwidth="1.5",
        arrowsize="0.8",
    )


def getStateColor(automaton: FiniteAutomaton, state: State) -> str:
    is_start = state == automaton.start_state
    is_accepting = automaton.isAccepting(state)

    if is_start and is_accepting:
        return START_ACCEPTING_STATE_COLOR
    if is_start:
        return START_STATE_COLOR
    if is_accepting:
        return ACCEPTING_STATE_COLOR
    return REGULAR_STATE_COLOR


def automaton_to_dot(
    automaton: FiniteAutomaton[TransitionLabelType, TransitionValueType],
) -> Digraph:
    graph = Digraph("finite_automaton")
    setup_graph_style(graph)

    for state in automaton.states:
        shape = "doublecircle" if automaton.isAccepting(state) else "circle"
        graph.node(
            f"state_{state}",
            f"q{state}",
            shape=shape,
            fillcolor=getStateColor(automaton, state),
        )

    graph.node(
        "start_pointer",
        "",
        shape="point",
        width="0.15",
        color="#FFFFFF",
        fillcolor="#FFFFFF",
    )
    graph.edge("start_pointer", f"state_{automaton.start_state}")

    labels_by_edge: dict[tuple[State, State], set[str]] = {}
    for source, label, destination in automaton.iterEdges():
        labels = labels_by_edge.setdefault((source, destination), set())
        labels.add(str(label))

    for (source, destination), labels in sorted(labels_by_edge.items()):
        graph.edge(
            f"state_{source}",
            f"state_{destination}",
            label=", ".join(sorted(labels)),
        )

    return graph
