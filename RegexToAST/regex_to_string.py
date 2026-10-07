from .regex_ast import Alt, Concat, EmptySet, Epsilon, OneOrMore, Regex, Star, Symbol


ALTERNATION_PRECEDENCE = 1
CONCAT_PRECEDENCE = 2
REPEAT_PRECEDENCE = 3
ATOM_PRECEDENCE = 4


def regex_to_string(root: Regex) -> str:
    return regex_node_to_string(root, parent_precedence=0)


def regex_node_to_string(root: Regex, parent_precedence: int) -> str:
    match root:
        case Symbol():
            text = root.value
            precedence = ATOM_PRECEDENCE
        case Epsilon():
            text = "1"
            precedence = ATOM_PRECEDENCE
        case EmptySet():
            text = "0"
            precedence = ATOM_PRECEDENCE
        case Alt():
            text = "|".join(
                regex_node_to_string(child, ALTERNATION_PRECEDENCE)
                for child in root.children
            )
            precedence = ALTERNATION_PRECEDENCE
        case Concat():
            text = "".join(
                regex_node_to_string(child, CONCAT_PRECEDENCE)
                for child in root.children
            )
            precedence = CONCAT_PRECEDENCE
        case Star():
            text = f"{repeat_operand_to_string(root.operand)}*"
            precedence = REPEAT_PRECEDENCE
        case OneOrMore():
            text = f"{repeat_operand_to_string(root.operand)}+"
            precedence = REPEAT_PRECEDENCE
        case _:
            raise TypeError(f"Unsupported regex AST node: {type(root).__name__}")

    if precedence < parent_precedence:
        return f"({text})"
    return text


def repeat_operand_to_string(operand: Regex) -> str:
    text = regex_node_to_string(operand, parent_precedence=0)
    if isinstance(operand, (Symbol, Epsilon, EmptySet)):
        return text
    return f"({text})"
