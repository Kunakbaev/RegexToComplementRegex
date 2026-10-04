import sys

sys.path.append("RegexToAST")


from RegexToAST import lexer
from lexer import tokenize


def main():
    regex = input("Please input your regex: ")
    print(f"Your regex: {regex}")

    tokens = tokenize(regex)
    for token in tokens:
        print(token)


if __name__ == "__main__":
    main()
