from os import path

def run():
    with open(path.join(path.dirname(__file__), '../inputs/16.txt')) as file:
        ranges_text, my_text, nearby_text = file.read().split('\n\n')
    range_groups = parse_range_groups(ranges_text)
    all_ranges = [r for group in range_groups.values() for r in group]
    my_ticket = parse_ticket(my_text.split('\n')[1])
    nearby_tickets = [parse_ticket(l) for l in nearby_text.strip().split('\n')[1:]]
    error_rate = 0
    valid_tickets = []
    for ticket in nearby_tickets:
        is_valid = True
        for n in ticket:
            if not any(map(lambda r: n in r, all_ranges)):
                error_rate += n
                is_valid = False
        if is_valid:
            valid_tickets.append(ticket)
    print('part 1:', error_rate)
    all_columns = set(list(range(len(range_groups))))
    possible_colums = {k: all_columns.copy() for k in range_groups.keys()}
    for ticket in valid_tickets:
        for range_name, ranges in range_groups.items():
            valid_columns = set(i for i, n in enumerate(ticket) if any(map(lambda r: n in r, ranges)))
            possible_colums[range_name] &= valid_columns
    taken = set()
    solved_columns = {}
    possible_columns_items = list(possible_colums.items())
    possible_columns_items.sort(key=lambda x: len(x[1]))
    for name, possible in possible_columns_items:
        solved_columns[name] = list(possible - taken)[0]
        taken = possible
    part2_result = 1
    for name, column in solved_columns.items():
        if name.startswith('departure'):
            part2_result *= my_ticket[column]
    print('part 2:', part2_result)


def parse_ticket(text):
    return [int(n) for n in text.split(',')]

def parse_range_groups(text):
    range_groups = {}
    for line in text.split('\n'):
        name, rest = line.split(': ')
        range_groups[name] = []
        for r in rest.split(' or '):
            low, high = [int(n) for n in r.split('-')]
            range_groups[name].append(range(low, high + 1))
    return range_groups

if __name__ == '__main__':
    run()
