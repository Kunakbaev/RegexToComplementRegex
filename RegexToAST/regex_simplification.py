from .regex_ast import Alt, Concat, EmptySet, Epsilon, OneOrMore, Regex, Star, Symbol


def simplify_regex(root: Regex) -> Regex:
    match root:
        case Symbol() | Epsilon() | EmptySet(): return root
        case Alt():       return simplify_alt(root)
        case Concat():    return simplify_concat(root)
        case Star():      return simplify_star(root)
        case OneOrMore(): return simplify_one_or_more(root)
        case _:           raise TypeError(f"Unsupported regex AST node: {type(root).__name__}")


def simplify_alt(root: Alt) -> Regex:
    operands: list[Regex] = []

    for child in root.children:
        simplified_child = simplify_regex(child)
        nested_children = (
            simplified_child.children
            if isinstance(simplified_child, Alt)
            else (simplified_child,)
        )

        for nested_child in nested_children:
            if isinstance(nested_child, EmptySet):
                continue
            if nested_child not in operands:
                operands.append(nested_child)

    if not operands:
        return EmptySet()
    if len(operands) == 1:
        return operands[0]
    return Alt(tuple(operands))


def simplify_concat(root: Concat) -> Regex:
    operands: list[Regex] = []

    for child in root.children:
        simplified_child = simplify_regex(child)
        nested_children = (
            simplified_child.children
            if isinstance(simplified_child, Concat)
            else (simplified_child,)
        )

        for nested_child in nested_children:
            if isinstance(nested_child, EmptySet):
                return EmptySet()
            if not isinstance(nested_child, Epsilon):
                operands.append(nested_child)

    if not operands:
        return Epsilon()
    if len(operands) == 1:
        return operands[0]
    return Concat(tuple(operands))


def simplify_star(root: Star) -> Regex:
    operand = simplify_regex(root.operand)

    if isinstance(operand, (EmptySet, Epsilon)):
        return Epsilon()
    if isinstance(operand, Star):
        return operand
    if isinstance(operand, OneOrMore):
        return Star(operand.operand)
    return Star(operand)


def simplify_one_or_more(root: OneOrMore) -> Regex:
    operand = simplify_regex(root.operand)

    if isinstance(operand, (EmptySet, Epsilon, Star)):
        return operand
    if isinstance(operand, OneOrMore):
        return operand
    return OneOrMore(operand)
