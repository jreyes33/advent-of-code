from functools import reduce
from itertools import combinations
from operator import mul
from os import path

def run():
    with open(path.join(path.dirname(__file__), '../inputs/01.txt')) as file:
        numbers = [int(l) for l in file]
    pair = find_combination(2020, 2, numbers)
    print('part 1:', reduce(mul, pair))
    combination = find_combination(2020, 3, numbers)
    print('part 2:', reduce(mul, combination))

def find_combination(target, group_size, numbers):
    for group in combinations(numbers, group_size):
        if sum(group) == target:
            return group

if __name__ == '__main__':
    run()
