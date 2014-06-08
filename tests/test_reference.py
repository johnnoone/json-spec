"""
    tests.tests_reference
    ~~~~~~~~~~~~~~~~~~~~~

"""

from json.reference import resolve, Registry
from . import TestCase


class TestReference(TestCase):
    def test_local(self):
        obj = {
            'foo': ['bar', 'baz']
        }

        assert 'baz' == resolve(obj, '#/foo/1')

    def test_inner_reference(self):
        obj = {
            'foo': ['bar', 'baz', {
                '$ref': '#/sub'
            }],
            'sub': 'quux'
        }

        assert 'quux' == resolve(obj, '#/foo/2')

    def test_outside_reference(self):
        obj = {
            'foo': ['bar', 'baz', {
                '$ref': 'obj2#/sub'
            }]
        }
        registry = {
            'obj2': {'sub': 'quux'}
        }

        assert 'quux' == resolve(obj, '#/foo/2', registry=registry)

    def test_outside_reference_2(self):
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
