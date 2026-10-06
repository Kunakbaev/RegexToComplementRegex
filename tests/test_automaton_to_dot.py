import unittest

from Automata import EPSILON, NFA, automaton_to_dot


class AutomatonToDotTest(unittest.TestCase):
    def testBuildsDotGraphForNFA(self):
        nfa = NFA(
            alphabet=frozenset(("a", "b")),
            transitions=[
                {"a": {1}, "b": {1}, EPSILON: {2}},
                {},
                {},
            ],
            start_state=0,
            accepting_states=frozenset((2,)),
        )

        source = automaton_to_dot(nfa).source

        self.assertIn("rankdir=LR", source)
        self.assertIn("state_0", source)
        self.assertIn("state_1", source)
        self.assertIn("state_2", source)
        self.assertIn("shape=doublecircle", source)
        self.assertIn("start_pointer -> state_0", source)
        self.assertIn('label="a, b"', source)
        self.assertIn('label="ε"', source)


if __name__ == "__main__":
    unittest.main()
