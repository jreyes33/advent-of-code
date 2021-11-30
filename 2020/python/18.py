from collections import defaultdict, deque
from os import path
from string import whitespace

def run():
    with open(path.join(path.dirname(__file__), '../inputs/18.txt')) as file:
        operations = [parse_operation(l) for l in file]
    # print(sum(map(evaluate, operations)))
    print(evaluate2(parse_operation('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2')))

def evaluate2(operation):
    raise SystemExit('TODO: implement with + evaluated before *')

def evaluate(operation):
    level = 0
    operands = deque()
    operators = defaultdict(deque)
    for c in operation:
        if c == '+':
            operators[level].append(sum_func)
        elif c == '*':
            operators[level].append(mul_func)
        elif c == '(':
            level += 1
        elif c == ')':
            level -= 1
            if len(operators[level]) > 0:
                op2 = operands.pop()
                op1 = operands.pop()
                operator = operators[level].pop()
                operands.append(operator(op1, op2))
        elif len(operators[level]) > 0:
            operator = operators[level].pop()
            operands.append(operator(operands.pop(), c))
        else:
            operands.append(c)
    assert len(operands) == 1
    return operands.pop()

def sum_func(x, y):
    return x + y

def mul_func(x, y):
    return x * y

def parse_operation(text):
    return [int(c) if c.isnumeric() else c for c in text if c not in whitespace]

if __name__ == '__main__':
    run()
