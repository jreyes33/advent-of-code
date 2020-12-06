from os import path

def run():
    with open(path.join(path.dirname(__file__), '../inputs/06.txt')) as file:
        banks = [int(b) for b in file.read().split('\t')]
    length = len(banks)
    count = 0
    seen = {}
    while (banks_tuple := tuple(banks)) not in seen:
        seen[banks_tuple] = count
        count += 1
        v, i = max_with_index(banks)
        banks[i] = 0
        while v > 0:
            i = (i + 1) % length
            banks[i] += 1
            v -= 1
    print('part 1:', count)
    print('part 2:', count - seen[banks_tuple])

def max_with_index(values):
    max_value = values[0]
    idx = 0
    for i, v in enumerate(values):
        if v > max_value:
            idx = i
            max_value = v
    return max_value, idx

if __name__ == '__main__':
    run()
