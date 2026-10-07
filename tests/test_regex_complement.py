import unittest
from itertools import product
from unittest.mock import patch

from Automata import nfa_to_dfa, regex_to_nfa, remove_epsilon_transitions
from RegexToAST.parser import RegexParser
from regex_complement import regex_to_complement_regex


class RegexComplementTest(unittest.TestCase):
    def testComplementsExampleLanguage(self):
        alphabet = frozenset(("a", "b"))
        original_regex = "(ab)*b+a(1|b(a|b))"
        complement_regex = regex_to_complement_regex(original_regex, alphabet)
        original_dfa = self.buildDFA(original_regex, alphabet)
        complement_dfa = self.buildDFA(complement_regex, alphabet)

        for word_length in range(6):
            for symbols in product(sorted(alphabet), repeat=word_length):
                word = "".join(symbols)
                with self.subTest(word=word):
                    self.assertNotEqual(
                        self.accepts(original_dfa, word),
                        self.accepts(complement_dfa, word),
                    )

    def testComplementsUniversalAndEmptyLanguages(self):
        alphabet = frozenset(("a", "b"))

        self.assertEqual(
            regex_to_complement_regex("(a|b)*", alphabet),
            "0",
        )
        self.assertEqual(
            regex_to_complement_regex("0", alphabet),
            "(a|b)*",
        )

    @patch("regex_complement.render_gnfa")
    @patch("regex_complement.render_automaton")
    @patch("regex_complement.render_regex_AST")
    def testGeneratesImagesOnlyWhenEnabled(
        self,
        render_ast,
        render_automaton,
        render_gnfa,
    ):
        alphabet = frozenset(("a",))

        regex_to_complement_regex("a", alphabet, generate_images=False)
        render_ast.assert_not_called()
        render_automaton.assert_not_called()
        render_gnfa.assert_not_called()

        regex_to_complement_regex("a", alphabet, generate_images=True)
        render_ast.assert_called_once()
        self.assertEqual(render_automaton.call_count, 5)
        self.assertGreater(render_gnfa.call_count, 0)

    @staticmethod
    def buildDFA(regex, alphabet):
        root = RegexParser(regex).parse()
        nfa = regex_to_nfa(root, alphabet)
        return nfa_to_dfa(remove_epsilon_transitions(nfa))

    @staticmethod
    def accepts(dfa, word):
        state = dfa.start_state
        for symbol in word:
            state = dfa.getDestination(state, symbol)
        return dfa.isAccepting(state)


if __name__ == "__main__":
    unittest.main()
