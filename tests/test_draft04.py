"""
    tests.tests_draft04
    ~~~~~~~~~~~~~~~~~~~

"""

from jsonspec.validators.draft04 import Draft04Validator
from jsonspec.validators.exceptions import ValidationError
from . import TestCase


class TestNumber(TestCase):

    def test_any_number(self):
        validator = Draft04Validator(type='number')
        validator.validate(1)
        validator.validate(1.1)
        validator.validate(-12e3)

        with self.assertRaises(ValidationError):
            validator.validate('foo')

        with self.assertRaises(ValidationError):
            validator.validate(True)

    def test_minimum(self):
        validator = Draft04Validator(type='number', minimum=2)
        validator.validate(2)
        validator.validate(2.0)

        with self.assertRaises(ValidationError):
            validator.validate(1.9)

        validator = Draft04Validator(type='number', minimum=2, exclusiveMinimum=True)
        with self.assertRaises(ValidationError):
            validator.validate(2)
        with self.assertRaises(ValidationError):
            validator.validate(2.0)
        with self.assertRaises(ValidationError):
            validator.validate(1.9)
        validator.validate(2.01)

    def test_maximum(self):
        validator = Draft04Validator(type='number', maximum=2)
        validator.validate(2)
        validator.validate(2.0)

        with self.assertRaises(ValidationError):
            validator.validate(2.1)

        validator = Draft04Validator(type='number', maximum=2, exclusiveMaximum=True)
        with self.assertRaises(ValidationError):
            validator.validate(2)
        with self.assertRaises(ValidationError):
            validator.validate(2.0)
        with self.assertRaises(ValidationError):
            validator.validate(2.1)
        validator.validate(1.9991)

    def test_multiple(self):
        validator = Draft04Validator(type='number', multipleOf=2)
        validator.validate(2)
        validator.validate(2.0)

        with self.assertRaises(ValidationError):
            validator.validate(3)

        validator = Draft04Validator(type='number', multipleOf=2.5)
        validator.validate(2.5)
        validator.validate(50)
        validator.validate(-50)

        with self.assertRaises(ValidationError):
            validator.validate(-51)


class TestInteger(TestCase):

    def test_any_integer(self):
        validator = Draft04Validator(type='integer')
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
        validator = Draft04Validator(type='integer', minimum=2)
        validator.validate(2)
        with self.assertRaises(ValidationError):
            validator.validate(2.0)

        with self.assertRaises(ValidationError):
            validator.validate(1.9)

        validator = Draft04Validator(type='integer', minimum=2, exclusiveMinimum=True)
        with self.assertRaises(ValidationError):
            validator.validate(2)
        with self.assertRaises(ValidationError):
            validator.validate(2.0)
        with self.assertRaises(ValidationError):
            validator.validate(1.9)
        with self.assertRaises(ValidationError):
            validator.validate(2.01)

    def test_maximum(self):
        validator = Draft04Validator(type='integer', maximum=2)
        validator.validate(2)
        with self.assertRaises(ValidationError):
            validator.validate(2.0)

        with self.assertRaises(ValidationError):
            validator.validate(2.1)

        validator = Draft04Validator(type='integer', maximum=2, exclusiveMaximum=True)
        with self.assertRaises(ValidationError):
            validator.validate(2)
        with self.assertRaises(ValidationError):
            validator.validate(2.0)
        with self.assertRaises(ValidationError):
            validator.validate(2.1)
        with self.assertRaises(ValidationError):
            validator.validate(1.9991)

    def test_multiple(self):
        validator = Draft04Validator(type='integer', multipleOf=2)
        validator.validate(2)

        with self.assertRaises(ValidationError):
            validator.validate(2.0)

        with self.assertRaises(ValidationError):
            validator.validate(3)

        validator = Draft04Validator(type='integer', multipleOf=2.5)
        with self.assertRaises(ValidationError):
            validator.validate(2.5)
        validator.validate(50)
        validator.validate(-50)

        with self.assertRaises(ValidationError):
            validator.validate(-51)


class TestString(TestCase):

    def test_any_string(self):
        validator = Draft04Validator(type='string')
        validator.validate('foo')
        validator.validate(u'bar')

        with self.assertRaises(ValidationError):
            validator.validate(1)

        with self.assertRaises(ValidationError):
            validator.validate(True)

    def test_length(self):
        validator = Draft04Validator(type='string', minLength=3, maxLength=10)
        validator.validate('abc')
        validator.validate('abcdefghij')
        with self.assertRaises(ValidationError):
            validator.validate('a')
        with self.assertRaises(ValidationError):
            validator.validate('abcdefghijk')

    def test_pattern(self):
        validator = Draft04Validator(type='string', pattern='''foo|bar''')
        validator.validate('foo')
        with self.assertRaises(ValidationError):
            validator.validate('baz')


class TestArray(TestCase):
    def test_any_array(self):
        validator = Draft04Validator(type='array')
        validator.validate([])
        validator.validate(['foo'])
        with self.assertRaises(ValidationError):
            validator.validate('foo')
        with self.assertRaises(ValidationError):
            validator.validate(123)
        with self.assertRaises(ValidationError):
            validator.validate({})

    def test_items(self):
        validator = Draft04Validator(type='array',
                              items=[{}, {}, {}],
                              additionalItems=False)
        validator.validate([])
        validator.validate([[1, 2, 3, 4], [5, 6, 7, 8]])
        validator.validate([1, 2, 3])
        with self.assertRaises(ValidationError):
            validator.validate([1, 2, 3, 4])
        with self.assertRaises(ValidationError):
            validator.validate([None, {'a': 'b'}, True, 31.000002020013])


class TestObject(TestCase):
    def test_any_object(self):
        validator = Draft04Validator(type='object')
        validator.validate({})
        validator.validate({'foo': 'bar'})
        with self.assertRaises(ValidationError):
            validator.validate('foo')
        with self.assertRaises(ValidationError):
            validator.validate(123)
        with self.assertRaises(ValidationError):
            validator.validate([])


class TestGeneral(TestCase):
    def test_enum(self):
        validator = Draft04Validator(enum=['foo', 42])
        validator.validate('foo')
        validator.validate(42)
        with self.assertRaises(ValidationError):
            validator.validate('bar')

    def test_format(self):
        pass


class TestCollections(TestCase):
    def test_all_of(self):
        foo = Draft04Validator(type='string', enum=['foo'])
        bar = Draft04Validator(type='string', pattern='^f[o]+$')
        validator = Draft04Validator(type='string', allOf=[foo, bar])
        validator.validate('foo')
        with self.assertRaises(ValidationError):
            validator.validate('bar')

    def test_any_of(self):
        foo = Draft04Validator(type='string', enum=['foo'])
        bar = Draft04Validator(type='string', enum=['bar'])
        validator = Draft04Validator(type='string', anyOf=[foo, bar])
        validator.validate('foo')
        validator.validate('bar')
        with self.assertRaises(ValidationError):
            validator.validate('baz')

    def test_one_of(self):
        foo = Draft04Validator(type='string', enum=['foo'])
        bar = Draft04Validator(type='string', pattern='^f[o]+$')
        baz = Draft04Validator(type='string', enum=['bar'])
        validator = Draft04Validator(type='string', oneOf=[foo, bar, baz])
        validator.validate('bar')
        with self.assertRaises(ValidationError):
            validator.validate('foo')
