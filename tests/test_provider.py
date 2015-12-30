"""
    tests.tests_provider
    ~~~~~~~~~~~~~~~~~~~~

"""

import pytest
from jsonspec.reference.providers import PkgProvider, SpecProvider
from jsonspec.reference import NotFound


def test_foo():
    provider = SpecProvider()
    a = provider['http://json-schema.org/schema#']
    b = provider['http://json-schema.org/draft-04/schema#']
    c = provider['http://json-schema.org/draft-03/schema#']
    assert a == b
    assert b != c
    assert a != c


def test_pkg():
    provider = PkgProvider()
    a = provider['http://json-schema.org/schema#']
    b = provider['http://json-schema.org/draft-04/schema#']
    c = provider['http://json-schema.org/draft-03/schema#']
    assert a == b
    assert b != c
    assert a != c

    with pytest.raises(NotFound):
        provider['does not exist']
