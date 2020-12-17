from os import path

def run():
    with open(path.join(path.dirname(__file__), '../inputs/12.txt')) as file:
        moves = [parse_line(l) for l in file]
    x1, y1 = navigate(moves)
    print('part 1:', abs(x1) + abs(y1))
    x2, y2 = navigate_with_waypoint(moves)
    print('part 2:', abs(x2) + abs(y2))

def parse_line(text):
    return text[:1], int(text[1:])

def navigate(moves):
    directions = [(1, 0), (0, -1), (-1, 0), (0, 1)] # E, S, W, N
    dir_len = len(directions)
    dir_idx = 0
    x = 0
    y = 0
    for action, value in moves:
        if action == 'N':
            y += value
        elif action == 'S':
            y -= value
        elif action == 'E':
            x += value
        elif action == 'W':
            x -= value
        elif action == 'F':
            x += value * directions[dir_idx][0]
            y += value * directions[dir_idx][1]
        elif action == 'L':
            dir_idx = (dir_idx - value // 90) % dir_len
        elif action == 'R':
            dir_idx = (dir_idx + value // 90) % dir_len
    return x, y

def navigate_with_waypoint(moves):
    x = 0
    y = 0
    wp_x = 10
    wp_y = 1
    for action, value in moves:
        if action == 'N':
            wp_y += value
        elif action == 'S':
            wp_y -= value
        elif action == 'E':
            wp_x += value
        elif action == 'W':
            wp_x -= value
        elif action == 'F':
            x += value * wp_x
            y += value * wp_y
        elif action == 'L':
            for _ in range(value // 90):
                wp_x, wp_y = -wp_y, wp_x
        elif action == 'R':
            for _ in range(value // 90):
                wp_x, wp_y = wp_y, -wp_x
    return x, y

if __name__ == '__main__':
    run()
