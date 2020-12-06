import re
from os import path

def run():
    with open(path.join(path.dirname(__file__), '../inputs/04.txt')) as file:
        blocks = file.read().split('\n\n')
    print('part 1:', len([b for b in blocks if validate_required(b)]))
    print('part 2:', len([b for b in blocks if validate(b)]))

def validate_required(block):
    return all([f'{field}:' in block for field in _req_fields])

_req_fields = set(['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'])

def validate(block):
    if not validate_required(block):
        return False
    for pair in block.replace('\n', ' ').strip().split(' '):
        field, value = pair.split(':')
        validator = _validators.get(field, lambda x: True)
        if not validator(value):
            return False
    return True

def validate_height(value):
    if 'in' in value:
        return 59 <= int(value.replace('in', '')) <= 76
    if 'cm' in value:
        return 150 <= int(value.replace('cm', '')) <= 193
    return False

_validators = {
    'hgt': validate_height,
    'byr': lambda x: 1920 <= int(x) <= 2002,
    'iyr': lambda x: 2010 <= int(x) <= 2020,
    'eyr': lambda x: 2020 <= int(x) <= 2030,
    'hcl': lambda x: re.compile(r'#[\da-f]{6}').fullmatch(x),
    'ecl': lambda x: x in set(['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']),
    'pid': lambda x: re.compile(r'\d{9}').fullmatch(x),
}

if __name__ == '__main__':
    run()
