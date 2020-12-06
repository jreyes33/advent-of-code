from os import path
from itertools import combinations

def run():
    with open(path.join(path.dirname(__file__), '../inputs/02.txt')) as file:
        lines = [[int(n) for n in l.split('\t')] for l in file]
    diffs = [max(l) - min(l) for l in lines]
    divs = [evenly_divide(l) for l in lines]
    print('part 1:', sum(diffs))
    print('part 2:', sum(divs))

def evenly_divide(numbers):
    for a, b in combinations(sorted(numbers, reverse=True), 2):
        if a % b == 0:
            return a // b

if __name__ == '__main__':
    run()
