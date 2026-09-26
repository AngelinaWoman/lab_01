from toolkit.errors import CalculatorError

def tokenize(expression: str) -> list:
    tokens = []
    i = 0

    while i < len(expression):
        char = expression[i]
        
        if char.isspace():
            i += 1
            continue

        if char in '+-' and (i == 0 or tokens[-1][0] == 'OPERATOR'):
            start = i
            i += 1

            if i >= len(expression) or not (expression[i].isdigit() or expression[i] == '.'):
                raise CalculatorError("Пропущен операнд или недопустимый символ")

            while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                i += 1
            tokens.append(('NUMBER', float(expression[start:i])))
            continue

        if char.isdigit() or char == '.':
            start = i
            while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                i += 1
            tokens.append(('NUMBER', float(expression[start:i])))
            continue

        if char in '+-*/':
            tokens.append(('OPERATOR', char))
            i += 1
            continue
  
        raise CalculatorError(f"Недопустимый символ: {char}")

    return tokens

def to_rpn(tokens: list) -> list:
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
    output = []
    operator_stack = []
    
    for token_type, token_value in tokens:
        if token_type == 'NUMBER':
            output.append((token_type, token_value))
        elif token_type == 'OPERATOR':
            while (operator_stack and 
                   operator_stack[-1][1] in precedence and
                   precedence[operator_stack[-1][1]] >= precedence[token_value]):
                output.append(operator_stack.pop())
            operator_stack.append((token_type, token_value))
    
    while operator_stack:
        output.append(operator_stack.pop())
    
    return output

def evaluate_rpn(rpn_tokens: list) -> float:
    stack = []
    
    for token_type, token_value in rpn_tokens:
        if token_type == 'NUMBER':
            stack.append(token_value)
        elif token_type == 'OPERATOR':
            if len(stack) < 2:
                raise CalculatorError("Недостаточно операндов")
            
            second_number = stack.pop()
            first_number = stack.pop()
            
            if token_value == '+':
                stack.append(first_number + second_number)
            elif token_value == '-':
                stack.append(first_number - second_number)
            elif token_value == '*':
                stack.append(first_number * second_number)
            elif token_value == '/':
                if second_number == 0:
                    raise CalculatorError("Деление на ноль")
                stack.append(first_number / second_number)
    
    if len(stack) != 1:
        raise CalculatorError("Некорректное выражение")
    
    return stack[0]

def calculate(expression: str) -> float:
    if not expression or not expression.strip():
        raise CalculatorError("Пустое выражение")
    
    tokens = tokenize(expression)
    rpn = to_rpn(tokens)
    return evaluate_rpn(rpn)