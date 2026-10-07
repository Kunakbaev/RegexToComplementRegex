import unittest

from Automata import DFA, GNFA, dfa_to_gnfa, dfa_to_regex, eliminate_state
from RegexToAST.regex_ast import Alt, Concat, EmptySet, Epsilon, Star, Symbol


class DFAToRegexTest(unittest.TestCase):
    def testEliminatesStateAndUpdatesRegexTransition(self):
        gnfa = GNFA(
            states={0, 1, 2},
            transitions={
                0: {1: Symbol("a"), 2: Symbol("d")},
                1: {1: Symbol("b"), 2: Symbol("c")},
                2: {},
            },
            start_state=0,
            accepting_state=2,
        )

        eliminate_state(gnfa, 1)

        self.assertEqual(gnfa.states, {0, 2})
        self.assertEqual(
            gnfa.getTransition(0, 2),
            Alt((
                Symbol("d"),
                Concat((Symbol("a"), Star(Symbol("b")), Symbol("c"))),
            )),
        )

    def testCreatesGNFAWithSyntheticStartAndAcceptingStates(self):
        dfa = DFA(
            alphabet=frozenset(("a", "b")),
            transitions=[
                {"a": 1, "b": 1},
                {"a": 1, "b": 1},
            ],
            start_state=0,
            accepting_states=frozenset((1,)),
        )

        gnfa = dfa_to_gnfa(dfa)

        self.assertEqual(gnfa.states, {0, 1, 2, 3})
        self.assertEqual(gnfa.start_state, 2)
        self.assertEqual(gnfa.accepting_state, 3)
        self.assertEqual(gnfa.getTransition(2, 0), Epsilon())
        self.assertEqual(
            gnfa.getTransition(0, 1),
            Alt((Symbol("a"), Symbol("b"))),
        )
        self.assertEqual(
            gnfa.getTransition(1, 1),
            Alt((Symbol("a"), Symbol("b"))),
        )
        self.assertEqual(gnfa.getTransition(1, 3), Epsilon())
        self.assertEqual(gnfa.getTransition(0, 3), EmptySet())

    def testBuildsRegexForSingleWordLanguage(self):
        dfa = DFA(
            alphabet=frozenset(("a",)),
            transitions=[
                {"a": 1},
                {"a": 2},
                {"a": 2},
            ],
            start_state=0,
            accepting_states=frozenset((1,)),
        )

        self.assertEqual(dfa_to_regex(dfa), Symbol("a"))

    def testBuildsRegexForAllAndEmptyLanguages(self):
        all_words_dfa = DFA(
            alphabet=frozenset(("a",)),
            transitions=[{"a": 0}],
            start_state=0,
            accepting_states=frozenset((0,)),
        )
        empty_language_dfa = DFA(
            alphabet=frozenset(("a",)),
            transitions=[{"a": 0}],
            start_state=0,
            accepting_states=frozenset(),
        )

        self.assertEqual(dfa_to_regex(all_words_dfa), Star(Symbol("a")))
        self.assertEqual(dfa_to_regex(empty_language_dfa), EmptySet())


if __name__ == "__main__":
    unittest.main()
