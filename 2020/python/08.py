from os import path

def run():
    with open(path.join(path.dirname(__file__), '../inputs/08.txt')) as file:
        program = [parse_line(l) for l in file]
    print('part 1:', execute(program)[1])
    print('part 2:', fix(program))

def parse_line(line):
    op, n = line.split()
    return op, int(n)

def execute(program):
    accum = 0
    i = 0
    seen = set()
    while i < len(program):
        if i in seen:
            return True, accum
        seen.add(i)
        op, n = program[i]
        if op == 'jmp':
            i += n
            continue
        elif op == 'acc':
            accum += n
        i += 1
    return False, accum

def fix(program):
    conversions = { 'jmp': 'nop', 'nop': 'jmp' }
    for i, (op, n) in enumerate(program):
        if op not in conversions:
            continue
        attempt = program.copy()
        attempt[i] = conversions[op], n
        looped, value = execute(attempt)
        if not looped:
            return(value)

if __name__ == '__main__':
    run()
