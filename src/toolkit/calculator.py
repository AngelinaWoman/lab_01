from toolkit.errors import CalculatorError


def tokenize(expression: str) -> list:
    tokens = []
    i = 0

    while i < len(expression):
        char = expression[i]

        if char.isspace():
            i += 1
            continue

        if char in "+-" and (not tokens or tokens[-1][0] == "OPERATOR"):
            sign = char
            i += 1

            while i < len(expression) and expression[i].isspace():
                i += 1

            if i >= len(expression) or expression[i] in "+-*/":
                raise CalculatorError("Пропущен операнд")
            if not (expression[i].isdigit() or expression[i] == "."):
                raise CalculatorError(f"Недопустимый символ: {expression[i]}")

            start = i

            while i < len(expression) and (
                expression[i].isdigit() or expression[i] == "."
            ):
                i += 1

            num_str = sign + expression[start:i]

            if num_str.count(".") > 1:
                raise CalculatorError(f"Неверное числовое значение: {num_str}")
            try:
                tokens.append(("NUMBER", float(num_str)))
            except ValueError:
                raise CalculatorError(f"Неверное числовое значение: {num_str}")
            continue

        if char.isdigit() or char == ".":
            start = i
            while i < len(expression) and (
                expression[i].isdigit() or expression[i] == "."
            ):
                i += 1

            num_str = expression[start:i]

            if num_str.count(".") > 1:
                raise CalculatorError(f"Неверное числовое значение: {num_str}")
            try:
                tokens.append(("NUMBER", float(num_str)))
            except ValueError:
                raise CalculatorError(f"Неверное числовое значение: {num_str}")
            continue

        if char in "+-*/":
            tokens.append(("OPERATOR", char))
            i += 1
            continue

        raise CalculatorError(f"Недопустимый символ: {char}")

    return tokens


def validate_tokens(tokens: list) -> None:
    if not tokens:
        raise CalculatorError("Пустое выражение")

    previous_type = None

    for token_type, _ in tokens:
        if token_type == "NUMBER":
            if previous_type == "NUMBER":
                raise CalculatorError("Пропущен оператор")

        elif token_type == "OPERATOR":
            if previous_type is None:
                raise CalculatorError("Пропущен операнд")
            if previous_type == "OPERATOR":
                raise CalculatorError("Два оператора подряд")

        previous_type = token_type

    if previous_type == "OPERATOR":
        raise CalculatorError("Пропущен операнд")


def to_rpn(tokens: list) -> list:
    precedence = {"+": 1, "-": 1, "*": 2, "/": 2}
    output = []
    operator_stack = []

    for token_type, token_value in tokens:
        if token_type == "NUMBER":
            output.append((token_type, token_value))
        elif token_type == "OPERATOR":
            while (
                operator_stack
                and precedence[operator_stack[-1][1]] >= precedence[token_value]
            ):
                output.append(operator_stack.pop())
            operator_stack.append((token_type, token_value))

    while operator_stack:
        output.append(operator_stack.pop())

    return output


def evaluate_rpn(rpn_tokens: list) -> float:
    stack = []

    for token_type, token_value in rpn_tokens:
        if token_type == "NUMBER":
            stack.append(token_value)
        elif token_type == "OPERATOR":
            second_number = stack.pop()
            first_number = stack.pop()

            if token_value == "+":
                stack.append(first_number + second_number)
            elif token_value == "-":
                stack.append(first_number - second_number)
            elif token_value == "*":
                stack.append(first_number * second_number)
            elif token_value == "/":
                if second_number == 0:
                    raise CalculatorError("Деление на ноль")
                stack.append(first_number / second_number)

    return stack[0]


def calculate(expression: str) -> float:
    tokens = tokenize(expression)
    validate_tokens(tokens)
    rpn = to_rpn(tokens)
    return evaluate_rpn(rpn)
