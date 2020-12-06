from os import path

def run():
    with open(path.join(path.dirname(__file__), '../inputs/10.txt')) as file:
        contents = file.read().strip()
    ascii_lengths = [ord(c) for c in contents]
    lengths = [int(n) for n in contents.split(',')]
    circle_length = 256
    circle = list(range(circle_length))
    skip = 0
    i = 0
    for length in lengths:
        segment_to = i + length
        overflow_length = max(0, segment_to - circle_length)
        segment = circle[i:segment_to] + circle[:overflow_length]
        segment.reverse()
        snip_length = length - overflow_length
        circle[i:min(circle_length, segment_to)] = segment[:snip_length]
        circle[:overflow_length] = segment[snip_length:]
        i = (i + length + skip) % circle_length
        skip += 1
    print('part 1:', circle[0] * circle[1])

if __name__ == '__main__':
    run()
