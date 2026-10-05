from pathlib import Path

from .regex_ast import Regex
from .ast_to_dot import ast_to_dot


def render_regex_AST(root: Regex) -> Path:
    graph = ast_to_dot(root)
    dir_name = Path("images")
    file_name = "regex_ast"

    dir_name.mkdir(parents=True, exist_ok=True)
    image_path = graph.render(
        filename=file_name,
        directory=dir_name,
        format="svg",
    )
    return Path(image_path)
