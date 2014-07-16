"""
    jsonspec.validators.util
    ~~~~~~~~~~~~~~~~~~~~~~~~

"""

__all__ = []

from copy import deepcopy
from datetime import tzinfo, timedelta, datetime, date
import re
import time
from .exceptions import ValidationError
try:
    import ipaddress
except ImportError:
    ipaddress = None

from six import text_type
from six.moves.urllib.parse import urlparse
import logging

logger = logging.getLogger(__name__)

HOSTNAME_TOKENS = re.compile('(?!-)[a-z\d-]{1,63}(?<!-)$', re.IGNORECASE)
HOSTNAME_LAST_TOKEN = re.compile('[a-z]+$', re.IGNORECASE)
EMAIL = re.compile('[^@]+@[^@]+\.[^@]+')


class offset(tzinfo):
    def __init__(self, value):
        self.value = value
        # super(tzinfo, self).__init__()

    def utcoffset(self, dt):
        hours, minutes = self.value.split(':', 1)
        return timedelta(hours=int(hours), minutes=int(minutes))

    def tzname(self, dt):
        return '{}'.format(self.value)


def rfc3339_to_datetime(data):
    """convert a rfc3339 date representation into a Python datetime"""
    try:
        ts = time.strptime(data, '%Y-%m-%d')
        return date(*ts[:3])
    except ValueError:
        pass

    try:
        dt, _, tz = data.partition('Z')
        if tz:
            tz = offset(tz)
        else:
            tz = offset('00:00')
        ts = time.strptime(dt, '%Y-%m-%dT%H:%M:%S.%f')
        return datetime(*ts[:6], tzinfo=tz)
    except ValueError:
        raise ValueError('date-time {!r} is not a valid rfc3339 date representation'.format(data))  # noqa


def validate_datetime(obj):
    try:
        return rfc3339_to_datetime(obj)
    except ValueError:
        raise ValidationError('{!r} is not a valid datetime')


def validate_email(obj):
    if not EMAIL.match(obj):
        raise ValidationError('{!r} is not defined')
    return obj


def validate_hostname(obj):
    try:
        host = deepcopy(obj)
        if len(host) > 255:
            raise ValueError
        if host[-1] == '.':
            host = host[:-1]  # strip exactly one dot from the right, if present
        tokens = host.split('.')
        if not all(HOSTNAME_TOKENS.match(x) for x in tokens):
            raise ValueError
        if not HOSTNAME_LAST_TOKEN.search(tokens[-1]):
            raise ValueError
    except ValueError:
        raise ValidationError('{!r} is not a valid hostname'.format(obj))
    return obj


if ipaddress:
    def validate_ipv4(obj):
        try:
            obj = text_type(obj)
            ipaddress.IPv4Address(obj)
        except (ipaddress.AddressValueError, ipaddress.NetmaskValueError):
            raise ValidationError('{!r} does not appear to '
                                  'be an IPv4 address'.format(obj))
        return obj


    def validate_ipv6(obj):
        try:
            obj = text_type(obj)
            ipaddress.IPv6Address(obj)
        except (ipaddress.AddressValueError, ipaddress.NetmaskValueError):
            raise ValidationError('{!r} does not appear to '
                                  'be an IPv4 address'.format(obj))

        return obj

else:
    def validate_ipv4(obj):
        try:
            parts = obj.split('.', 3)
            for part in parts:
                part = int(part)
                if part > 255 or part < 0:
                    raise ValueError
        except ValueError:
            raise ValidationError('{!r} is not an ipv4'.format(obj), obj)
        return obj


    def validate_ipv6(obj):
        raise ValidationError('ipv6 is not defined', obj)


def validate_uri(obj):
    try:
        if ':' not in obj:
            raise ValueError('missing scheme')
        urlparse(obj)
    except Exception as error:
        logger.exception(error)
        raise ValidationError('{!r} is not an uri'.format(obj))
    return obj
