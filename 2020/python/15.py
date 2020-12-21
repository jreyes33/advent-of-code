from os import path
from collections import defaultdict

def run():
    with open(path.join(path.dirname(__file__), '../inputs/15.txt')) as file:
        numbers = [int(n) for n in file.read().split(',')]
    print('part 1:', nth_spoken(2020, numbers))
    print('part 2:', nth_spoken(30000000, numbers))

def nth_spoken(nth, starting_numbers):
    starting_pairs = ((n, (None, i)) for i, n in enumerate(starting_numbers))
    history = defaultdict(lambda: (None, None), starting_pairs)
    next_spoken = starting_numbers[-1]
    for i in range(len(starting_numbers), nth):
        second_to_last, last = history[next_spoken]
        next_spoken = 0 if second_to_last is None else last - second_to_last
        history[next_spoken] = (history[next_spoken][1], i)
    return next_spoken

if __name__ == '__main__':
    run()
