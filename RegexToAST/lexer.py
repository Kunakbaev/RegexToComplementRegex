from dataclasses import dataclass
from enum import Enum, auto


class TokenKind(Enum):
    SYMBOL      = auto()
    EPSILON     = auto()
    EMPTY_SET   = auto()
    LEFT_PAREN  = auto()
    RIGHT_PAREN = auto()
    ALTERNATION = auto()
    KLEENE_STAR = auto()
    ONE_OR_MORE = auto()
    END         = auto()


@dataclass(frozen=True, slots=True)
class Token:
    kind: TokenKind
    text: str
    position: int


# =======================================


def tokenize(text: str) -> list[Token]:
    tokens = [
        getTokenBySymb(c, i)
        for i, c in enumerate(text)
        if not c.isspace()
    ]
    tokens.append(Token(TokenKind.END, '', len(text)))
    return tokens


def getTokenBySymb(c: str, i: int) -> Token:
    if c == '(':
        return Token(TokenKind.LEFT_PAREN, '(', i)
    elif c == ')':
        return Token(TokenKind.RIGHT_PAREN, ')', i)
    elif c == '|':
        return Token(TokenKind.ALTERNATION, '|', i)
    elif c == '*':
        return Token(TokenKind.KLEENE_STAR, '*', i)
    elif c == '+':
        return Token(TokenKind.ONE_OR_MORE, '+', i)
    elif c == '1':
        return Token(TokenKind.EPSILON, '1', i)
    elif c == '0':
        return Token(TokenKind.EMPTY_SET, '0', i)
    elif isSmallLatin(c):
        return Token(TokenKind.SYMBOL, c, i)
    else:
        raise ValueError(f'Invalid character: \'{c}\' at position {i}')


def isSmallLatin(c: str) -> bool:
    return 'a' <= c <= 'z'
