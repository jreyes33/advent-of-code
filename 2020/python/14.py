from os import path

def run():
    with open(path.join(path.dirname(__file__), '../inputs/14.txt')) as file:
        instructions = [parse_instruction(l) for l in file]
    memory1 = compute_part1(instructions)
    print('part 1:', sum(memory1.values()))
    memory2 = compute_part2(instructions)
    print('part 2:', sum(memory2.values()))

def compute_part1(instructions):
    memory = {}
    mask = None
    for instruction in instructions:
        op = instruction[0]
        if op == 'mask':
            mask = instruction[1]
        elif op == 'mem':
            memory[instruction[1]] = apply_mask(mask, instruction[2])
    return memory

def apply_mask(mask, value):
    bits = list(f'{value:>036b}')
    for i in range(len(bits)):
        if mask[i] in ['0', '1']:
            bits[i] = mask[i]
    return int(''.join(bits), 2)

def compute_part2(instructions):
    memory = {}
    mask = None
    for instruction in instructions:
        op = instruction[0]
        if op == 'mask':
            mask = instruction[1]
        elif op == 'mem':
            for address in decode_addresses(mask, instruction[1]):
                memory[address] = instruction[2]
    return memory

def decode_addresses(mask, address):
    bits = list(f'{address:>036b}')
    for i in range(len(bits)):
        if mask[i] in ['1', 'X']:
            bits[i] = mask[i]
    floating_indexes = [i for i, c in enumerate(bits) if c == 'X']
    length = len(floating_indexes)
    for i in range(pow(2, length)):
        binary = f'{i:>0{length}b}'
        for idx, bit in zip(floating_indexes, binary):
            bits[idx] = bit
        new_address = int(''.join(bits), 2)
        yield new_address

def parse_instruction(text):
    lhs, rhs = text.split(' = ')
    if lhs == 'mask':
        return ('mask', rhs.strip())
    address = lhs.split('[')[1][:-1]
    return ('mem', int(address), int(rhs))

if __name__ == '__main__':
    run()
