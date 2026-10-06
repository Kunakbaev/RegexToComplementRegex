import unittest

from Automata import EPSILON, NFA, regex_to_nfa
from RegexToAST.regex_ast import Alt, Concat, EmptySet, Epsilon, OneOrMore, Star, Symbol


ALPHABET = frozenset(("a", "b"))


def epsilonClosure(nfa: NFA, states: set[int]) -> set[int]:
    closure = set(states)
    states_to_visit = list(states)

    while states_to_visit:
        state = states_to_visit.pop()
        for destination in nfa.getDestinations(state, EPSILON):
            if destination not in closure:
                closure.add(destination)
                states_to_visit.append(destination)

    return closure


def accepts(nfa: NFA, word: str) -> bool:
    current_states = epsilonClosure(nfa, {nfa.start_state})

    for symbol in word:
        next_states = set()
        for state in current_states:
            next_states.update(nfa.getDestinations(state, symbol))
        current_states = epsilonClosure(nfa, next_states)

    return bool(current_states & nfa.accepting_states)


class ThompsonBuilderTest(unittest.TestCase):
    def testBuildsLeafFragments(self):
        symbol_nfa = regex_to_nfa(Symbol("a"), ALPHABET)
        epsilon_nfa = regex_to_nfa(Epsilon(), ALPHABET)
        empty_set_nfa = regex_to_nfa(EmptySet(), ALPHABET)

        self.assertEqual(symbol_nfa.numStates, 2)
        self.assertEqual(set(symbol_nfa.iterEdges()), {(0, "a", 1)})
        self.assertTrue(accepts(symbol_nfa, "a"))
        self.assertFalse(accepts(symbol_nfa, ""))

        self.assertEqual(epsilon_nfa.numStates, 2)
        self.assertEqual(set(epsilon_nfa.iterEdges()), {(0, EPSILON, 1)})
        self.assertTrue(accepts(epsilon_nfa, ""))
        self.assertFalse(accepts(epsilon_nfa, "a"))

        self.assertEqual(empty_set_nfa.numStates, 2)
        self.assertEqual(empty_set_nfa.numTransitions, 0)
        self.assertFalse(accepts(empty_set_nfa, ""))
        self.assertFalse(accepts(empty_set_nfa, "a"))

    def testBuildsConcat(self):
        nfa = regex_to_nfa(
            Concat((Symbol("a"), Symbol("b"))),
            ALPHABET,
        )

        self.assertEqual(nfa.numStates, 4)
        self.assertEqual(nfa.numTransitions, 3)
        self.assertTrue(accepts(nfa, "ab"))
        self.assertFalse(accepts(nfa, ""))
        self.assertFalse(accepts(nfa, "a"))
        self.assertFalse(accepts(nfa, "b"))

    def testBuildsAlternation(self):
        nfa = regex_to_nfa(
            Alt((Symbol("a"), Symbol("b"))),
            ALPHABET,
        )

        self.assertEqual(nfa.numStates, 6)
        self.assertEqual(nfa.numTransitions, 6)
        self.assertTrue(accepts(nfa, "a"))
        self.assertTrue(accepts(nfa, "b"))
        self.assertFalse(accepts(nfa, ""))
        self.assertFalse(accepts(nfa, "ab"))

    def testDistinguishesStarAndOneOrMore(self):
        star_nfa = regex_to_nfa(Star(Symbol("a")), ALPHABET)
        one_or_more_nfa = regex_to_nfa(OneOrMore(Symbol("a")), ALPHABET)
        star_end_state = next(iter(star_nfa.accepting_states))
        one_or_more_end_state = next(iter(one_or_more_nfa.accepting_states))

        self.assertIn(
            star_end_state,
            star_nfa.getDestinations(star_nfa.start_state, EPSILON),
        )
        self.assertNotIn(
            one_or_more_end_state,
            one_or_more_nfa.getDestinations(one_or_more_nfa.start_state, EPSILON),
        )
        self.assertTrue(accepts(star_nfa, ""))
        self.assertTrue(accepts(star_nfa, "a"))
        self.assertTrue(accepts(star_nfa, "aaa"))
        self.assertFalse(accepts(star_nfa, "b"))
        self.assertFalse(accepts(one_or_more_nfa, ""))
        self.assertTrue(accepts(one_or_more_nfa, "a"))
        self.assertTrue(accepts(one_or_more_nfa, "aaa"))
        self.assertFalse(accepts(one_or_more_nfa, "b"))

    def testBuildsNestedAst(self):
        root = Concat((
            Star(Symbol("a")),
            Alt((Epsilon(), Symbol("b"))),
        ))
        nfa = regex_to_nfa(root, ALPHABET)

        for accepted_word in ("", "a", "aa", "b", "ab", "aab"):
            with self.subTest(word=accepted_word):
                self.assertTrue(accepts(nfa, accepted_word))

        for rejected_word in ("ba", "bb", "aba"):
            with self.subTest(word=rejected_word):
                self.assertFalse(accepts(nfa, rejected_word))


if __name__ == "__main__":
    unittest.main()
