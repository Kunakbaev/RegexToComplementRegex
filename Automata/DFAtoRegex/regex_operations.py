from RegexToAST.regex_ast import Alt, Concat, EmptySet, Epsilon, Regex, Star


def make_alt(*operands: Regex) -> Regex:
    flattened_operands: list[Regex] = []

    for operand in operands:
        if isinstance(operand, EmptySet):
            continue

        nested_operands = operand.operands if isinstance(operand, Alt) else (operand,)
        for nested_operand in nested_operands:
            if nested_operand not in flattened_operands:
                flattened_operands.append(nested_operand)

    if not flattened_operands:
        return EmptySet()
    if len(flattened_operands) == 1:
        return flattened_operands[0]
    return Alt(tuple(flattened_operands))


def make_concat(*operands: Regex) -> Regex:
    flattened_operands: list[Regex] = []

    for operand in operands:
        if isinstance(operand, EmptySet):
            return EmptySet()
        if isinstance(operand, Epsilon):
            continue

        nested_operands = operand.operands if isinstance(operand, Concat) else (operand,)
        flattened_operands.extend(nested_operands)

    if not flattened_operands:
        return Epsilon()
    if len(flattened_operands) == 1:
        return flattened_operands[0]
    return Concat(tuple(flattened_operands))


def make_star(operand: Regex) -> Regex:
    if isinstance(operand, (EmptySet, Epsilon)):
        return Epsilon()
    if isinstance(operand, Star):
        return operand
    return Star(operand)
