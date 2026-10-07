import unittest

from Automata import GNFA, gnfa_to_dot
from RegexToAST.regex_ast import Alt, Epsilon, Symbol


class GNFAToDotTest(unittest.TestCase):
    def testBuildsDotGraphWithRegexLabels(self):
        gnfa = GNFA(
            states={0, 1, 2},
            transitions={
                0: {1: Alt((Symbol("a"), Symbol("b")))},
                1: {2: Epsilon()},
                2: {},
            },
            start_state=0,
            accepting_state=2,
        )

        source = gnfa_to_dot(gnfa).source

        self.assertIn("label=S", source)
        self.assertIn("label=F", source)
        self.assertIn('label="a|b"', source)
        self.assertIn("label=1", source)
        self.assertIn("shape=doublecircle", source)


if __name__ == "__main__":
    unittest.main()
