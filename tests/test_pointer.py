"""
    tests.tests_reference
    ~~~~~~~~~~~~~~~~~~~~~

"""

from json.pointer import extract, ExtractError, DocumentPointer, Pointer
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
        with self.assertRaises(ExtractError):
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
