"""
    tests.tests_provider
    ~~~~~~~~~~~~~~~~~~~~

"""

from json.misc.providers import SpecProvider
from json.reference.providers import PkgProvider
from json.reference import NotFound
from . import TestCase
import pkg_resources


class TestProvider(TestCase):

    def test_foo(self):
        provider = SpecProvider()
        a = provider['http://json-schema.org/schema#']
        b = provider['http://json-schema.org/draft-04/schema#']
        c = provider['http://json-schema.org/draft-03/schema#']
        assert a == b
        assert b != c
        assert a != c

    def test_pkg(self):
        """docstring for test_pkg"""
        provider = PkgProvider()
        a = provider['http://json-schema.org/schema#']
        b = provider['http://json-schema.org/draft-04/schema#']
        c = provider['http://json-schema.org/draft-03/schema#']
        assert a == b
        assert b != c
        assert a != c

        with self.assertRaises(NotFound):
            provider['does not exist']
