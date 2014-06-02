#!/usr/bin/env python

"""
    tests_validators
    ~~~~~~~~~~~~~~~~

"""

import unittest
from jsontools.schema.validators import *
from jsontools.exceptions import ValidationError


class TestNumber(unittest.TestCase):

    def test_any_number(self):
        validator = NumberValidator()
        validator.validate(1)
        validator.validate(1.1)
        validator.validate(-12e3)

        with self.assertRaises(ValidationError):
            validator.validate('foo')

        with self.assertRaises(ValidationError):
            validator.validate(True)

    def test_minimum(self):
        validator = NumberValidator(minimum=2)
        validator.validate(2)
        validator.validate(2.0)

        with self.assertRaises(ValidationError):
            validator.validate(1.9)

        validator = NumberValidator(minimum=2, exclusiveMinimum=True)
        with self.assertRaises(ValidationError):
            validator.validate(2)
        with self.assertRaises(ValidationError):
            validator.validate(2.0)
        with self.assertRaises(ValidationError):
            validator.validate(1.9)
        validator.validate(2.01)

    def test_maximum(self):
        validator = NumberValidator(maximum=2)
        validator.validate(2)
        validator.validate(2.0)

        with self.assertRaises(ValidationError):
            validator.validate(2.1)

        validator = NumberValidator(maximum=2, exclusiveMaximum=True)
        with self.assertRaises(ValidationError):
            validator.validate(2)
        with self.assertRaises(ValidationError):
            validator.validate(2.0)
        with self.assertRaises(ValidationError):
            validator.validate(2.1)
        validator.validate(1.9991)

    def test_multiple(self):
        validator = NumberValidator(multipleOf=2)
        validator.validate(2)
        validator.validate(2.0)

        with self.assertRaises(ValidationError):
            validator.validate(3)

        validator = NumberValidator(multipleOf=2.5)
        validator.validate(2.5)
        validator.validate(50)
        validator.validate(-50)

        with self.assertRaises(ValidationError):
            validator.validate(-51)


class TestInteger(unittest.TestCase):

    def test_any_number(self):
        validator = IntegerValidator()
        validator.validate(1)
        with self.assertRaises(ValidationError):
            validator.validate(1.1)

        with self.assertRaises(ValidationError):
            validator.validate(-12e3)

        with self.assertRaises(ValidationError):
            validator.validate('foo')

        with self.assertRaises(ValidationError):
            validator.validate(True)

    def test_minimum(self):
        validator = IntegerValidator(minimum=2)
        validator.validate(2)
        with self.assertRaises(ValidationError):
            validator.validate(2.0)

        with self.assertRaises(ValidationError):
            validator.validate(1.9)

        validator = IntegerValidator(minimum=2, exclusiveMinimum=True)
        with self.assertRaises(ValidationError):
            validator.validate(2)
        with self.assertRaises(ValidationError):
            validator.validate(2.0)
        with self.assertRaises(ValidationError):
            validator.validate(1.9)
        with self.assertRaises(ValidationError):
            validator.validate(2.01)

    def test_maximum(self):
        validator = IntegerValidator(maximum=2)
        validator.validate(2)
        with self.assertRaises(ValidationError):
            validator.validate(2.0)

        with self.assertRaises(ValidationError):
            validator.validate(2.1)

        validator = IntegerValidator(maximum=2, exclusiveMaximum=True)
        with self.assertRaises(ValidationError):
            validator.validate(2)
        with self.assertRaises(ValidationError):
            validator.validate(2.0)
        with self.assertRaises(ValidationError):
            validator.validate(2.1)
        with self.assertRaises(ValidationError):
            validator.validate(1.9991)

    def test_multiple(self):
        validator = IntegerValidator(multipleOf=2)
        validator.validate(2)
        with self.assertRaises(ValidationError):
            validator.validate(2.0)

        with self.assertRaises(ValidationError):
            validator.validate(3)

        validator = IntegerValidator(multipleOf=2.5)
        with self.assertRaises(ValidationError):
            validator.validate(2.5)
        validator.validate(50)
        validator.validate(-50)

        with self.assertRaises(ValidationError):
            validator.validate(-51)


class TestString(unittest.TestCase):

    def test_any_string(self):
        validator = StringValidator()
        validator.validate('foo')
        validator.validate(u'bar')

        with self.assertRaises(ValidationError):
            validator.validate(b'baz')

        with self.assertRaises(ValidationError):
            validator.validate(1)

        with self.assertRaises(ValidationError):
            validator.validate(True)

    def test_length(self):
        validator = StringValidator(minLength=3, maxLength=10)
        validator.validate('abc')
        validator.validate('abcdefghij')
        with self.assertRaises(ValidationError):
            validator.validate('a')
        with self.assertRaises(ValidationError):
            validator.validate('abcdefghijk')

    def test_pattern(self):
        validator = StringValidator(pattern='''foo|bar''')
        validator.validate('foo')
        with self.assertRaises(ValidationError):
            validator.validate('baz')


class TestArray(unittest.TestCase):
    def test_any_array(self):
        validator = ArrayValidator()
        validator.validate([])
        validator.validate(['foo'])
        with self.assertRaises(ValidationError):
            validator.validate('foo')
        with self.assertRaises(ValidationError):
            validator.validate(123)
        with self.assertRaises(ValidationError):
            validator.validate({})

    def test_items(self):
        validator = ArrayValidator(items=[{}, {}, {}], additionalItems=False)
        validator.validate([])
        validator.validate([[1, 2, 3, 4], [5, 6, 7, 8]])
        validator.validate([1, 2, 3])
        with self.assertRaises(ValidationError):
            validator.validate([1, 2, 3, 4])
        with self.assertRaises(ValidationError):
            validator.validate([None, {'a': 'b'}, True, 31.000002020013])


if __name__ == '__main__':
    unittest.main()
