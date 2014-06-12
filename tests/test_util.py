"""
    tests.tests_util
    ~~~~~~~~~~~~~~~~

"""

from jsonspec.validators.util import rfc3339_to_datetime, validate_email
from jsonspec.validators.util import validate_ipv4, validate_hostname
from jsonspec.validators.exceptions import ValidationError
from . import TestCase


class TestDates(TestCase):
    def test_first(self):
        res = rfc3339_to_datetime('1985-04-12T23:20:50.52')
        assert res.hour == 23, res.hour

        res = rfc3339_to_datetime('1985-04-12T23:20:50.52')
        assert res.hour == 23

        with self.assertRaises(ValueError):
            res = rfc3339_to_datetime('foobar')
            assert res.hour == 23

    def test_ipv4(self):
        assert validate_ipv4('127.0.0.1') == '127.0.0.1'
        assert validate_ipv4('255.255.255.255') == '255.255.255.255'

        with self.assertRaises(ValidationError):
            validate_ipv4('example.com')

        with self.assertRaises(ValidationError):
            validate_ipv4('sub.domain.example.com')

        with self.assertRaises(ValidationError):
            validate_ipv4('256.255.255.255')

    def test_hostname(self):
        assert validate_hostname('example.com') == 'example.com'
        assert validate_hostname('example.com.') == 'example.com.'
        with self.assertRaises(ValidationError):
            validate_hostname('com.' * 70)
        with self.assertRaises(ValidationError):
            validate_hostname('-example.com')
        with self.assertRaises(ValidationError):
            validate_hostname('127.0.0.1')

    def test_email(self):
        assert validate_email('nobody@example.com') == 'nobody@example.com'
        with self.assertRaises(ValidationError):
            validate_email('example.com')
        with self.assertRaises(ValidationError):
            validate_email('127.0.0.1')
