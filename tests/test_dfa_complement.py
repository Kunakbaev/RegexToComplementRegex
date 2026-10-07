import unittest

from Automata import DFA, complement_dfa


class DFAComplementTest(unittest.TestCase):
    def testFlipsAcceptingStates(self):
        dfa = DFA(
            alphabet=frozenset(("a",)),
            transitions=[
                {"a": 1},
                {"a": 1},
            ],
            start_state=0,
            accepting_states=frozenset((1,)),
        )

        result = complement_dfa(dfa)

        self.assertEqual(result.transitions, dfa.transitions)
        self.assertEqual(result.start_state, dfa.start_state)
        self.assertEqual(result.accepting_states, frozenset((0,)))


if __name__ == "__main__":
    unittest.main()
