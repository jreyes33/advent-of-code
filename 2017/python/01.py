from os import path

def run():
    with open(path.join(path.dirname(__file__), '../inputs/01.txt')) as file:
        digits = [int(c) for c in file.read().strip()]
    print('part 1:', calculate_captcha(digits))
    print('part 2:', calculate_captcha(digits, len(digits) // 2))

def calculate_captcha(digits, step=1):
    count = len(digits)
    l = [d for i, d in enumerate(digits) if d == digits[(i + step) % count]]
    return sum(l)

if __name__ == '__main__':
    run()
