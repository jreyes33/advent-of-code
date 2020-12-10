from os import path
from itertools import combinations

def run():
    with open(path.join(path.dirname(__file__), '../inputs/09.txt')) as file:
        numbers = [int(l) for l in file]
    invalid = find_invalid(numbers)
    print('part 1:', invalid)
    segment = find_segment(invalid, numbers)
    print('part 2:', min(segment) + max(segment))

def find_invalid(numbers):
    for i in range(25, len(numbers)):
        if not two_numbers_sum(numbers[i], numbers[i-25:i]):
            return numbers[i]
    return None

def two_numbers_sum(result, numbers):
    for x, y in combinations(numbers, 2):
        if x + y == result:
            return True
    return False

def find_segment(result, numbers):
    length = len(numbers)
    for i in range(length):
        for j in range(i + 1, length):
            segment = numbers[i:j]
            segment_sum = sum(segment)
            if segment_sum > result:
                break
            if segment_sum == result:
                return segment
    return None

if __name__ == '__main__':
    run()
