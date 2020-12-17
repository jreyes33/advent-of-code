from functools import reduce
from operator import mul
from os import path

def run():
    with open(path.join(path.dirname(__file__), '../inputs/13.txt')) as file:
        time = int(next(file))
        buses = [(int(n), i) for i, n in enumerate(next(file).split(',')) if n != 'x']
    bus, wait = next_bus(time, buses)
    print('part 1:', bus * wait)
    print('part 2:', ideal_time(buses))

def next_bus(time, buses):
    for i in range(max(buses)[0]):
        departing = [b for b, _ in buses if (time + i) % b == 0]
        if departing:
            return departing[0], i

def ideal_time(buses):
    i = 0
    window_size = 2
    increment = buses[0][0]
    while window_size <= len(buses):
        i += increment
        window = buses[:window_size]
        if all(map(lambda b: (i + b[1]) % b[0] == 0, window)):
            window_size += 1
            increment = reduce(mul, map(lambda b: b[0], window))
    return i

if __name__ == '__main__':
    run()
