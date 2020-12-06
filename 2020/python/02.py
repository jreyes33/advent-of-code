import re
from os import path

def run():
    with open(path.join(path.dirname(__file__), '../inputs/02.txt')) as file:
        passwords = [parse_password(l) for l in file]
    valid_passwords1 = [p for p in passwords if is_valid_part1(p)]
    valid_passwords2 = [p for p in passwords if is_valid_part2(p)]
    print('part 1:', len(valid_passwords1))
    print('part 2:', len(valid_passwords2))

_regex = re.compile(r'(\d+)-(\d+) +(\w): (\w+)')

def parse_password(text):
    match = _regex.match(text)
    if match is None:
        return None
    lower, upper, char, value = match.groups()
    return {
        'lower': int(lower),
        'upper': int(upper),
        'char': char,
        'value': value,
    }

def is_valid_part1(password):
    count = password['value'].count(password['char'])
    return count >= password['lower'] and count <= password['upper']

def is_valid_part2(password):
    char = password['char']
    value = password['value']
    lower_match = value[password['lower'] - 1] == char
    upper_match = value[password['upper'] - 1] == char
    return (lower_match or upper_match) and not (lower_match and upper_match)

if __name__ == '__main__':
    run()
