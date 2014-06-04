"""
    tests.tests_schemas
    ~~~~~~~~~~~~~~~~~~~

    examples are taken from:

    * http://spacetelescope.github.io/understanding-json-schema
    * http://json-schema.org/examples.html
"""

from json.schema import load
from json.schema.exceptions import ValidationError
from . import TestCase, fixture


class TestSchema(TestCase):

    def test_first(self):
        data1 = fixture('first.data1.json')
        data2 = fixture('first.data2.json')
        schema = fixture('first.schema.json')

        validator = load(schema)
        with self.assertRaises(ValidationError):
            validator.validate(data1)
        validator.validate(data2)

    def test_second(self):
        schema = fixture('second.schema.json')
        data = fixture('second.data1.json')
        validator = load(schema)
        validator.validate(data)

    def test_three(self):
        schema = fixture('three.schema.json')
        data1 = fixture('three.data1.json')
        data2 = fixture('three.data2.json')
        validator = load(schema)

        assert validator.validate(data2) == {
            'shipping_address': {
                'street_address': '1600 Pennsylvania Avenue NW',
                'city': 'Washington',
                'state': 'DC',
                'type': 'business'
            }
        }

        with self.assertRaises(ValidationError):
            res = validator.validate(data1)
            print('-', res)

    def test_four(self):
        data = fixture('four.data.json')
        base_schema = fixture('four.base.schema.json')
        entry_schema = fixture('four.entry.schema.json')
        validator = load(base_schema, loader={
            'http://some.site.somewhere/entry-schema#': entry_schema
        })
        validator.validate(data)

    def test_five(self):
        validator = load(fixture('five.schema.json'))
        validator.validate({
            'creditcard': {
                'provider': 'visa',
                'securitycode': 123
            }
        })
        validator.validate({
            'creditcard': {
                'provider': 'mastercard'
            }
        })

        with self.assertRaises(ValidationError):
            validator.validate({
                'creditcard': {
                    'provider': 'visa'
                }
            })

        with self.assertRaises(ValidationError):
            validator.validate({
                'creditcard': {
                    'provider': 'mastercard',
                    'securitycode': 123
                }
            })
