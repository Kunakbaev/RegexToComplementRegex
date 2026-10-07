from pathlib import Path

from .generalized_nfa import GNFA
from .gnfa_to_dot import gnfa_to_dot


def render_gnfa(
    gnfa: GNFA,
    file_name: str,
    image_dir_name: Path = Path("images/state_elimination"),
    dot_dir_name: Path = Path("dot/state_elimination"),
) -> Path:
    graph = gnfa_to_dot(gnfa)
    image_dir_name.mkdir(parents=True, exist_ok=True)
    dot_dir_name.mkdir(parents=True, exist_ok=True)

    image_path = graph.render(
        filename=f"{file_name}.dot",
        directory=dot_dir_name,
        outfile=image_dir_name / f"{file_name}.svg",
        format="svg",
    )
    return Path(image_path)
