"""
    jsonspec.validators.factorize
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""

__all__ = ['Factory', 'register']

from functools import partial
from jsonspec.pointer import DocumentPointer
from jsonspec.reference import LocalRegistry
from .exceptions import CompilationError


class Factory(object):
    """

    :ivar provider: the registry
    :ivar spec: the default spec
    """

    spec = 'http://json-schema.org/draft-04/schema#'
    compilers = {}

    def __init__(self, provider=None, spec=None):
        self.provider = provider or {}
        self.spec = spec or self.spec

    def __call__(self, schema, pointer, spec=None):
        try:
            spec = schema.get('$schema', spec or self.spec)
            compiler = self.compilers[spec]
        except KeyError:
            raise CompilationError('{!r} not registered'.format(spec))

        registry = LocalRegistry(schema, self.provider)
        local = DocumentPointer(pointer)

        if local.document:
            registry[local.document] = schema
        local.document = '<local>'

        return compiler(schema, pointer, self, registry)

    @classmethod
    def register(cls, spec, compiler):
        cls.compilers[spec] = compiler
        return compiler


def register(compiler=None, spec=None):
    if not compiler:
        return partial(register, spec=spec)
    return Factory.register(spec, compiler)
