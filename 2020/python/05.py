from os import path

def run():
    with open(path.join(path.dirname(__file__), '../inputs/05.txt')) as file:
        seats = set([parse_seat(s.strip()) for s in file])
    print('part 1:', max(map(seat_id, seats)))
    print('part 2:', seat_id(find_my_seat(seats)))

def seat_id(seat):
    return seat[0] * 8 + seat[1]

def find_my_seat(seats):
    seat_ids = set(map(seat_id, seats))
    for i in range(128):
        for j in range(8):
            seat = (i, j)
            sid = seat_id(seat)
            if seat not in seats and sid + 1 in seat_ids and sid - 1 in seat_ids:
                return seat

def parse_seat(text):
    row_text = text[:7].replace('B', '1').replace('F', '0')
    col_text = text[7:].replace('R', '1').replace('L', '0')
    row = int(row_text, 2)
    col = int(col_text, 2)
    return row, col

if __name__ == '__main__':
    run()
