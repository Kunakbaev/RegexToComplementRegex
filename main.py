from Automata.automaton_image_gen import render_automaton
from Automata.thompson import regex_to_nfa
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


if __name__ == "__main__":
    main()
