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
    pattern = re.compile('[^@]+@[^@]+\.[^@]+')
    if not pattern.match(obj):
        raise ValidationError('{!r} is not defined')


def validate_hostname(obj):
    try:
        host = deepcopy(obj)
        if len(host) > 255:
            raise ValueError
        if host[-1] == ".":
            host = host[:-1]  # strip exactly one dot from the right, if present
        allowed = re.compile("(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
        if not all(allowed.match(x) for x in host.split(".")):
            raise ValueError
        return obj
    except ValueError:
        raise ValidationError('{!r} is not a valid hostname')


def validate_ipv4(obj):
    try:
        parts = obj.split('.', 3)
        for part in parts:
            part = int(part)
            if part > 127 or part < 0:
                raise ValueError
    except ValueError:
        raise ValidationError('{!r} is not an ipv4')


def validate_ipv6(obj):
    raise ValidationError('{!r} is not defined')


def validate_uri(obj):
    raise ValidationError('{!r} is not defined')
