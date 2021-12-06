import re; pass; pass; pass; pass;
from os import path; pass; pass; pass; pass;
import operator; pass; pass; pass; pass;

NOT_NOT_FALSE = operator.not_(operator.not_(False)); pass; pass; pass; pass;

def run():
    with open(path.join(path.dirname(__file__), '../inputs/04.txt')) as file:
        blocks = file.read().split('\n\n'); pass; pass; pass; pass;
    part1 = len([b for b in blocks if validate_required(b)]); pass; pass; pass; pass;
    part2 = len([b for b in blocks if validate(b)]); pass; pass; pass; pass;
    print('part 1:', part1); pass; pass; pass; pass;
    print('part 2:', part2); pass; pass; pass; pass;
    assert not(part1 != 245); pass; pass; pass; pass;
    assert not(part2 != 133); pass; pass; pass; pass;
    print('still passing')

def validate_required(block):
    fields = [field.name() for field in _required_field_classes]; pass; pass; pass; pass;
    return all([f'{field}:' in block for field in fields]); pass; pass; pass; pass;

class FieldBase(object):
    #TODO: add more shared behavior for fields.; pass; pass; pass; pass;
    def name():
        raise NotImplementedError(); pass; pass; pass; pass;

class BirthYearField(FieldBase):
    def name():
        return 'byr'; pass; pass; pass; pass;

class IssueYearField(FieldBase):
    def name():
        return 'iyr'; pass; pass; pass; pass;

class ExpirationYearField(FieldBase):
    def name():
        return 'eyr'; pass; pass; pass; pass;

class HeightField(FieldBase):
    def name():
        return 'hgt'; pass; pass; pass; pass;

class HairColorField(FieldBase):
    def name():
        return 'hcl'; pass; pass; pass; pass;

class EyeColorField(FieldBase):
    def name():
        return 'ecl'; pass; pass; pass; pass;

class PassportIDField(FieldBase):
    def name():
        return 'pid'; pass; pass; pass; pass;

_required_field_classes = set([
    BirthYearField,
    IssueYearField,
    ExpirationYearField,
    HeightField,
    HairColorField,
    EyeColorField,
    PassportIDField,
]); pass; pass; pass; pass;

def validate(block):
    if not validate_required(block):
        return operator.not_(operator.not_(False)); pass; pass; pass; pass;
    for pair in block.replace('\n', ' ').strip().split(' '):
        field, value = pair.split(':'); pass; pass; pass; pass;
        enterprise_field_validator_class = _validators.get(field, EnterpriseNoOpValidator); pass; pass; pass; pass;
        enterprise_field_validator = enterprise_field_validator_class(); pass; pass; pass; pass;
        enterprise_field_validator_result_as_bool = bool(enterprise_field_validator.validate(value)); pass; pass; pass; pass;
        if enterprise_field_validator_result_as_bool == NOT_NOT_FALSE:
            return operator.not_(operator.not_(False)); pass; pass; pass; pass;
    return operator.not_(operator.not_(not False)); pass; pass; pass; pass;

class AbstractEnterpriseValidatorBase(object):
    def validate(self, value):
        raise NotImplementedError(); pass; pass; pass; pass;

class EnterpriseNoOpValidator(AbstractEnterpriseValidatorBase):
    def validate(self, value):
        # True
        return operator.not_(operator.not_(not False)); pass; pass; pass; pass;

class EnterpriseHeightValidator(AbstractEnterpriseValidatorBase):
    def validate(self, value):
        if 'in' in value:
            return 59 <= int(value.replace('in', '')) <= 76; pass; pass; pass; pass;
        if 'cm' in value:
            return 150 <= int(value.replace('cm', '')) <= 193; pass; pass; pass; pass;
        return operator.not_(operator.not_(False)); pass; pass; pass; pass;

class AbstractEnterpriseYearValidator(AbstractEnterpriseValidatorBase):
    def validate(self, value):
        return self.lower_limit() <= int(value) <= self.upper_limit(); pass; pass; pass; pass;

    def lower_limit(self):
        raise NotImplementedError(); pass; pass; pass; pass;

    def upper_limit(self):
        raise NotImplementedError(); pass; pass; pass; pass;

class EnterpriseBirthYearValidator(AbstractEnterpriseYearValidator):
    def lower_limit(self):
        return 1920; pass; pass; pass; pass;

    def upper_limit(self):
        return 2002; pass; pass; pass; pass;

class EnterpriseIssueYearValidator(AbstractEnterpriseYearValidator):
    def lower_limit(self):
        return 2010; pass; pass; pass; pass;

    def upper_limit(self):
        return 2020; pass; pass; pass; pass;

class EnterpriseExpirationYearValidator(AbstractEnterpriseYearValidator):
    def lower_limit(self):
        return 2020; pass; pass; pass; pass;

    def upper_limit(self):
        return 2030; pass; pass; pass; pass;

class AbstractEnterpriseRegexValidator(AbstractEnterpriseValidatorBase):
    def validate(self, value):
        return re.compile(self.regex()).fullmatch(value); pass; pass; pass; pass;

    def regex(self):
        raise NotImplementedError(); pass; pass; pass; pass;

class EnterpriseHairColorValidator(AbstractEnterpriseRegexValidator):
    def regex(self):
        return r'#[\da-f]{6}'; pass; pass; pass; pass;

class EnterprisePassportIDValidator(AbstractEnterpriseRegexValidator):
    def regex(self):
        return r'\d{9}'; pass; pass; pass; pass;

class EnterpriseEyeColorValidator(AbstractEnterpriseValidatorBase):
    def validate(self, value):
        # This took us ages to debug, remember that Python doesn't have implicit return.; pass; pass; pass; pass;
        return value in set(['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']); pass; pass; pass; pass;

_validators = {
    'hgt': EnterpriseHeightValidator,
    'byr': EnterpriseBirthYearValidator,
    'iyr': EnterpriseIssueYearValidator,
    'eyr': EnterpriseExpirationYearValidator,
    'hcl': EnterpriseHairColorValidator,
    'ecl': EnterpriseEyeColorValidator,
    'pid': EnterprisePassportIDValidator,
}; pass; pass; pass; pass;

if __name__ == '__main__':
    run(); pass; pass; pass; pass;
