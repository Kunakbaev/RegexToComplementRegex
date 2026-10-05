import unittest

from RegexToAST.parser import RegexParser
from RegexToAST.regex_ast import Alt, Concat, EmptySet, Epsilon, OneOrMore, Star, Symbol


class RegexParserTest(unittest.TestCase):
    def testParsesLeafNodes(self):
        self.assertEqual(RegexParser("a").parse(), Symbol("a"))
        self.assertEqual(RegexParser("1").parse(), Epsilon())
        self.assertEqual(RegexParser("0").parse(), EmptySet())

    def testParsesConcatAndStar(self):
        root = RegexParser("ab*").parse()

        self.assertEqual(
            root.children,
            (
                Symbol("a"),
                Star(Symbol("b")),
            ),
        )

    def testParsesAlternationAndOneOrMore(self):
        root = RegexParser("(a|b)+").parse()

        self.assertEqual(
            root,
            OneOrMore(
                Alt((Symbol("a"), Symbol("b"))),
            ),
        )

    def testParsesFullExample(self):
        root = RegexParser("(ab)* b+ a(1|b(a|b))").parse()

        self.assertEqual(
            root,
            Concat((
                Star(Concat((Symbol("a"), Symbol("b")))),
                OneOrMore(Symbol("b")),
                Symbol("a"),
                Alt((
                    Epsilon(),
                    Concat((
                        Symbol("b"),
                        Alt((Symbol("a"), Symbol("b"))),
                    )),
                )),
            )),
        )


if __name__ == "__main__":
    unittest.main()
