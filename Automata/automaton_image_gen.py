from collections.abc import Hashable
from pathlib import Path
from typing import TypeVar

from .automaton_to_dot import automaton_to_dot
from .finite_automaton import FiniteAutomaton


TransitionLabelType = TypeVar("TransitionLabelType", bound=Hashable)
TransitionValueType = TypeVar("TransitionValueType")


def render_automaton(
    automaton: FiniteAutomaton[TransitionLabelType, TransitionValueType],
    file_name: str = "automaton",
    image_dir_name: Path = Path("images"),
    dot_dir_name: Path = Path("dot"),
) -> Path:
    graph = automaton_to_dot(automaton)
    image_dir_name.mkdir(parents=True, exist_ok=True)
    dot_dir_name.mkdir(parents=True, exist_ok=True)

    image_path = graph.render(
        filename=f"{file_name}.dot",
        directory=dot_dir_name,
        outfile=image_dir_name / f"{file_name}.svg",
        format="svg",
    )
    return Path(image_path)
