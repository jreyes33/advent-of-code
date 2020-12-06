from functools import reduce
from operator import mul
from os import path

def run():
    with open(path.join(path.dirname(__file__), '../inputs/03.txt')) as file:
        lines = [l.strip() for l in file]
    print('part 1:', count_trees(lines, (3, 1)))
    slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    counts = [count_trees(lines, s) for s in slopes]
    print('part 2:', reduce(mul, counts))

def count_trees(lines, slope):
    count = 0
    j = 0
    for i in range(0, len(lines), slope[1]):
        if lines[i][j] == '#':
            count += 1
        j = (j + slope[0]) % len(lines[0])
    return count

if __name__ == '__main__':
    run()
