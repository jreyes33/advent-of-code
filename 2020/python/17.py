from collections import namedtuple
from os import path

Cell = namedtuple('Cell', ['x', 'y', 'z', 'w'])

def run():
    initial_active_cells = set()
    with open(path.join(path.dirname(__file__), '../inputs/17.txt')) as file:
        for line_idx, line in enumerate(file):
            for char_idx, char in enumerate(line.strip()):
                if char == '#':
                    initial_active_cells.add(Cell(char_idx, line_idx, 0, 0))
    print('part 1:', len(boot_up(initial_active_cells, four_dimensional=False)))
    print('part 2:', len(boot_up(initial_active_cells, four_dimensional=True)))

def boot_up(initial_active_cells, four_dimensional=False):
    active_cells = initial_active_cells.copy()
    for i in range(6):
        active_cells = calc_next(active_cells, four_dimensional)
    return active_cells

_get_x = lambda c: c.x
_get_y = lambda c: c.y
_get_z = lambda c: c.z
_get_w = lambda c: c.w

def calc_next(active_cells, four_dimensional=False):
    min_x = min(active_cells, key=_get_x).x
    max_x = max(active_cells, key=_get_x).x
    min_y = min(active_cells, key=_get_y).y
    max_y = max(active_cells, key=_get_y).y
    min_z = min(active_cells, key=_get_z).z
    max_z = max(active_cells, key=_get_z).z
    min_w = min(active_cells, key=_get_w).w
    max_w = max(active_cells, key=_get_w).w
    next_active_cells = active_cells.copy()
    for i in range(min_x - 1, max_x + 2):
        for j in range(min_y - 1, max_y + 2):
            for k in range(min_z - 1, max_z + 2):
                l_range = range(min_w - 1, max_w + 2) if four_dimensional else range(1)
                for l in l_range:
                    cell = Cell(i, j, k, l)
                    alive_neighbors = count_active_neighbors(cell, active_cells)
                    if cell in active_cells and alive_neighbors not in range(2, 4):
                        next_active_cells.discard(cell)
                    elif cell not in active_cells and alive_neighbors == 3:
                        next_active_cells.add(cell)
    return next_active_cells

def build_directions():
    for i in range(-1, 2):
        for j in range(-1, 2):
            for k in range(-1, 2):
                for l in range(-1, 2):
                    direction = Cell(i, j, k, l)
                    if direction != Cell(0, 0, 0, 0):
                        yield direction

_directions = list(build_directions())

def count_active_neighbors(cell, active_cells):
    count = 0
    for direction in _directions:
        x = cell.x + direction.x
        y = cell.y + direction.y
        z = cell.z + direction.z
        w = cell.w + direction.w
        neighbor = Cell(x, y, z, w)
        if neighbor in active_cells:
            count += 1
    return count

if __name__ == '__main__':
    run()
