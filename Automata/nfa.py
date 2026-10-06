from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from enum import Enum, auto

from .finite_automaton import FiniteAutomaton, State, Symbol


class SpecialTransitionSymbol(Enum):
    EPSILON = auto()

    def __str__(self) -> str:
        return "ε"


EPSILON = SpecialTransitionSymbol.EPSILON
TransitionLabel = Symbol | SpecialTransitionSymbol


@dataclass
class NFA(FiniteAutomaton[TransitionLabel, set[State]]):
    def __post_init__(self) -> None:
        super().__post_init__()

        if EPSILON in self.alphabet:
            raise ValueError("EPSILON must not be contained in the alphabet")

        for state, outgoing_transitions in enumerate(self.transitions):
            for label, destinations in outgoing_transitions.items():
                if label is not EPSILON and label not in self.alphabet:
                    raise ValueError(f"Transition label is not in the alphabet: {label}")
                for destination in destinations:
                    self.validateState(destination)

    def getDestinations(
        self,
        state: State,
        label: TransitionLabel,
    ) -> frozenset[State]:
        self.validateState(state)
        if label is not EPSILON and label not in self.alphabet:
            raise ValueError(f"Transition label is not in the alphabet: {label}")
        return frozenset(self.transitions[state].get(label, set()))

    def iterEdges(self) -> Iterator[tuple[State, TransitionLabel, State]]:
        for source, outgoing_transitions in enumerate(self.transitions):
            for label, destinations in outgoing_transitions.items():
                for destination in destinations:
                    yield source, label, destination

    def isDeterministic(self) -> bool:
        for outgoing_transitions in self.transitions:
            if outgoing_transitions.get(EPSILON):
                return False
            if any(len(destinations) > 1 for destinations in outgoing_transitions.values()):
                return False
        return True


class NFABuilder:
    def __init__(self, alphabet: Iterable[Symbol]):
        self.alphabet = frozenset(alphabet)
        assert EPSILON not in self.alphabet
        self.transitions: list[dict[TransitionLabel, set[State]]] = []

    def newState(self) -> State:
        state = len(self.transitions)
        self.transitions.append({})
        return state

    def addTransition(
        self,
        source: State,
        label: TransitionLabel,
        destination: State,
    ) -> None:
        assert 0 <= source < len(self.transitions)
        assert 0 <= destination < len(self.transitions)

        if label is not EPSILON and label not in self.alphabet:
            raise ValueError(f"Transition label is not in the alphabet: {label}")

        destinations = self.transitions[source].setdefault(label, set())
        destinations.add(destination)

    def build(
        self,
        start_state: State,
        accepting_states: Iterable[State],
    ) -> NFA:
        transitions = [
            {
                label: set(destinations)
                for label, destinations in outgoing_transitions.items()
            }
            for outgoing_transitions in self.transitions
        ]
        return NFA(
            alphabet=self.alphabet,
            transitions=transitions,
            start_state=start_state,
            accepting_states=frozenset(accepting_states),
        )
