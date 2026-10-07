import unittest

from Automata import DFA, minimize_dfa


class DFAMinimizationTest(unittest.TestCase):
    def testMergesEquivalentStatesAndRemovesUnreachableStates(self):
        dfa = DFA(
            alphabet=frozenset(("a", "b")),
            transitions=[
                {"a": 1, "b": 2},
                {"a": 1, "b": 3},
                {"a": 1, "b": 3},
                {"a": 3, "b": 3},
                {"a": 3, "b": 4},
            ],
            start_state=0,
            accepting_states=frozenset((1, 2, 4)),
        )

        result = minimize_dfa(dfa)

        self.assertEqual(result.numStates, 3)
        self.assertEqual(result.start_state, 0)
        self.assertEqual(result.accepting_states, frozenset((1,)))
        self.assertEqual(
            set(result.iterEdges()),
            {
                (0, "a", 1),
                (0, "b", 1),
                (1, "a", 1),
                (1, "b", 2),
                (2, "a", 2),
                (2, "b", 2),
            },
        )

    def testKeepsDistinguishableStates(self):
        dfa = DFA(
            alphabet=frozenset(("a", "b")),
            transitions=[
                {"a": 1, "b": 0},
                {"a": 0, "b": 1},
            ],
            start_state=0,
            accepting_states=frozenset((1,)),
        )

        result = minimize_dfa(dfa)

        self.assertEqual(result.numStates, 2)
        self.assertEqual(result.accepting_states, frozenset((1,)))
        self.assertEqual(set(result.iterEdges()), set(dfa.iterEdges()))


if __name__ == "__main__":
    unittest.main()
