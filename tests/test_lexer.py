import unittest

from RegexToAST.lexer import Token, TokenKind, tokenize


class TokenizeTest(unittest.TestCase):
    def testTokenizesOperatorsAndParentheses(self):
        self.assertEqual(
            tokenize("(a|b)+"),
            [
                Token(TokenKind.LEFT_PAREN, "(", 0),
                Token(TokenKind.SYMBOL, "a", 1),
                Token(TokenKind.ALTERNATION, "|", 2),
                Token(TokenKind.SYMBOL, "b", 3),
                Token(TokenKind.RIGHT_PAREN, ")", 4),
                Token(TokenKind.ONE_OR_MORE, "+", 5),
                Token(TokenKind.END, "", 6),
            ],
        )

    def testTokenizesSpecialLanguagesAndStar(self):
        self.assertEqual(
            tokenize("0|1*"),
            [
                Token(TokenKind.EMPTY_SET, "0", 0),
                Token(TokenKind.ALTERNATION, "|", 1),
                Token(TokenKind.EPSILON, "1", 2),
                Token(TokenKind.KLEENE_STAR, "*", 3),
                Token(TokenKind.END, "", 4),
            ],
        )

    def testIgnoresWhitespaceAndPreservesPositions(self):
        self.assertEqual(
            tokenize("a | b"),
            [
                Token(TokenKind.SYMBOL, "a", 0),
                Token(TokenKind.ALTERNATION, "|", 2),
                Token(TokenKind.SYMBOL, "b", 4),
                Token(TokenKind.END, "", 5),
            ],
        )


if __name__ == "__main__":
    unittest.main()
