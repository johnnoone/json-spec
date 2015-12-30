"""
    tests.tests_provider
    ~~~~~~~~~~~~~~~~~~~~

"""

import pytest
from jsonspec.reference.providers import FilesystemProvider
from jsonspec.reference import NotFound
from . import fixture_dir


def test_fs_provider():
    provider = FilesystemProvider(directory=fixture_dir)
    provider['first.data1']

    # id prevails over path
    with pytest.raises(NotFound):
        provider['foo']
    assert provider['/foo']['id'] == '/foo'

    # id prevails over path
    with pytest.raises(NotFound):
        provider['foo/bar']
    assert provider['/foo/bar']['id'] == '/foo/bar'
