from .lexer import Token, TokenKind, tokenize
from .regex_ast import Alt, Symbol, Epsilon, EmptySet, Star, OneOrMore, Concat, Regex


ATOM_START_KINDS = {
    TokenKind.SYMBOL,
    TokenKind.EPSILON,
    TokenKind.EMPTY_SET,
    TokenKind.LEFT_PAREN,
}


class RegexParser:
    def __init__(self, regex: str):
        self.tokens = tokenize(regex)
        self.position = 0

    def parse(self) -> Regex:
        root = self.parseAlternationRule()
        self.consumeToken(TokenKind.END)
        return root

    def parseAlternationRule(self) -> Regex:
        children = [self.parseConcatRule()]

        while self.tryConsumeToken(TokenKind.ALTERNATION):
            children.append(self.parseConcatRule())

        if len(children) == 1:
            return children[0]
        return Alt(tuple(children))

    def parseConcatRule(self) -> Regex:
        children = []

        while self.currentToken().kind in ATOM_START_KINDS:
            children.append(self.parseRepeatRule())

        if len(children) == 0:
            token = self.currentToken()
            raise ValueError(f'Expected an atom at position {token.position}')
        if len(children) == 1:
            return children[0]
        return Concat(tuple(children))

    def parseRepeatRule(self) -> Regex:
        atom = self.parseAtomRule()

        if self.tryConsumeToken(TokenKind.KLEENE_STAR):
            return Star(atom)
        if self.tryConsumeToken(TokenKind.ONE_OR_MORE):
            return OneOrMore(atom)
        return atom

    def parseAtomRule(self) -> Regex:
        token = self.currentToken()

        if token.kind == TokenKind.SYMBOL:
            self.advanceToken()
            return Symbol(token.text)
        if token.kind == TokenKind.EPSILON:
            self.advanceToken()
            return Epsilon()
        if token.kind == TokenKind.EMPTY_SET:
            self.advanceToken()
            return EmptySet()
        if token.kind == TokenKind.LEFT_PAREN:
            self.advanceToken()
            node = self.parseAlternationRule()
            self.consumeToken(TokenKind.RIGHT_PAREN)
            return node

        raise ValueError(f'Expected an atom at position {token.position}')

    def currentToken(self) -> Token:
        return self.tokens[self.position]

    # no checks at all, get current, move to the nxt one
    def advanceToken(self) -> Token:
        token = self.currentToken()
        self.position += 1
        return token

    # useful when we are lenient about no match (as in parse repeat rule)
    def tryConsumeToken(self, expected_kind: TokenKind) -> bool:
        if self.currentToken().kind != expected_kind:
            return False
        self.advanceToken()
        return True

    # most strict, ensures that consumed token is exactly as we expect it to be
    def consumeToken(self, expected_kind: TokenKind) -> Token:
        token = self.currentToken()
        if not self.tryConsumeToken(expected_kind):
            raise ValueError(
                f'Expected {expected_kind.name}, got {token.kind.name} '
                f'at position {token.position}'
            )
        return token
