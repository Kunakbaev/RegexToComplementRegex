from collections import deque
from collections.abc import Iterable

from ..finite_automaton import State
from ..nfa import EPSILON, NFA


def epsilon_closure(nfa: NFA, states: Iterable[State]) -> frozenset[State]:
    closure = set(states)
    states_to_visit = list(closure)

    while states_to_visit:
        state = states_to_visit.pop()

        for destination in nfa.getDestinations(state, EPSILON):
            if destination not in closure:
                closure.add(destination)
                states_to_visit.append(destination)

    return frozenset(closure)


def remove_epsilon_transitions(nfa: NFA) -> NFA:
    original_to_new_state = {nfa.start_state: 0}
    states_to_visit = deque((nfa.start_state,))
    transitions: list[dict[str, set[State]]] = [{}]
    accepting_states: set[State] = set()

    while states_to_visit:
        original_source = states_to_visit.popleft()
        new_source = original_to_new_state[original_source]
        closure = epsilon_closure(nfa, (original_source,))

        if closure & nfa.accepting_states:
            accepting_states.add(new_source)

        for symbol in sorted(nfa.alphabet):
            original_destinations: set[State] = set()

            for closure_state in closure:
                original_destinations.update(
                    nfa.getDestinations(closure_state, symbol)
                )

            if not original_destinations:
                continue

            new_destinations: set[State] = set()
            for original_destination in sorted(original_destinations):
                if original_destination not in original_to_new_state:
                    new_state = len(transitions)
                    original_to_new_state[original_destination] = new_state
                    transitions.append({})
                    states_to_visit.append(original_destination)

                new_destinations.add(
                    original_to_new_state[original_destination]
                )

            transitions[new_source][symbol] = new_destinations

    return NFA(
        alphabet=nfa.alphabet,
        transitions=transitions,
        start_state=0,
        accepting_states=frozenset(accepting_states),
    )
