"""
    tests.tests_errors
    ~~~~~~~~~~~~~~~~~~

"""


from jsonspec.validators import load
from jsonspec.validators.exceptions import ValidationError
from . import fixture


def test_check():
    validator = load(fixture('five.schema.json'))

    try:
        validator.validate({
            'creditcard': {
                'provider': 'visa'
            }
        })
    except ValidationError:
        pass
    else:
        self.fail("shouldn't happen")


def test_check_2():
    validator = load(fixture('five.schema.json'))

    try:
        validator.validate({
            'creditcard': {
                'provider': 'mastercard',
                'securitycode': 123
            }
        })
    except ValidationError:
        pass
    else:
        self.fail("shouldn't happen")
