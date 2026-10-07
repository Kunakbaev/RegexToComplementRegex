from collections import deque

from ..dfa import DFA
from ..finite_automaton import State


StatePartition = frozenset[State]


def get_reachable_states(dfa: DFA) -> frozenset[State]:
    reachable_states = {dfa.start_state}
    states_to_visit = deque((dfa.start_state,))

    while states_to_visit:
        state = states_to_visit.popleft()

        for symbol in sorted(dfa.alphabet):
            destination = dfa.getDestination(state, symbol)
            if destination not in reachable_states:
                reachable_states.add(destination)
                states_to_visit.append(destination)

    return frozenset(reachable_states)


def refine_partitions(
    dfa: DFA,
    partitions: list[StatePartition],
) -> list[StatePartition]:
    symbols = tuple(sorted(dfa.alphabet))

    while True:
        partition_by_state = {
            state: partition_index
            for partition_index, partition in enumerate(partitions)
            for state in partition
        }
        refined_partitions: list[StatePartition] = []

        for partition in partitions:
            states_by_signature: dict[tuple[int, ...], set[State]] = {}

            for state in sorted(partition):
                signature = tuple(
                    partition_by_state[dfa.getDestination(state, symbol)]
                    for symbol in symbols
                )
                states_by_signature.setdefault(signature, set()).add(state)

            refined_partitions.extend(
                frozenset(states)
                for states in states_by_signature.values()
            )

        if refined_partitions == partitions:
            return partitions

        partitions = refined_partitions


def minimize_dfa(dfa: DFA) -> DFA:
    reachable_states = get_reachable_states(dfa)
    accepting_states = reachable_states & dfa.accepting_states
    non_accepting_states = reachable_states - accepting_states
    partitions = [
        partition
        for partition in (
            frozenset(non_accepting_states),
            frozenset(accepting_states),
        )
        if partition
    ]
    partitions = refine_partitions(dfa, partitions)

    partition_by_state = {
        state: partition
        for partition in partitions
        for state in partition
    }
    start_partition = partition_by_state[dfa.start_state]
    partition_to_state = {start_partition: 0}
    partitions_to_visit = deque((start_partition,))
    transitions: list[dict[str, State]] = [{}]
    minimized_accepting_states: set[State] = set()

    while partitions_to_visit:
        source_partition = partitions_to_visit.popleft()
        source = partition_to_state[source_partition]
        representative = min(source_partition)

        if source_partition & dfa.accepting_states:
            minimized_accepting_states.add(source)

        for symbol in sorted(dfa.alphabet):
            original_destination = dfa.getDestination(representative, symbol)
            destination_partition = partition_by_state[original_destination]

            if destination_partition not in partition_to_state:
                destination = len(transitions)
                partition_to_state[destination_partition] = destination
                transitions.append({})
                partitions_to_visit.append(destination_partition)

            transitions[source][symbol] = partition_to_state[destination_partition]

    return DFA(
        alphabet=dfa.alphabet,
        transitions=transitions,
        start_state=0,
        accepting_states=frozenset(minimized_accepting_states),
    )
