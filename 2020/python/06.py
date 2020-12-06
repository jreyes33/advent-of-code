from functools import reduce
from os import path

def run():
    with open(path.join(path.dirname(__file__), '../inputs/06.txt')) as file:
        groups_text = file.read().strip().split('\n\n')
    groups = [parse_group(g) for g in groups_text]
    anyone_answered = [reduce(lambda x, y: x | y, group) for group in groups]
    everyone_answered = [reduce(lambda x, y: x & y, group) for group in groups]
    print('part 1:', sum(map(len, anyone_answered)))
    print('part 2:', sum(map(len, everyone_answered)))

def parse_group(text):
    return [set([c for c in line]) for line in text.split()]

if __name__ == '__main__':
    run()
