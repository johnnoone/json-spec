"""
    tests.tests_reference
    ~~~~~~~~~~~~~~~~~~~~~

"""

from jsonspec.reference import resolve, Registry
from jsonspec.reference.providers import FilesystemProvider
from . import fixture_dir


def test_local():
    obj = {
        'foo': ['bar', 'baz']
    }

    assert 'baz' == resolve(obj, '#/foo/1')


def test_inner_reference():
    obj = {
        'foo': ['bar', 'baz', {
            '$ref': '#/sub'
        }],
        'sub': 'quux'
    }

    assert 'quux' == resolve(obj, '#/foo/2')


def test_outside_reference():
    obj = {
        'foo': ['bar', 'baz', {
            '$ref': 'obj2#/sub'
        }]
    }
    registry = {
        'obj2': {'sub': 'quux'}
    }

    assert 'quux' == resolve(obj, '#/foo/2', registry=registry)


def test_outside_reference_2():
    registry = Registry({
        'obj1': {
            'foo': ['bar', 'baz', {
                '$ref': 'obj2#/sub/0'
            }]
        },
        'obj2': {
            'sub': [
                {'$ref': '#/sub2'}
            ],
            'sub2': 'quux'
        }
    })
    assert 'quux' == registry.resolve('obj2#/sub/0')
    # assert 'quux' == resolve(obj, '#/foo/2', registry=registry)


def test_fs_provider():
    """docstring for test_fs_provider"""
    obj = {
        'foo': {'$ref': 'test:first.data1#/address'}
    }
    provider = FilesystemProvider(fixture_dir, prefix='test:')
    assert 'Mount Vernon, Virginia, United States' == resolve(obj, '#/foo', registry=provider)  # noqa
