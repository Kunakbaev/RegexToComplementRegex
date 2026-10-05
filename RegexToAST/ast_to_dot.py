from itertools import count

from graphviz import Digraph

from .regex_ast import Alt, Concat, EmptySet, Epsilon, OneOrMore, Regex, Star, Symbol


NODE_FILL_COLORS = {
    Symbol: "#00C853",
    Epsilon: "#C49A00",
    EmptySet: "#FF6D00",
    Star: "#2962FF",
    OneOrMore: "#AA00FF",
    Alt: "#D50000",
    Concat: "#37474F",
}


def setup_graph_style(graph: Digraph) -> None:
    graph.attr(
        bgcolor="#000000",
        rankdir="TB",
        pad="0.25",
        nodesep="0.35",
        ranksep="0.5",
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
        penwidth="1.5",
        arrowsize="0.8",
    )


def ast_to_dot(root: Regex) -> Digraph:
    graph = Digraph("regex_ast")
    setup_graph_style(graph)

    identifiers = count()

    def visit(node: Regex) -> str:
        node_id = f"n{next(identifiers)}"
        fill_color = NODE_FILL_COLORS[type(node)]
        graph.node(node_id, node.label, fillcolor=fill_color)

        for child in node.children:
            child_id = visit(child)  # this is a tree, thus no cycles
            graph.edge(node_id, child_id)

        return node_id

    visit(root)
    return graph
