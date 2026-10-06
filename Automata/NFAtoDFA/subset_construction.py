from collections import deque

from ..dfa import DFA
from ..finite_automaton import State
from ..nfa import EPSILON, NFA


StateSubset = frozenset[State]


def nfa_to_dfa(nfa: NFA) -> DFA:
    if any(label is EPSILON for _, label, _ in nfa.iterEdges()):
        raise ValueError("Subset construction requires an epsilon-free NFA")

    start_subset: StateSubset = frozenset((nfa.start_state,))
    subset_to_state = {start_subset: 0}
    subsets_to_visit = deque((start_subset,))
    transitions: list[dict[str, State]] = [{}]
    accepting_states: set[State] = set()

    while subsets_to_visit:
        source_subset = subsets_to_visit.popleft()
        source = subset_to_state[source_subset]

        if source_subset & nfa.accepting_states:
            accepting_states.add(source)

        for symbol in sorted(nfa.alphabet):
            destination_subset = frozenset(
                destination
                for nfa_state in source_subset
                for destination in nfa.getDestinations(nfa_state, symbol)
            )

            if destination_subset not in subset_to_state:
                destination = len(transitions)
                subset_to_state[destination_subset] = destination
                transitions.append({})
                subsets_to_visit.append(destination_subset)

            transitions[source][symbol] = subset_to_state[destination_subset]

    return DFA(
        alphabet=nfa.alphabet,
        transitions=transitions,
        start_state=0,
        accepting_states=frozenset(accepting_states),
    )
