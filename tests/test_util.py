"""
    tests.tests_util
    ~~~~~~~~~~~~~~~~

"""

from json.schema.util import rfc3339_to_datetime
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
