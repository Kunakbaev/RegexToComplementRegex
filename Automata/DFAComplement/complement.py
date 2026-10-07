from ..dfa import DFA


def complement_dfa(dfa: DFA) -> DFA:
    return DFA(
        alphabet=dfa.alphabet,
        transitions=[
            dict(outgoing_transitions)
            for outgoing_transitions in dfa.transitions
        ],
        start_state=dfa.start_state,
        accepting_states=frozenset(dfa.states) - dfa.accepting_states,
    )
