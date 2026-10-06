import unittest

from Automata import NFA, nfa_to_dfa


class SubsetConstructionTest(unittest.TestCase):
    def testBuildsCompleteDFA(self):
        nfa = NFA(
            alphabet=frozenset(("a", "b")),
            transitions=[
                {"a": {0, 1}},
                {},
            ],
            start_state=0,
            accepting_states=frozenset((1,)),
        )

        dfa = nfa_to_dfa(nfa)

        self.assertEqual(dfa.numStates, 3)
        self.assertEqual(dfa.start_state, 0)
        self.assertEqual(dfa.accepting_states, frozenset((1,)))
        self.assertEqual(
            set(dfa.iterEdges()),
            {
                (0, "a", 1),
                (0, "b", 2),
                (1, "a", 1),
                (1, "b", 2),
                (2, "a", 2),
                (2, "b", 2),
            },
        )
        self.assertTrue(dfa.isDeterministic())


if __name__ == "__main__":
    unittest.main()
