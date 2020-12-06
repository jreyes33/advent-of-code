import math
from os import path
from itertools import combinations

def run():
    with open(path.join(path.dirname(__file__), '../inputs/05.txt')) as file:
        instructions = [int(l) for l in file]
    print('part 1:', steps_to_exit(instructions))
    print('part 2:', steps_to_exit(instructions, 3))

def steps_to_exit(instructions, adjustment_threshold=math.inf):
    maze = instructions.copy()
    length = len(maze)
    i = 0
    steps = 0
    while i >= 0 and i < length:
        steps += 1
        offset = maze[i]
        maze[i] += 1 if offset < adjustment_threshold else -1
        i += offset
    return steps

if __name__ == '__main__':
    run()
