"""
    tests.tests_reference
    ~~~~~~~~~~~~~~~~~~~~~

"""

from jsonspec.pointer import extract, ExtractError, RefError, DocumentPointer, Pointer
from jsonspec.pointer import exceptions as events
from . import TestCase


class TestPointer(TestCase):
    document = {
        'foo': ['bar', 'baz', {
            '$ref': 'obj2#/sub'
        }]
    }

    def test_simple(self):
        assert 'baz' == extract(self.document, '/foo/1')

    def test_with_reference(self):
        with self.assertRaises(RefError):
            assert 'quux' == extract(self.document, '/foo/2')

    def test_bypass_reference(self):
        assert 'obj2#/sub' == extract(self.document, '/foo/2/$ref',
                                      bypass_ref=True)

    def test_compare(self):
        assert '/foo' == Pointer('/foo')
        assert Pointer('/foo') != Pointer('/bar')
        tokens = Pointer('//a~1b/c%d/e^f/g|h/i\\j/k\"l/ /m~0n').tokens
        assert tokens == ['', 'a/b', 'c%d', 'e^f', 'g|h', 'i\\j', 'k\"l', ' ', 'm~n']  # noqa

    def test_iteration(self):
        obj = self.document
        for token in Pointer('/foo/1'):
            obj = token.extract(obj)
        assert 'baz' == obj

    def test_document(self):
        dp = DocumentPointer('example.com#/foo')
        assert not dp.is_inner()
        assert dp.document == 'example.com'
        assert dp.pointer == '/foo'

    def test_inner_document(self):
        dp = DocumentPointer('#/foo')
        assert dp.is_inner()
        assert dp.document == ''
        assert dp.pointer == '/foo'


class TestSequence(TestCase):
    document = ['foo', 'bar', {'$ref': 'baz'}]

    def test_sequence(self):
        assert 'bar' == extract(self.document, '/1')

    def test_last_element(self):
        try:
            extract(self.document, '/-')
            self.fail('last element needed')
        except events.LastElement as event:
            assert self.document == event.obj

    def test_ref(self):
        try:
            extract(self.document, '/2')
            self.fail('last element needed')
        except events.RefError as event:
            assert self.document[2] == event.obj

    def test_bypass_ref(self):
        assert self.document[2] == extract(self.document, '/2',
                                           bypass_ref=True)

    def test_out_of_range(self):
        try:
            extract(self.document, '/3')
            self.fail('last element needed')
        except events.OutOfRange as event:
            assert self.document == event.obj

    def test_wrong_type(self):
        try:
            extract(self.document, '/foo')
            self.fail('last element needed')
        except events.WrongType as event:
            assert self.document == event.obj


class TestMapping(TestCase):
    document = {'foo': 42, 'bar': {'$ref': 'baz'}, 4: True}

    def test_mapping(self):
        assert 42 == extract(self.document, '/foo')

    def test_cast(self):
        assert self.document[4] == extract(self.document, '/4')

    def test_ref(self):
        try:
            extract(self.document, '/bar')
            self.fail('last element needed')
        except events.RefError as event:
            assert self.document['bar'] == event.obj

    def test_bypass_ref(self):
        assert self.document['bar'] == extract(self.document, '/bar',
                                               bypass_ref=True)

    def test_out_of_bound(self):
        try:
            extract(self.document, '/3')
            self.fail('out of bound')
        except events.OutOfBounds as event:
            assert self.document == event.obj

        try:
            extract(self.document, '/quux')
            self.fail('out of bound')
        except events.OutOfBounds as event:
            assert self.document == event.obj
