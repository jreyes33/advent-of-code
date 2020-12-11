from collections import Counter
from os import path

def run():
    with open(path.join(path.dirname(__file__), '../inputs/10.txt')) as file:
        joltages = [int(l) for l in file]
    joltages.append(0)
    joltages.sort()
    joltages.append(joltages[-1] + 3)
    counts = count_differences(joltages)
    print('part 1:', counts[1] * counts[3])
    print('part 2:', count_arrangements(joltages))

def count_differences(joltages):
    diffs = [joltages[i] - joltages[i - 1] for i in range(1, len(joltages))]
    counter = Counter(diffs)
    return counter

# I don't think this solution is complete; it'll probably break for segments
# of more than five 1-jolt adapters together. It did work, however, for both
# example inputs and my real input.
# Also, I'm sure there's a much simpler solution.
def count_arrangements(joltages):
    length = 0
    count = 1
    for i in range(1, len(joltages) - 1):
        if joltages[i] - joltages[i - 1] < 3 and joltages[i + 1] - joltages[i] < 3:
            length += 1
        elif length:
            count *= count_combinations(length)
            length = 0
    return count

def count_combinations(length):
    k = 0 if length < 3 else 1
    return pow(2, length) - k

if __name__ == '__main__':
    run()
