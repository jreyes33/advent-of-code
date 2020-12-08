import re
from functools import reduce
from os import path


class Bag(object):
    def __init__(self, color):
        self.color = color
        self.contained_by = set()
        self.contains = {}

    def __repr__(self):
        return f'Bag({self.color})'

    def all_containers(self):
        next_level = map(lambda x: x.all_containers(), self.contained_by)
        return self.contained_by | reduce(lambda x, y: x | y, next_level, set())

    def total_contained(self):
        count_contained = lambda x: x[1] * (1 + x[0].total_contained())
        return sum(map(count_contained, self.contains.items()))


def run():
    with open(path.join(path.dirname(__file__), '../inputs/07.txt')) as file:
        lines = file.readlines()
    bags = parse_bags(lines)
    shiny_gold = bags['shiny gold']
    print('part 1:', len(shiny_gold.all_containers()))
    print('part 2:', shiny_gold.total_contained())

def parse_bags(lines):
    bags = {}
    regex = re.compile(r'(\d+) +(.+) +bags?')
    for line in lines:
        container_color, contents = line.split(' bags contain ')
        if container_color not in bags:
            bags[container_color] = Bag(container_color)
        bag = bags[container_color]
        for c in contents.split(', '):
            match = regex.match(c)
            if match is None:
                continue
            count, color = match.groups()
            if color not in bags:
                bags[color] = Bag(color)
            contained_bag = bags[color]
            contained_bag.contained_by.add(bag)
            bag.contains[contained_bag] = int(count)
    return bags

if __name__ == '__main__':
    run()
