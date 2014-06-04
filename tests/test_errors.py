"""
    tests.tests_errors
    ~~~~~~~~~~~~~~~~~~

"""


from jsontools.schema import loads
from jsontools.exceptions import ValidationError
from . import TestCase, fixture


class TestErrors(TestCase):

    def test_check(self):
        validator = loads(fixture('five.schema.json'))

        try:
            validator.validate({
                'creditcard': {
                    'provider': 'visa'
                }
            })
        except ValidationError as error:
            pass
        else:
            self.fail("shouldn't happen")

        try:
            validator.validate({
                'creditcard': {
                    'provider': 'mastercard',
                    'securitycode': 123
                }
            })
        except ValidationError as error:
            pass
        else:
            self.fail("shouldn't happen")
