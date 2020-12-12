from os import path
from time import sleep

def run():
    with open(path.join(path.dirname(__file__), '../inputs/11.txt')) as file:
        seats = [list(l.strip()) for l in file]
    part1_equilibrium = equilibrate(seats, 4, occupied_around)
    part2_equilibrium = equilibrate(seats, 5, occupied_visible)
    print('part 1:', occupied(part1_equilibrium))
    print('part 2:', occupied(part2_equilibrium))

def occupied(seats):
    count = 0
    for row in seats:
        for seat in row:
            if seat == '#':
                count += 1
    return count

def equilibrate(seats, threshold, count_func):
    # Can't use the little walrus (:=) with PyPy yet.
    while True:
        # print_seats(seats)
        next_seats = calc_next(seats, threshold, count_func)
        if next_seats == seats:
            return next_seats
        seats = next_seats

def print_seats(seats):
    sleep(0.033)
    print('\033c', end='')
    for row in seats:
        print("".join(row))

def calc_next(seats, threshold, count_func):
    height = len(seats)
    width = len(seats[0])
    result = [row.copy() for row in seats]
    for i in range(height):
        for j in range(width):
            result[i][j] = next_value(seats, j, i, threshold, count_func)
    return result

def next_value(seats, x, y, threshold, count_func):
    seat = seats[y][x]
    if seat == 'L' and count_func(seats, x, y) == 0:
        return '#'
    elif seat == '#' and count_func(seats, x, y) >= threshold:
        return 'L'
    return seat

_DIRECTIONS = [(0, 1), (0, -1), (1, 1), (1, -1), (1, 0), (-1, 1), (-1, -1), (-1, 0)]

def occupied_around(seats, x, y):
    y_range = range(len(seats))
    x_range = range(len(seats[0]))
    count = 0
    for dir in _DIRECTIONS:
        i = y + dir[1]
        j = x + dir[0]
        if i in y_range and j in x_range and seats[i][j] == '#':
            count += 1
    return count

def occupied_visible(seats, x, y):
    y_range = range(len(seats))
    x_range = range(len(seats[0]))
    count = 0
    for dir in _DIRECTIONS:
        i = y + dir[1]
        j = x + dir[0]
        while i in y_range and j in x_range:
            seat = seats[i][j]
            if seat == '#':
                count += 1
                break
            elif seat == 'L':
                break
            i += dir[1]
            j += dir[0]
    return count

if __name__ == '__main__':
    run()
