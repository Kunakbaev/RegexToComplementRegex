import unittest

from Automata import DFA


class DFATest(unittest.TestCase):
    def testExposesDeterministicTransitions(self):
        dfa = DFA(
            alphabet=frozenset(("a", "b")),
            transitions=[
                {"a": 1, "b": 0},
                {"a": 1, "b": 0},
            ],
            start_state=0,
            accepting_states=frozenset((1,)),
        )

        self.assertEqual(dfa.numStates, 2)
        self.assertEqual(dfa.numTransitions, 4)
        self.assertEqual(dfa.getDestination(0, "a"), 1)
        self.assertEqual(dfa.getDestinations(0, "a"), frozenset((1,)))
        self.assertEqual(
            set(dfa.iterEdges()),
            {
                (0, "a", 1),
                (0, "b", 0),
                (1, "a", 1),
                (1, "b", 0),
            },
        )
        self.assertTrue(dfa.isDeterministic())


if __name__ == "__main__":
    unittest.main()
