from collections.abc import Iterable
from dataclasses import dataclass

from RegexToAST.regex_ast import Alt, Concat, EmptySet, Epsilon, OneOrMore, Regex, Star, Symbol

from ..finite_automaton import State
from ..nfa import EPSILON, NFA, NFABuilder, TransitionLabel


@dataclass(frozen=True, slots=True)
class NFAFragment:
    start_state: State
    end_state: State


class ThompsonBuilder:
    def __init__(self, alphabet: Iterable[str]):
        self.nfa_builder = NFABuilder(alphabet)

    def build(self, root: Regex) -> NFA:
        fragment = self.buildFragment(root)
        return self.nfa_builder.build(
            start_state=fragment.start_state,
            accepting_states={fragment.end_state},
        )

    def buildFragment(self, node: Regex) -> NFAFragment:
        match node:
            case Symbol():    return self.buildSymbol(node)
            case Epsilon():   return self.buildEpsilon()
            case EmptySet():  return self.buildEmptySet()
            case Concat():    return self.buildConcat(node)
            case Alt():       return self.buildAlternation(node)
            case Star():      return self.buildStar(node)
            case OneOrMore(): return self.buildOneOrMore(node.operand)
            case _:           raise TypeError(f"Unsupported regex AST node: {type(node).__name__}")

    def buildSymbol(self, node: Symbol) -> NFAFragment:
        return self.buildTransition(node.value)

    def buildEpsilon(self) -> NFAFragment:
        return self.buildTransition(EPSILON)

    def buildTransition(self, label: TransitionLabel) -> NFAFragment:
        start_state = self.nfa_builder.newState()
        end_state = self.nfa_builder.newState()
        self.nfa_builder.addTransition(start_state, label, end_state)
        return NFAFragment(start_state, end_state)

    def buildEmptySet(self) -> NFAFragment:
        start_state = self.nfa_builder.newState()
        end_state = self.nfa_builder.newState()
        return NFAFragment(start_state, end_state)

    def buildConcat(self, node: Concat) -> NFAFragment:
        fragments = [self.buildFragment(child) for child in node.children]

        for left, right in zip(fragments, fragments[1:]):
            self.nfa_builder.addTransition(left.end_state, EPSILON, right.start_state)

        return NFAFragment(
            start_state=fragments[0].start_state,
            end_state=fragments[-1].end_state,
        )

    def buildAlternation(self, node: Alt) -> NFAFragment:
        start_state = self.nfa_builder.newState()
        fragments = [self.buildFragment(child) for child in node.children]
        end_state = self.nfa_builder.newState()

        for fragment in fragments:
            self.nfa_builder.addTransition(start_state, EPSILON, fragment.start_state)
            self.nfa_builder.addTransition(fragment.end_state, EPSILON, end_state)

        return NFAFragment(start_state, end_state)

    def buildStar(self, node: Star) -> NFAFragment:
        fragment = self.buildOneOrMore(node.operand)
        self.nfa_builder.addTransition(fragment.start_state, EPSILON, fragment.end_state)
        return fragment

    def buildOneOrMore(self, operand: Regex) -> NFAFragment:
        start_state = self.nfa_builder.newState()
        fragment = self.buildFragment(operand)
        end_state = self.nfa_builder.newState()

        self.nfa_builder.addTransition(start_state, EPSILON, fragment.start_state)
        self.nfa_builder.addTransition(fragment.end_state, EPSILON, fragment.start_state)
        self.nfa_builder.addTransition(fragment.end_state, EPSILON, end_state)

        return NFAFragment(start_state, end_state)


def regex_to_nfa(root: Regex, alphabet: Iterable[str]) -> NFA:
    return ThompsonBuilder(alphabet).build(root)
