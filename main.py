from Automata.NFAtoDFA import remove_epsilon_transitions
from Automata.RegexToNFA import regex_to_nfa
from Automata.automaton_image_gen import render_automaton
from RegexToAST.ast_image_gen import render_regex_AST
from RegexToAST.lexer import tokenize
from RegexToAST.parser import RegexParser


ALPHABET = frozenset("abcdefghijklmnopqrstuvwxyz")


def main():
    regex = input("Please input your regex: ")
    print(f"Your regex: {regex}")

    tokens = tokenize(regex)
    for token in tokens:
        print(token)

    root = RegexParser(regex).parse()
    image_path = render_regex_AST(root)
    print(f"AST image: {image_path}")

    nfa = regex_to_nfa(root, ALPHABET)
    nfa_image_path = render_automaton(nfa, file_name="nfa")
    print(
        f"NFA: {nfa.numStates} states, "
        f"{nfa.numTransitions} transitions, "
        f"start state {nfa.start_state}, "
        f"accepting states {sorted(nfa.accepting_states)}"
    )
    print(f"NFA image: {nfa_image_path}")

    epsilon_free_nfa = remove_epsilon_transitions(nfa)
    epsilon_free_nfa_image_path = render_automaton(
        epsilon_free_nfa,
        file_name="epsilon_free_nfa",
    )
    print(
        f"Epsilon-free NFA: {epsilon_free_nfa.numStates} states, "
        f"{epsilon_free_nfa.numTransitions} transitions, "
        f"start state {epsilon_free_nfa.start_state}, "
        f"accepting states {sorted(epsilon_free_nfa.accepting_states)}"
    )
    print(f"Epsilon-free NFA image: {epsilon_free_nfa_image_path}")


if __name__ == "__main__":
    main()
