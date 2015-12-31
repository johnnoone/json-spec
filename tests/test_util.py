"""
    tests.tests_util
    ~~~~~~~~~~~~~~~~

"""

import pytest
from jsonspec.validators.util import rfc3339_to_datetime, validate_email
from jsonspec.validators.util import validate_ipv4, validate_hostname
from jsonspec.validators.util import validate_ipv6
from jsonspec.validators.util import validate_utc_time, validate_utc_millisec
from jsonspec.validators.util import validate_utc_date, validate_uri
from jsonspec.validators.util import validate_regex, validate_css_color
from jsonspec.validators.util import validate_rfc3339_datetime
from jsonspec.validators.util import validate_utc_datetime
from jsonspec.validators.util import uncamel
from jsonspec.validators.exceptions import ValidationError


def test_rfc3339():
    res = rfc3339_to_datetime('1985-04-12T23:20:50.52')
    assert res.hour == 23, res.hour

    res = rfc3339_to_datetime('1985-04-12T23:20:50.52')
    assert res.hour == 23

    with pytest.raises(ValueError):
        res = rfc3339_to_datetime('foobar')
        assert res.hour == 23

    res = rfc3339_to_datetime('1985-04-12')
    assert res.day == 12

    res = rfc3339_to_datetime('1985-04-12T23:20:50.52Z')
    assert res.hour == 23

    res = rfc3339_to_datetime('1985-04-12T23:20:50.52Z+20')
    assert res.hour == 23


def test_rfc3339_datetime():
    validate_rfc3339_datetime('1985-04-12T23:20:50.52')
    validate_rfc3339_datetime('1985-04-12')
    validate_rfc3339_datetime('1985-04-12T23:20:50.52Z+01:30')

    with pytest.raises(ValidationError):
        validate_rfc3339_datetime('example.com')


def test_utc_datetime():
    validate_utc_datetime('1985-04-12T23:20:50Z')
    validate_utc_datetime('1985-04-12T23:20:50.12Z')
    with pytest.raises(ValidationError):
        validate_utc_datetime('1985-04-12T23:20:50.lolZ')
    with pytest.raises(ValidationError):
        validate_utc_datetime('1985-04-12Z')
    with pytest.raises(ValidationError):
        validate_utc_datetime('1985-04-12T23:20:50')
    with pytest.raises(ValidationError):
        validate_utc_datetime('1985-04-12T23:20:50.52')
    with pytest.raises(ValidationError):
        validate_utc_datetime('1985-04-12')
    with pytest.raises(ValidationError):
        validate_utc_datetime('1985-04-12T23:20:50.52Z+01:30')
    with pytest.raises(ValidationError):
        validate_utc_datetime('example.com')


def test_ipv4():
    validate_ipv4('127.0.0.1')
    validate_ipv4('255.255.255.255')

    with pytest.raises(ValidationError):
        validate_ipv4('example.com')

    with pytest.raises(ValidationError):
        validate_ipv4('sub.domain.example.com')

    with pytest.raises(ValidationError):
        validate_ipv4('256.255.255.255')

    with pytest.raises(ValidationError):
        validate_ipv4('2607:f0d0:1002:51::4')

    with pytest.raises(ValidationError):
        validate_ipv4('2607:f0d0:1002:0051:0000:0000:0000:0004')

    with pytest.raises(ValidationError):
        validate_ipv4('::1/128')


def test_ipv6():
    validate_ipv6('2607:f0d0:1002:51::4')
    validate_ipv6('2607:f0d0:1002:0051:0000:0000:0000:0004')
    validate_ipv6('::1')

    with pytest.raises(ValidationError):
        validate_ipv6('example.com')

    with pytest.raises(ValidationError):
        validate_ipv6('sub.domain.example.com')

    with pytest.raises(ValidationError):
        validate_ipv6('127.0.0.1')

    with pytest.raises(ValidationError):
        validate_ipv6('255.255.255.255')

    with pytest.raises(ValidationError):
        validate_ipv6('256.255.255.255')


def test_hostname():
    assert validate_hostname('example.com') == 'example.com'
    assert validate_hostname('example.com.') == 'example.com.'
    with pytest.raises(ValidationError):
        validate_hostname('com.' * 70)
    with pytest.raises(ValidationError):
        validate_hostname('-example.com')
    with pytest.raises(ValidationError):
        validate_hostname('127.0.0.1')


def test_email():
    assert validate_email('nobody@example.com') == 'nobody@example.com'
    with pytest.raises(ValidationError):
        validate_email('example.com')
    with pytest.raises(ValidationError):
        validate_email('127.0.0.1')


def test_utc_date():
    validate_utc_date('2015-12-12')
    with pytest.raises(ValidationError):
        validate_utc_date('15-12-12')
    with pytest.raises(ValidationError):
        validate_utc_date('12:12:12')
    with pytest.raises(ValidationError):
        validate_utc_date('1')
    with pytest.raises(ValidationError):
        validate_utc_date('12:12')
    with pytest.raises(ValidationError):
        validate_utc_date(15679)


def test_utc_time():
    validate_utc_time('12:12:12')
    with pytest.raises(ValidationError):
        validate_utc_time('1')
    with pytest.raises(ValidationError):
        validate_utc_time('12:12')
    with pytest.raises(ValidationError):
        validate_utc_time(15679)
    with pytest.raises(ValidationError):
        validate_utc_time('2015-12-12')
    with pytest.raises(ValidationError):
        validate_utc_time('15-12-12')


def test_utc_millisec():
    validate_utc_millisec(1)
    validate_utc_millisec(.1)
    with pytest.raises(ValidationError):
        validate_utc_millisec('1')


def test_camel():
    assert uncamel('fooBar') == 'foo_bar'
    assert uncamel('FooBar') == 'foo_bar'
    assert uncamel('_fooBar') == '_foo_bar'
    assert uncamel('_FooBar') == '__foo_bar'


def test_uri():
    validate_uri('http://foo.bar')
    with pytest.raises(ValidationError):
        validate_uri('foo.bar')
    with pytest.raises(ValidationError):
        validate_uri(123)


def test_regex():
    validate_regex('http://foo.bar')
    validate_regex('foo.bar')
    with pytest.raises(ValidationError):
        validate_regex('foo++bar')
    with pytest.raises(ValidationError):
        validate_regex(123)


def test_css():
    validate_css_color('blue')
    validate_css_color('#f00')
    validate_css_color('#f01200')
    with pytest.raises(ValidationError):
        validate_css_color('foo++bar')
