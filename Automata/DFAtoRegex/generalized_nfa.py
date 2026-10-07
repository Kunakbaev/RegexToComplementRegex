from dataclasses import dataclass

from RegexToAST.regex_ast import EmptySet, Epsilon, Regex, Symbol

from ..dfa import DFA
from ..finite_automaton import State
from .regex_operations import make_alt


@dataclass
class GNFA:
    states: set[State]
    transitions: dict[State, dict[State, Regex]]
    start_state: State
    accepting_state: State

    def __post_init__(self) -> None:
        if self.start_state not in self.states:
            raise ValueError("GNFA start state is not contained in its states")
        if self.accepting_state not in self.states:
            raise ValueError("GNFA accepting state is not contained in its states")

        for source, outgoing_transitions in self.transitions.items():
            self.validateState(source)
            for destination in outgoing_transitions:
                self.validateState(destination)

    def validateState(self, state: State) -> None:
        if state not in self.states:
            raise ValueError(f"Invalid GNFA state: {state}")

    def getTransition(self, source: State, destination: State) -> Regex:
        self.validateState(source)
        self.validateState(destination)
        return self.transitions.get(source, {}).get(destination, EmptySet())

    def setTransition(
        self,
        source: State,
        destination: State,
        regex: Regex,
    ) -> None:
        self.validateState(source)
        self.validateState(destination)

        if isinstance(regex, EmptySet):
            self.transitions.setdefault(source, {}).pop(destination, None)
        else:
            self.transitions.setdefault(source, {})[destination] = regex

    def addTransition(
        self,
        source: State,
        destination: State,
        regex: Regex,
    ) -> None:
        self.setTransition(
            source,
            destination,
            make_alt(self.getTransition(source, destination), regex),
        )

    def removeState(self, state: State) -> None:
        self.validateState(state)
        if state in (self.start_state, self.accepting_state):
            raise ValueError("Cannot remove the GNFA start or accepting state")

        self.states.remove(state)
        self.transitions.pop(state, None)
        for outgoing_transitions in self.transitions.values():
            outgoing_transitions.pop(state, None)


def dfa_to_gnfa(dfa: DFA) -> GNFA:
    start_state = dfa.numStates
    accepting_state = dfa.numStates + 1
    states = set(dfa.states) | {start_state, accepting_state}
    gnfa = GNFA(
        states=states,
        transitions={state: {} for state in states},
        start_state=start_state,
        accepting_state=accepting_state,
    )

    gnfa.addTransition(start_state, dfa.start_state, Epsilon())

    for source in dfa.states:
        for symbol in sorted(dfa.alphabet):
            gnfa.addTransition(
                source,
                dfa.getDestination(source, symbol),
                Symbol(symbol),
            )

    for state in sorted(dfa.accepting_states):
        gnfa.addTransition(state, accepting_state, Epsilon())

    return gnfa
