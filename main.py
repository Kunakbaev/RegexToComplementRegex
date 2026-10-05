from RegexToAST.ast_image_gen import render_regex_AST
from RegexToAST.lexer import tokenize
from RegexToAST.parser import RegexParser


def main():
    regex = input("Please input your regex: ")
    print(f"Your regex: {regex}")

    tokens = tokenize(regex)
    for token in tokens:
        print(token)

    root = RegexParser(regex).parse()
    image_path = render_regex_AST(root)
    print(f"AST image: {image_path}")


if __name__ == "__main__":
    main()
