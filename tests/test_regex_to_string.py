import unittest

from RegexToAST.parser import RegexParser
from RegexToAST.regex_ast import Alt, Concat, EmptySet, Epsilon, OneOrMore, Star, Symbol
from RegexToAST.regex_to_string import regex_to_string


class RegexToStringTest(unittest.TestCase):
    def testSerializesLeafNodes(self):
        self.assertEqual(regex_to_string(Symbol("a")), "a")
        self.assertEqual(regex_to_string(Epsilon()), "1")
        self.assertEqual(regex_to_string(EmptySet()), "0")

    def testAddsOnlyRequiredPrecedenceParentheses(self):
        root = Alt((
            Concat((
                Symbol("a"),
                Star(Alt((Symbol("b"), Symbol("c")))),
            )),
            OneOrMore(Symbol("d")),
        ))

        self.assertEqual(regex_to_string(root), "a(b|c)*|d+")

    def testParenthesizesNestedRepeatOperators(self):
        self.assertEqual(
            regex_to_string(Star(OneOrMore(Symbol("a")))),
            "(a+)*",
        )

    def testSerializedRegexCanBeParsedBack(self):
        root = Alt((
            Concat((Symbol("a"), Star(Symbol("b")))),
            OneOrMore(Symbol("c")),
        ))

        self.assertEqual(RegexParser(regex_to_string(root)).parse(), root)


if __name__ == "__main__":
    unittest.main()
