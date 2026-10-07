from pathlib import Path

from .regex_ast import Regex
from .ast_to_dot import ast_to_dot


def render_regex_AST(root: Regex) -> Path:
    graph = ast_to_dot(root)
    image_dir_name = Path("images")
    dot_dir_name = Path("dot")
    file_name = "regex_ast"

    image_dir_name.mkdir(parents=True, exist_ok=True)
    dot_dir_name.mkdir(parents=True, exist_ok=True)
    image_path = graph.render(
        filename=f"{file_name}.dot",
        directory=dot_dir_name,
        outfile=image_dir_name / f"{file_name}.svg",
        format="svg",
    )
    return Path(image_path)
