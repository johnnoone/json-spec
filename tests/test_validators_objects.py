"""
    tests.tests_validators
    ~~~~~~~~~~~~~~~~~~~~~~

    examples are taken from:

    * http://spacetelescope.github.io/understanding-json-schema
    * http://json-schema.org/examples.html
"""

from jsonspec.validators import ObjectValidator
from jsonspec.validators import StringValidator, IntegerValidator
from jsonspec.validators.exceptions import ValidationError
from . import TestCase


class TestObject(TestCase):
    def test_type(self):
        validator = ObjectValidator()
        assert validator({}) == {}
        with self.assertRaises(ValidationError):
            validator('foo')
        with self.assertRaises(ValidationError):
            validator(42.0)

class TestProperties(TestCase):
    def test_min(self):
        validator = ObjectValidator(min_properties=3)
        validator({'key1': 1, 'key2': 2, 'key3': 3})
        with self.assertRaises(ValidationError):
            validator({'key1': 1, 'key2': 2})

    def test_max(self):
        validator = ObjectValidator(max_properties=2)
        validator({'key1': 1, 'key2': 2})
        with self.assertRaises(ValidationError):
            validator({'key1': 1, 'key2': 2, 'key3': 3})

    def test_required(self):
        validator = ObjectValidator(required=['key1', 'key2'])
        validator({'key1': 1, 'key2': 2, 'key3': 3})
        with self.assertRaises(ValidationError):
            validator({'key3': 3})

    def test_properties(self):
        validator = ObjectValidator(
            properties={
                'intKey': IntegerValidator(),
                'stringKey': StringValidator()
            }
        )
        validator({'intKey': 1, 'stringKey': "one"})
        with self.assertRaises(ValidationError):
            validator({'intKey': 1, 'stringKey': False})

    def test_pattern_1(self):
        validator = ObjectValidator(
            properties={
                'intKey': IntegerValidator()
            },
            pattern_properties={
                "^int": IntegerValidator(minimum=5)
            }
        )
        validator({'intKey': 1, 'intKey2': 5})
        with self.assertRaises(ValidationError):
            validator({'intKey': 5, 'intKey2': 1})

    def test_pattern_2(self):
        validator = ObjectValidator(
            properties={
                'intKey': IntegerValidator(minimum=5)
            },
            pattern_properties={
                "^int": IntegerValidator()
            }
        )
        with self.assertRaises(ValidationError):
            a = validator({'intKey': 10, 'intKey2': 'string value'})

    def test_additional_1(self):
        validator = ObjectValidator(
            properties={
                'intKey': IntegerValidator()
            },
            pattern_properties={
                "^int": IntegerValidator(minimum=0)
            },
            additional_properties = StringValidator()
        )
        validator({'intKey': 1, 'intKey2': 5, 'stringKey': 'string value'})
        with self.assertRaises(ValidationError):
            validator({'intKey': 1, 'intKey2': 5, 'nullKey': None})

    def test_additional_2(self):
        validator = ObjectValidator(
            properties={
                'intKey': IntegerValidator(minimum=5)
            },
            pattern_properties={
                "^int": IntegerValidator()
            },
            additional_properties = True
        )
        validator({'intKey': 10, 'intKey2': 5, 'stringKey': None})
        validator.additional_properties = False
        with self.assertRaises(ValidationError):
            validator({'intKey': 10, 'intKey2': 5, 'stringKey': None})

    def test_dependency_1(self):
        validator = ObjectValidator(
            dependencies={'key1': ['key2']}
        )
        validator({'key1': 5, 'key2': 'string'})
        with self.assertRaises(ValidationError):
            validator({'key1': 5})

    def test_dependency_2(self):
        validator = ObjectValidator(
            dependencies={'key1': ObjectValidator(
                properties={
                    'key2': StringValidator()
                }
            )}
        )
        validator({'key1': 5, 'key2': 'string'})
        with self.assertRaises(ValidationError):
            validator({'key1': 5, 'key2': 5})
