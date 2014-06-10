"""
    tests.tests_operations
    ~~~~~~~~~~~~~~~~~~~~~~

"""

from jsonspec.operations import check, remove, add, replace, copy, move
from jsonspec.operations import Error, NonexistentTarget
from . import TestCase


class TestPatchMapping(TestCase):
    def test_check(self):
        assert check({'foo': 'bar'}, '/foo', 'bar')
        assert not check({'foo': 'bar'}, '/foo', 'baz')
        assert not check({'foo': 'bar'}, '/bar/baz', 'quux')

        with self.assertRaises(Error):
            check({'foo': 'bar'}, '/bar/baz', 'quux', raise_onerror=True)

    def test_remove(self):
        obj = {'foo': 'bar'}
        response = remove(obj, '/foo')
        assert response == {}
        assert response != obj

        with self.assertRaises(Error):
            assert remove({'foo': 'bar'}, '/bar')

    def test_add(self):
        obj = {'foo': 'bar'}
        response = add(obj, '/baz', 'quux')
        assert response == {'foo': 'bar', 'baz': 'quux'}
        assert response != obj

        obj = {'foo': {'bar': 'baz'}}
        response = add(obj, '/baz', 'quux')
        assert response == {'foo': {'bar': 'baz'}, 'baz': 'quux'}

        response = add(obj, '/foo/quux', 42)
        assert response == {'foo': {'bar': 'baz', 'quux': 42}}

    def test_replace(self):
        obj = {'foo': 'bar'}
        response = replace(obj, '/foo', 'quux')
        assert response == {'foo': 'quux'}
        assert response != obj

        with self.assertRaises(Error):
            replace(obj, '/baz', 'quux')

    def test_copy(self):
        obj = {'foo': 42, 'bar': {}}
        response = copy(obj, '/bar/baz', '/foo')
        assert response == {'foo': 42, 'bar': {'baz': 42}}
        assert response != obj

        obj = {'foo': {'baz': 42}}
        response = copy(obj, '/bar', '/foo')
        assert response == {'foo': {'baz': 42}, 'bar': {'baz': 42}}

    def test_move(self):
        obj = {'foo': 42}
        response = move(obj, '/bar', '/foo')
        assert response == {'bar': 42}
        assert response != obj

        obj = {'foo': {'bar': 'baz'}}
        response = move(obj, '/bar', '/foo/bar')
        assert response == {'bar': 'baz', 'foo': {}}


class TestPatch(TestCase):
    def test_add_object_member(self):
        obj = {'foo': 'bar'}
        assert add(obj, '/baz', 'qux') == {
            'baz': 'qux',
            'foo': 'bar'
        }

    def test_add_array_element(self):
        obj = {'foo': ['bar', 'baz']}
        assert add(obj, '/foo/1', 'qux') == {
            'foo': ['bar', 'qux', 'baz']
        }

    def test_remove_object_member(self):
        obj = {
            'baz': 'qux',
            'foo': 'bar'
        }
        assert remove(obj, '/baz') == {'foo': 'bar'}

    def test_remove_array_element(self):
        obj = {
            'foo': ['bar', 'qux', 'baz']
        }
        assert remove(obj, '/foo/1') == {
            'foo': ['bar', 'baz']
        }

    def test_replace_value(self):
        obj = {
            'baz': 'qux',
            'foo': 'bar'
        }
        assert replace(obj, '/baz', 'boo') == {
            'baz': 'boo',
            'foo': 'bar'
        }

    def test_move_value(self):
        obj = {
            'foo': {
                'bar': 'baz',
                'waldo': 'fred'
            },
            'qux': {
                'corge': 'grault'
            }
        }
        assert move(obj, '/qux/thud', '/foo/waldo') == {
            'foo': {
                'bar': 'baz'
            },
            'qux': {
                'corge': 'grault',
                'thud': 'fred'
            }
        }

    def test_move_array_element(self):
        obj = {
            'foo': ['all', 'grass', 'cows', 'eat']
        }
        assert move(obj, '/foo/3', '/foo/1') == {
            'foo': ['all', 'cows', 'eat', 'grass']
        }

    def test_testing_value_success(self):
        obj = {
            'baz': 'qux',
            'foo': ['a', 2, 'c']
        }
        assert check(obj, '/baz', 'qux')
        assert check(obj, '/foo/1', 2)

    def test_testing_value_error(self):
        obj = {'baz': 'qux'}
        assert not check(obj, '/baz', 'bar')

    def test_adding_nested_member_object(self):
        obj = {'foo': 'bar'}
        assert add(obj, '/child', {'grandchild': {}}) == {
            'foo': 'bar',
            'child': {
                'grandchild': {}
            }
        }

    def test_adding_to_nonexistent_target(self):
        obj = {'foo': 'bar'}
        with self.assertRaises(NonexistentTarget):
            assert add(obj, '/baz/bat', 'qux')

    def test_escape_ordering(self):
        obj = {
            '/': 9,
            '~1': 10
        }
        assert check(obj, '/~01', 10)

    def test_comparing_strings_and_numbers(self):
        obj = {
            '/': 9,
            '~1': 10
        }
        assert not check(obj, '/~01', '10')

    def test_adding_array_value(self):
        obj = {'foo': ['bar']}
        assert add(obj, '/foo/-', ['abc', 'def']) == {
            'foo': ['bar', ['abc', 'def']]
        }
