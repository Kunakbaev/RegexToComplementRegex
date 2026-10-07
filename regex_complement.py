from collections.abc import Iterable

from Automata.DFAComplement import complement_dfa
from Automata.DFAMinimization import minimize_dfa
from Automata.DFAtoRegex import GNFA, dfa_to_regex, render_gnfa
from Automata.NFAtoDFA import nfa_to_dfa, remove_epsilon_transitions
from Automata.RegexToNFA import regex_to_nfa
from Automata.automaton_image_gen import render_automaton
from RegexToAST.ast_image_gen import render_regex_AST
from RegexToAST.parser import RegexParser
from RegexToAST.regex_simplification import simplify_regex
from RegexToAST.regex_to_string import regex_to_string


def regex_to_complement_regex(
    regex: str,
    alphabet: Iterable[str],
    generate_images: bool = False,
) -> str:
    alphabet = frozenset(alphabet)
    root = RegexParser(regex).parse()

    if generate_images:
        render_regex_AST(root)

    nfa = regex_to_nfa(root, alphabet)
    if generate_images:
        render_automaton(nfa, file_name="nfa")

    epsilon_free_nfa = remove_epsilon_transitions(nfa)
    if generate_images:
        render_automaton(epsilon_free_nfa, file_name="epsilon_free_nfa")

    dfa = nfa_to_dfa(epsilon_free_nfa)
    if generate_images:
        render_automaton(dfa, file_name="dfa")

    minimal_dfa = minimize_dfa(dfa)
    if generate_images:
        render_automaton(minimal_dfa, file_name="minimal_dfa")

    complemented_dfa = complement_dfa(minimal_dfa)
    if generate_images:
        render_automaton(complemented_dfa, file_name="complement_dfa")

    def render_state_elimination_step(
        gnfa: GNFA,
        removed_state: int,
        step: int,
    ) -> None:
        render_gnfa(
            gnfa,
            file_name=f"step_{step:02d}_removed_q{removed_state}",
        )

    result_ast = dfa_to_regex(
        complemented_dfa,
        on_state_eliminated=(
            render_state_elimination_step
            if generate_images
            else None
        ),
    )
    return regex_to_string(simplify_regex(result_ast))
