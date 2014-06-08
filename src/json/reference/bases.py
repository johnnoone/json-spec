"""
    json.reference.bases
    ~~~~~~~~~~~~~~~~~~~~

"""

__all__ = ['LocalRegistry', 'Registry']

import logging
from .exceptions import NotFound, Forbidden
from .util import ref, MutableMapping
from json.pointer import DocumentPointer

logger = logging.getLogger(__name__)


class Registry(MutableMapping):
    """Register all documents.

    :ivar docs: all documents

    """

    def __init__(self, docs=None):
        self.docs = docs or {}
        super(Registry, self).__init__()

    def prototype(self, dp):
        obj = self[dp.document]
        return self[dp.document], LocalRegistry(obj, self)

    def resolve(self, pointer):
        """Resolve from documents.

        :param pointer: foo
        :type pointer: DocumentPointer
        """

        dp = DocumentPointer(pointer)
        obj, fetcher = self.prototype(dp)

        for token in dp.pointer:
            obj = token.extract(obj, bypass_ref=True)
            reference = ref(obj)
            if reference:
                obj = fetcher.resolve(reference)
        return obj

    def __getitem__(self, uri):
        try:
            return self.docs[uri]
        except KeyError:
            return NotFound('{!r} not registered'.format(uri))

    def __setitem__(self, uri, obj):
        self.docs[uri] = obj

    def __delitem__(self, uri):
        del self.docs[uri]

    def __len__(self):
        return len(self.docs)

    def __iter__(self):
        return iter(self.docs)


class LocalRegistry(Registry):
    """Scoped registry to a local document.

    :ivar doc: the local document
    :ivar registry: all documents
    :ivar key: current document identifier

    """

    key = '<local>'

    def __init__(self, doc, registry=None):
        self.doc = doc
        self.registry = registry or {}

    def prototype(self, dp):
        if dp.is_inner():
            return self.doc, self
        else:
            obj = self[dp.document]
            return self[dp.document], LocalRegistry(obj, self)

    def __getitem__(self, uri):
        try:
            return self.doc if uri == self.key else self.registry[uri]
        except (NotFound, KeyError):
            return NotFound('{!r} not registered'.format(uri))

    def __setitem__(self, uri, obj):
        if uri == self.key:
            raise Forbidden('setting {} is forbidden'.format(self.key))
        self.registry[uri] = obj

    def __delitem__(self, uri):
        if uri == self.key:
            raise Forbidden('deleting {} is forbidden'.format(self.key))
        del self.registry[uri]

    def __len__(self):
        return len(set(list(self.registry.keys()) + [self.key]))

    def __iter__(self):
        yield self.key
        for key in self.registry.keys():
            yield key
