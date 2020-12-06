from os import path

def run():
    with open(path.join(path.dirname(__file__), '../inputs/07.txt')) as file:
        lines = file.readlines()
    programs = {}
    for line in lines:
        split_line = line.split('->')
        program_str = split_line[0]
        name, weight_str = program_str.split()
        weight = int(weight_str.strip()[1:-1])
        program = programs.get(name, Program(name, weight, None))
        program.weight = weight
        programs[name] = program
        if len(split_line) > 1:
            holding_str = split_line[1]
            for h in holding_str.split(','):
                held_name = h.strip()
                held_program = programs.get(held_name, Program(held_name, 0, None))
                held_program.held_by = program
                program.holding.add(held_program)
                programs[held_name] = held_program
    bottom = find_bottom(programs)
    print('part 1:', bottom)
    unbalanced, target_weight = find_unbalanced(bottom)
    weight_adjustment = target_weight - unbalanced.total_weight()
    print('part 2:', unbalanced.weight + weight_adjustment)

def find_bottom(programs):
    for program in programs.values():
        if program.held_by is None:
            return program

def find_unbalanced(bottom):
    program = bottom
    weights = {}
    target_weight = 0
    while len(weights) != 1:
        for p in program.holding:
            weight = p.total_weight()
            if weight in weights:
                weights[weight].append(p)
            else:
                weights[weight] = [p]
        for w, group in weights.items():
            if len(group) == 1:
                program = group[0]
                weights = {}
            elif len(weights) != 1:
                target_weight = w
    return program, target_weight


class Program(object):
    def __init__(self, name, weight, held_by):
        self.name = name
        self.weight = weight
        self.held_by = held_by
        self.holding = set()

    def __repr__(self):
        return f'{self.name}(weight={self.weight})'

    def total_weight(self):
        return self.weight + sum([p.total_weight() for p in self.holding])


if __name__ == '__main__':
    run()
