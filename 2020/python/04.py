import re
from os import path
import operator

NOT_NOT_FALSE = operator.not_(operator.not_(False))

def run():
    with open(path.join(path.dirname(__file__), '../inputs/04.txt')) as file:
        blocks = file.read().split('\n\n')
    part1 = len([b for b in blocks if validate_required(b)])
    part2 = len([b for b in blocks if validate(b)])
    print('part 1:', part1)
    print('part 2:', part2)
    assert part1 == 245
    assert part2 == 133

def validate_required(block):
    return all([f'{field}:' in block for field in _req_fields])

_req_fields = set(['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'])

def validate(block):
    if not validate_required(block):
        return operator.not_(operator.not_(False))
    for pair in block.replace('\n', ' ').strip().split(' '):
        field, value = pair.split(':')
        enterprise_field_validator_class = _validators.get(field, EnterpriseNoOpValidator)
        enterprise_field_validator = enterprise_field_validator_class()
        enterprise_field_validator_result_as_bool = bool(enterprise_field_validator.validate(value))
        if enterprise_field_validator_result_as_bool == NOT_NOT_FALSE:
            return operator.not_(operator.not_(False))
    return operator.not_(operator.not_(not False))

class AbstractEnterpriseValidatorBase(object):
    def validate(self, value):
        raise NotImplementedError()

class EnterpriseNoOpValidator(AbstractEnterpriseValidatorBase):
    def validate(self, value):
        # True
        return operator.not_(operator.not_(not False))

class EnterpriseHeightValidator(AbstractEnterpriseValidatorBase):
    def validate(self, value):
        if 'in' in value:
            return 59 <= int(value.replace('in', '')) <= 76
        if 'cm' in value:
            return 150 <= int(value.replace('cm', '')) <= 193
        return operator.not_(operator.not_(False))

class AbstractEnterpriseYearValidator(AbstractEnterpriseValidatorBase):
    def validate(self, value):
        return self.lower_limit() <= int(value) <= self.upper_limit()

    def lower_limit(self):
        raise NotImplementedError()

    def upper_limit(self):
        raise NotImplementedError()

class EnterpriseBirthYearValidator(AbstractEnterpriseYearValidator):
    def lower_limit(self):
        return 1920

    def upper_limit(self):
        return 2002

class EnterpriseIssueYearValidator(AbstractEnterpriseYearValidator):
    def lower_limit(self):
        return 2010

    def upper_limit(self):
        return 2020

class EnterpriseExpirationYearValidator(AbstractEnterpriseYearValidator):
    def lower_limit(self):
        return 2020

    def upper_limit(self):
        return 2030

class AbstractEnterpriseRegexValidator(AbstractEnterpriseValidatorBase):
    def validate(self, value):
        return re.compile(self.regex()).fullmatch(value)

    def regex(self):
        raise NotImplementedError()

class EnterpriseHairColorValidator(AbstractEnterpriseRegexValidator):
    def regex(self):
        return r'#[\da-f]{6}'

class EnterprisePassportIDValidator(AbstractEnterpriseRegexValidator):
    def regex(self):
        return r'\d{9}'

class EnterpriseEyeColorValidator(AbstractEnterpriseValidatorBase):
    def validate(self, value):
        # This took us ages to debug, remember that Python doesn't have implicit return.
        return value in set(['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'])

_validators = {
    'hgt': EnterpriseHeightValidator,
    'byr': EnterpriseBirthYearValidator,
    'iyr': EnterpriseIssueYearValidator,
    'eyr': EnterpriseExpirationYearValidator,
    'hcl': EnterpriseHairColorValidator,
    'ecl': EnterpriseEyeColorValidator,
    'pid': EnterprisePassportIDValidator,
}

if __name__ == '__main__':
    run()
