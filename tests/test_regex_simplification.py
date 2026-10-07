import unittest

from RegexToAST.regex_ast import Alt, Concat, EmptySet, Epsilon, OneOrMore, Star, Symbol
from RegexToAST.regex_simplification import simplify_regex


class RegexSimplificationTest(unittest.TestCase):
    def testSimplifiesExistingNestedAst(self):
        root = Concat((
            Epsilon(),
            Alt((
                EmptySet(),
                Symbol("a"),
                Alt((Symbol("a"), EmptySet())),
            )),
            Concat((Symbol("b"), Epsilon())),
        ))

        self.assertEqual(
            simplify_regex(root),
            Concat((Symbol("a"), Symbol("b"))),
        )

    def testSimplifiesUnaryOperators(self):
        self.assertEqual(simplify_regex(Star(EmptySet())), Epsilon())
        self.assertEqual(
            simplify_regex(Star(Star(Symbol("a")))),
            Star(Symbol("a")),
        )
        self.assertEqual(simplify_regex(OneOrMore(EmptySet())), EmptySet())
        self.assertEqual(
            simplify_regex(OneOrMore(Star(Symbol("a")))),
            Star(Symbol("a")),
        )

    def testIsIdempotent(self):
        root = Alt((
            EmptySet(),
            Concat((Epsilon(), Symbol("a"))),
            Symbol("a"),
        ))

        simplified = simplify_regex(root)

        self.assertEqual(simplified, Symbol("a"))
        self.assertEqual(simplify_regex(simplified), simplified)


if __name__ == "__main__":
    unittest.main()
