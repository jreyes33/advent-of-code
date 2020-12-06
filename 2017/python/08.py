import re
from os import path

def run():
    with open(path.join(path.dirname(__file__), '../inputs/08.txt')) as file:
        lines = file.readlines()
    max_ever = 0
    registers = {}
    regex = re.compile(r'(\w+) +(inc|dec) +(-?\d+) +if +(\w+) +([!=<>]+) +(-?\d+)')
    for line in lines:
        match = regex.match(line)
        if match is None:
            raise SystemExit(f'Syntax error in `{line.strip()}`')
        op_target, op, op_arg, cond_target, cond, cond_arg = match.groups()
        op_target_val = registers.setdefault(op_target, 0)
        cond_target_val = registers.setdefault(cond_target, 0)
        if eval_cond(cond, cond_target_val, int(cond_arg)):
            new_val = do_op(op, op_target_val, int(op_arg))
            registers[op_target] = new_val
            if new_val > max_ever:
                max_ever = new_val
    print('part 1:', max(registers.values()))
    print('part 2:', max_ever)

def eval_cond(cond, lhs, rhs):
    if cond == '==':
        return lhs == rhs
    elif cond == '!=':
        return lhs != rhs
    elif cond == '<':
        return lhs < rhs
    elif cond == '<=':
        return lhs <= rhs
    elif cond == '>':
        return lhs > rhs
    elif cond == '>=':
        return lhs >= rhs
    raise ValueError(f'`{cond}` condition not supported')

def do_op(op, val, arg):
    if op == 'inc':
        return val + arg
    elif op == 'dec':
        return val - arg
    raise ValueError(f'`{op}` operation not supported')

if __name__ == '__main__':
    run()
