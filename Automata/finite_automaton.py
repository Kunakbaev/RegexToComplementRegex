from abc import ABC, abstractmethod
from collections.abc import Hashable, Iterator
from dataclasses import dataclass
from typing import Generic, TypeVar


State = int
Symbol = str

TransitionLabelType = TypeVar("TransitionLabelType", bound=Hashable)
TransitionValueType = TypeVar("TransitionValueType")


@dataclass
class FiniteAutomaton(ABC, Generic[TransitionLabelType, TransitionValueType]):
    alphabet: frozenset[Symbol]
    transitions: list[dict[TransitionLabelType, TransitionValueType]]
    start_state: State
    accepting_states: frozenset[State]

    def __post_init__(self) -> None:
        self.alphabet = frozenset(self.alphabet)
        self.accepting_states = frozenset(self.accepting_states)

        if self.numStates == 0:
            raise ValueError("A finite automaton must contain at least one state")
        if any(not isinstance(symbol, Symbol) or len(symbol) != 1 for symbol in self.alphabet):
            raise ValueError("Alphabet symbols must be one-character strings")

        self.validateState(self.start_state)
        for state in self.accepting_states:
            self.validateState(state)

    @property
    def numStates(self) -> int:
        return len(self.transitions)

    @property
    def states(self) -> range:
        return range(self.numStates)

    @property
    def numTransitions(self) -> int:
        return sum(1 for _ in self.iterEdges())

    def isAccepting(self, state: State) -> bool:
        self.validateState(state)
        return state in self.accepting_states

    def validateState(self, state: State) -> None:
        if not 0 <= state < self.numStates:
            raise ValueError(f"Invalid state: {state}")

    @abstractmethod
    def getDestinations(
        self,
        state: State,
        label: TransitionLabelType,
    ) -> frozenset[State]:
        raise NotImplementedError

    @abstractmethod
    def iterEdges(self) -> Iterator[tuple[State, TransitionLabelType, State]]:
        raise NotImplementedError
