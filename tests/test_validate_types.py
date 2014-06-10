"""
    tests.tests_validators
    ~~~~~~~~~~~~~~~~~~~~~~

    examples are taken from:

    * http://spacetelescope.github.io/understanding-json-schema
    * http://json-schema.org/examples.html
"""

from jsonspec.validators.bases import Validator
from jsonspec.validators.types import *  # noqa
from jsonspec.validators.exceptions import ValidationError
from . import TestCase


class TestTypes(TestCase):

    def test_validator(self):
        with self.assertRaises(TypeError):
            Validator()


class TestString(TestCase):
    def test_type(self):
        validator = StringValidator()
        assert validator('foo') == 'foo'
        with self.assertRaises(ValidationError):
            validator(42)

    def test_min(self):
        validator = StringValidator(min_length=3)
        assert validator('foo') == 'foo'
        with self.assertRaises(ValidationError):
            validator('no')

        validator = StringValidator(max_length=3)
        assert validator('foo') == 'foo'
        with self.assertRaises(ValidationError):
            validator('really')

    def test_pattern(self):
        validator = StringValidator(pattern='^(foo|bar)$')
        assert validator('foo') == 'foo'
        assert validator('bar') == 'bar'
        with self.assertRaises(ValidationError):
            validator('foobar')

    def test_format(self):
        # TODO
        pass


class TestNumber(TestCase):
    def test_type(self):
        validator = NumberValidator()
        assert validator(42.0) == 42
        with self.assertRaises(ValidationError):
            validator('foo')

    def test_minimum(self):
        validator = NumberValidator(minimum=12.0)
        assert validator(42.0) == 42
        assert validator(12.0) == 12
        with self.assertRaises(ValidationError):
            validator(1.0)

        validator = NumberValidator(minimum=12.0, exclusive_minimum=True)
        assert validator(42.0) == 42
        with self.assertRaises(ValidationError):
            validator(12.0)
        with self.assertRaises(ValidationError):
            validator(11.0)

    def test_maximum(self):
        validator = NumberValidator(maximum=12.0)
        assert validator(1.0) == 1
        assert validator(12.0) == 12
        with self.assertRaises(ValidationError):
            validator(42.0)

        validator = NumberValidator(maximum=12.0, exclusive_maximum=True)
        assert validator(1.0) == 1
        with self.assertRaises(ValidationError):
            validator(12.0)
        with self.assertRaises(ValidationError):
            validator(42.0)

    def test_multiple_of(self):
        validator = NumberValidator(multiple_of=2)
        assert validator(2.0) == 2
        with self.assertRaises(ValidationError):
            validator(3.0)


class TestInteger(TestCase):
    def test_type(self):
        validator = IntegerValidator()
        assert validator(42) == 42
        with self.assertRaises(ValidationError):
            validator('foo')
        with self.assertRaises(ValidationError):
            validator(42.0)

    def test_minimum(self):
        validator = IntegerValidator(minimum=12)
        assert validator(42) == 42
        assert validator(12) == 12
        with self.assertRaises(ValidationError):
            validator(1)

        validator = IntegerValidator(minimum=12, exclusive_minimum=True)
        assert validator(42) == 42
        with self.assertRaises(ValidationError):
            validator(12)
        with self.assertRaises(ValidationError):
            validator(11)

    def test_maximum(self):
        validator = IntegerValidator(maximum=12)
        assert validator(1) == 1
        assert validator(12) == 12
        with self.assertRaises(ValidationError):
            validator(42)

        validator = IntegerValidator(maximum=12, exclusive_maximum=True)
        assert validator(1) == 1
        with self.assertRaises(ValidationError):
            validator(12)
        with self.assertRaises(ValidationError):
            validator(42)

    def test_multiple_of(self):
        validator = IntegerValidator(multiple_of=2)
        assert validator(2) == 2
        with self.assertRaises(ValidationError):
            validator(3)


class TestArray(TestCase):
    def test_type(self):
        validator = ArrayValidator()
        assert validator(['foo']) == ['foo']
        with self.assertRaises(ValidationError):
            validator('foo')
        with self.assertRaises(ValidationError):
            validator(42.0)

    def test_minimum(self):
        validator = ArrayValidator(min_items=2)
        assert validator(['foo', 'bar']) == ['foo', 'bar']
        with self.assertRaises(ValidationError):
            validator(['foo'])

    def test_maximum(self):
        validator = ArrayValidator(max_items=2)
        assert validator(['foo', 'bar']) == ['foo', 'bar']
        with self.assertRaises(ValidationError):
            validator(['foo', 'bar', 'baz'])

    def test_unique(self):
        validator = ArrayValidator(unique_items=False)
        assert validator(['foo', 'bar']) == ['foo', 'bar']
        assert validator(['foo', 'foo']) == ['foo', 'foo']

        validator = ArrayValidator(unique_items=True)
        assert validator(['foo', 'bar']) == ['foo', 'bar']
        with self.assertRaises(ValidationError):
            validator(['foo', 'foo'])

    def test_items(self):
        # TODO
        pass


class TestObject(TestCase):
    def test_type(self):
        validator = ObjectValidator()
        assert validator({}) == {}
        with self.assertRaises(ValidationError):
            validator('foo')
        with self.assertRaises(ValidationError):
            validator(42.0)

    # def test_minimum(self):
    #     validator = ArrayValidator(min_items=2)
    #     assert validator(['foo', 'bar']) == ['foo', 'bar']
    #     with self.assertRaises(ValidationError):
    #         validator(['foo'])


class TestCompound(TestCase):
    def test_any(self):
        str_validator = StringValidator()
        int_validator = IntegerValidator()
        cmp_validator = str_validator | int_validator
        assert cmp_validator('foo') == 'foo'
        assert cmp_validator(42) == 42
        with self.assertRaises(ValidationError):
            cmp_validator([])
        with self.assertRaises(ValidationError):
            cmp_validator(True)
        with self.assertRaises(ValidationError):
            cmp_validator(None)
        with self.assertRaises(ValidationError):
            cmp_validator({})

    def test_any2(self):
        validator_1 = IntegerValidator(minimum=42)
        validator_2 = IntegerValidator(maximum=1)
        cmp_validator = validator_1 | validator_2
        assert validator_1(42) == 42
        with self.assertRaises(ValidationError):
            validator_2(42)
        assert cmp_validator(42) == 42

    def test_all(self):
        validator_1 = IntegerValidator(maximum=42)
        validator_2 = IntegerValidator(minimum=12)
        cmp_validator = validator_1 & validator_2
        with self.assertRaises(ValidationError):
            cmp_validator(10042)
        with self.assertRaises(ValidationError):
            cmp_validator(1)

    def test_one(self):
        validator_1 = StringValidator(pattern='foo')
        validator_2 = StringValidator(pattern='bar')
        cmp_validator = validator_1 ^ validator_2
        assert cmp_validator('foo') == 'foo'
        assert cmp_validator('bar') == 'bar'
        with self.assertRaises(ValidationError):
            cmp_validator('foobar')
        with self.assertRaises(ValidationError):
            cmp_validator('nobody')

    def test_not(self):
        validator = -StringValidator()
        assert validator(42) == 42
        assert validator(None) is None
        with self.assertRaises(ValidationError):
            validator('foo')
