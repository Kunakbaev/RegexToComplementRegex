from RegexToAST.regex_ast import Alt, Concat, Regex, Star
from RegexToAST.regex_simplification import simplify_regex

from ..dfa import DFA
from ..finite_automaton import State
from .generalized_nfa import GNFA, dfa_to_gnfa


def eliminate_state(gnfa: GNFA, state: State) -> None:
    gnfa.validateState(state)
    if state in (gnfa.start_state, gnfa.accepting_state):
        raise ValueError("Cannot eliminate the GNFA start or accepting state")

    remaining_states = sorted(gnfa.states - {state})
    repeated_loop = simplify_regex(Star(gnfa.getTransition(state, state)))

    for source in remaining_states:
        transition_to_state = gnfa.getTransition(source, state)

        for destination in remaining_states:
            transition_from_state = gnfa.getTransition(state, destination)
            transition_through_state = simplify_regex(Concat((
                transition_to_state,
                repeated_loop,
                transition_from_state,
            )))
            gnfa.setTransition(
                source,
                destination,
                simplify_regex(Alt((
                    gnfa.getTransition(source, destination),
                    transition_through_state,
                ))),
            )

    gnfa.removeState(state)


def dfa_to_regex(dfa: DFA) -> Regex:
    gnfa = dfa_to_gnfa(dfa)

    for state in dfa.states:
        eliminate_state(gnfa, state)

    return simplify_regex(
        gnfa.getTransition(gnfa.start_state, gnfa.accepting_state)
    )
