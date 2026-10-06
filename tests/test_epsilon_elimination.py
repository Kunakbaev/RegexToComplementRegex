import unittest

from Automata import EPSILON, NFA, epsilon_closure, remove_epsilon_transitions


class EpsilonEliminationTest(unittest.TestCase):
    def testComputesEpsilonClosureWithCycle(self):
        nfa = NFA(
            alphabet=frozenset(("a",)),
            transitions=[
                {EPSILON: {1}},
                {EPSILON: {0, 2}},
                {},
            ],
            start_state=0,
            accepting_states=frozenset((2,)),
        )

        self.assertEqual(epsilon_closure(nfa, (0,)), frozenset((0, 1, 2)))
        self.assertEqual(epsilon_closure(nfa, (2,)), frozenset((2,)))

    def testRemovesEpsilonTransitionsAndRedundantStates(self):
        nfa = NFA(
            alphabet=frozenset(("a", "b")),
            transitions=[
                {EPSILON: {1, 2}},
                {"a": {3}},
                {"a": {4}},
                {EPSILON: {5}},
                {EPSILON: {5}},
                {},
            ],
            start_state=0,
            accepting_states=frozenset((5,)),
        )

        result = remove_epsilon_transitions(nfa)

        self.assertEqual(result.alphabet, nfa.alphabet)
        self.assertEqual(result.numStates, 3)
        self.assertEqual(result.start_state, 0)
        self.assertEqual(result.accepting_states, frozenset((1, 2)))
        self.assertEqual(
            set(result.iterEdges()),
            {
                (0, "a", 1),
                (0, "a", 2),
            },
        )
        self.assertTrue(
            all(label is not EPSILON for _, label, _ in result.iterEdges())
        )

    def testPropagatesAcceptanceThroughTrailingEpsilonEdges(self):
        nfa = NFA(
            alphabet=frozenset(("a",)),
            transitions=[
                {EPSILON: {1}},
                {},
            ],
            start_state=0,
            accepting_states=frozenset((1,)),
        )

        result = remove_epsilon_transitions(nfa)

        self.assertEqual(result.numStates, 1)
        self.assertEqual(result.accepting_states, frozenset((0,)))
        self.assertEqual(result.numTransitions, 0)


if __name__ == "__main__":
    unittest.main()
