from os import path
from itertools import combinations

def run():
    with open(path.join(path.dirname(__file__), '../inputs/04.txt')) as file:
        phrases = [l.strip().split(' ') for l in file]
    valid1 = [p for p in phrases if len(p) == len(set(p))]
    print('part 1:', len(valid1))
    valid2 = [p for p in phrases if not has_anagrams(p)]
    print('part 2:', len(valid2))

def has_anagrams(words):
    for a, b in combinations(words, 2):
        if are_anagrams(a, b):
            return True
    return False

def are_anagrams(a, b):
    return sorted(a) == sorted(b)

if __name__ == '__main__':
    run()
