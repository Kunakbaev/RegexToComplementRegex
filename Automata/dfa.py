from collections.abc import Iterator
from dataclasses import dataclass

from .finite_automaton import FiniteAutomaton, State, Symbol


@dataclass
class DFA(FiniteAutomaton[Symbol, State]):
    def __post_init__(self) -> None:
        super().__post_init__()

        for state, outgoing_transitions in enumerate(self.transitions):
            transition_symbols = frozenset(outgoing_transitions)

            if transition_symbols != self.alphabet:
                raise ValueError(
                    f"DFA state {state} must have exactly one transition "
                    "for every alphabet symbol"
                )

            for destination in outgoing_transitions.values():
                self.validateState(destination)

    def getDestination(self, state: State, symbol: Symbol) -> State:
        self.validateState(state)
        if symbol not in self.alphabet:
            raise ValueError(f"Transition symbol is not in the alphabet: {symbol}")
        return self.transitions[state][symbol]

    def getDestinations(self, state: State, label: Symbol) -> frozenset[State]:
        return frozenset((self.getDestination(state, label),))

    def iterEdges(self) -> Iterator[tuple[State, Symbol, State]]:
        for source, outgoing_transitions in enumerate(self.transitions):
            for symbol, destination in outgoing_transitions.items():
                yield source, symbol, destination

    def isDeterministic(self) -> bool:
        return True
