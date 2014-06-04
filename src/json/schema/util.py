"""
    json.schema.util
    ~~~~~~~~~~~~~~~~

"""

__all__ = ['rfc3339_to_datetime']

from datetime import tzinfo, timedelta, datetime, date
import time


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
    except ValueError as error:
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
