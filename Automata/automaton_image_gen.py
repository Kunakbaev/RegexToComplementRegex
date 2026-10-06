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
    dir_name: Path = Path("images"),
) -> Path:
    graph = automaton_to_dot(automaton)
    dir_name.mkdir(parents=True, exist_ok=True)

    image_path = graph.render(
        filename=file_name,
        directory=dir_name,
        format="svg",
    )
    return Path(image_path)
