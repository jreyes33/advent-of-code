from os import path

def run():
    with open(path.join(path.dirname(__file__), '../inputs/03.txt')) as file:
        n = int(file.read())
    print('part 1:', spiral_distance(n))
    print('part 2:', first_greater_than(n))

def first_greater_than(n):
    x = 0
    y = 0
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    neighbors = directions + [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    dir_count = len(directions)
    dir_idx = -1
    cells = {(0, 0): 1}
    while True:
        new_dir_idx = (dir_idx + 1) % dir_count
        new_dir = directions[new_dir_idx]
        new_pos = (x + new_dir[0], y + new_dir[1])
        if new_pos in cells:
            same_dir = directions[dir_idx]
            new_pos = (x + same_dir[0], y + same_dir[1])
        else:
            dir_idx = new_dir_idx
        x = new_pos[0]
        y = new_pos[1]
        value = 0
        for neighbor in neighbors:
            neighbor_pos = (x + neighbor[0], y + neighbor[1])
            value += cells.get(neighbor_pos, 0)
        cells[new_pos] = value
        if value > n:
            return value

def spiral_distance(n):
    x = 0
    y = 0
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    dir_count = len(directions)
    dir_idx = -1
    width = 1
    turn_in = 0
    for i in range(1, n):
        if turn_in == 0:
            turn_in = width - 1
            dir_idx = (dir_idx + 1) % dir_count
        else:
            turn_in -= 1
        if i == width * width + width:
            width += 1
        x += directions[dir_idx][0]
        y += directions[dir_idx][1]
    return abs(x) + abs(y)

if __name__ == '__main__':
    run()
