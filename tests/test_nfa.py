import unittest

from Automata import EPSILON, NFA


class NFATest(unittest.TestCase):
    def testExposesStatesAndTransitions(self):
        nfa = NFA(
            alphabet=frozenset(("a", "b")),
            transitions=[
                {"a": {1}, EPSILON: {2}},
                {"b": {1, 2}},
                {},
            ],
            start_state=0,
            accepting_states=frozenset((2,)),
        )

        self.assertEqual(nfa.numStates, 3)
        self.assertEqual(nfa.states, range(3))
        self.assertEqual(nfa.numTransitions, 4)
        self.assertFalse(nfa.isAccepting(0))
        self.assertTrue(nfa.isAccepting(2))
        self.assertEqual(nfa.getDestinations(0, "a"), frozenset((1,)))
        self.assertEqual(nfa.getDestinations(0, "b"), frozenset())
        self.assertEqual(nfa.getDestinations(0, EPSILON), frozenset((2,)))
        self.assertEqual(
            set(nfa.iterEdges()),
            {
                (0, "a", 1),
                (0, EPSILON, 2),
                (1, "b", 1),
                (1, "b", 2),
            },
        )

    def testDetectsDeterminism(self):
        deterministic_nfa = NFA(
            alphabet=frozenset(("a",)),
            transitions=[
                {"a": {1}},
                {},
            ],
            start_state=0,
            accepting_states=frozenset((1,)),
        )
        epsilon_nfa = NFA(
            alphabet=frozenset(("a",)),
            transitions=[
                {EPSILON: {1}},
                {},
            ],
            start_state=0,
            accepting_states=frozenset((1,)),
        )
        branching_nfa = NFA(
            alphabet=frozenset(("a",)),
            transitions=[
                {"a": {1, 2}},
                {},
                {},
            ],
            start_state=0,
            accepting_states=frozenset((2,)),
        )

        self.assertTrue(deterministic_nfa.isDeterministic())
        self.assertFalse(epsilon_nfa.isDeterministic())
        self.assertFalse(branching_nfa.isDeterministic())


if __name__ == "__main__":
    unittest.main()
