from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


class Regex(ABC):
    __slots__ = ()

    @property
    @abstractmethod
    def children(self) -> tuple[Regex, ...]:
        raise NotImplementedError

    @property
    def kind(self) -> str:
        return type(self).__name__

    @property
    def label(self) -> str:
        return self.kind


class _Leaf(Regex):
    __slots__ = ()

    @property
    def children(self) -> tuple[Regex, ...]:
        return ()


@dataclass(frozen=True, slots=True)
class Symbol(_Leaf):
    value: str

    def __post_init__(self) -> None:
        if len(self.value) != 1:
            raise ValueError("A symbol must contain exactly one character")

    @property
    def label(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class Epsilon(_Leaf):
    @property
    def label(self) -> str:
        return "ε"


@dataclass(frozen=True, slots=True)
class EmptySet(_Leaf):
    @property
    def label(self) -> str:
        return "∅"


@dataclass(frozen=True, slots=True)
class _Unary(Regex):
    operand: Regex

    @property
    def children(self) -> tuple[Regex, ...]:
        return (self.operand,)


@dataclass(frozen=True, slots=True)
class Star(_Unary):
    @property
    def label(self) -> str:
        return "*"


@dataclass(frozen=True, slots=True)
class OneOrMore(_Unary):
    @property
    def label(self) -> str:
        return "+"


@dataclass(frozen=True, slots=True)
class _Nary(Regex):
    operands: tuple[Regex, ...]

    def __post_init__(self) -> None:
        if len(self.operands) < 2:
            raise ValueError(f"{self.kind} requires at least two operands")

    @property
    def children(self) -> tuple[Regex, ...]:
        return self.operands


@dataclass(frozen=True, slots=True)
class Concat(_Nary):
    pass


@dataclass(frozen=True, slots=True)
class Alt(_Nary):
    @property
    def label(self) -> str:
        return "|"
