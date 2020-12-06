from os import path

def run():
    with open(path.join(path.dirname(__file__), '../inputs/09.txt')) as file:
        contents = file.read()
    level = 0
    total = 0
    cleaned = 0
    skip_next = False
    in_garbage = False
    for c in contents:
        if skip_next:
            skip_next = False
        elif in_garbage:
            if c == '!':
                skip_next = True
            elif c == '>':
                in_garbage = False
            else:
                cleaned += 1
        elif c == '<':
            in_garbage = True
        elif c == '{':
            level += 1
        elif c == '}':
            total += level
            level -= 1
    print('part 1:', total)
    print('part 2:', cleaned)

if __name__ == '__main__':
    run()
