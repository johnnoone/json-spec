"""
    jsonspec.validators.factorize
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""

__all__ = ['Context', 'Factory', 'register']

from functools import partial
from jsonspec.pointer import DocumentPointer
from jsonspec.reference import LocalRegistry
from .exceptions import CompilationError


class Context(object):
    """

    :ivar factory: global factory
    :ivar registry: the current registry
    :ivar spec: the current spec
    """
    def __init__(self, factory, registry, spec=None):
        self.factory = factory
        self.registry = registry
        self.spec = spec

    def __call__(self, schema, pointer):
        return self.factory(schema, pointer, self.spec)

    def resolve(self, pointer):
        return self.factory(self.registry.resolve(pointer), pointer, self.spec)


class Factory(object):
    """

    :ivar provider: global registry
    :ivar spec: default spec
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
        context = Context(self, registry, spec)
        return compiler(schema, pointer, context)

    @classmethod
    def register(cls, spec, compiler):
        cls.compilers[spec] = compiler
        return compiler


def register(compiler=None, spec=None):
    """
    Expose compiler to factory.

    :param compiler: the callable to expose
    :type compiler: callable
    :param spec: name of the spec
    :type spec: str

    It can be used as a decorator::

        @register(spec='my:first:spec')
        def my_compiler(schema, pointer, context):
            return ObjectValidator(schema)

    or as a function::

        def my_compiler(schema, pointer, context):
            return ObjectValidator(schema)

        register(my_compiler, 'my:second:spec')

    """
    if not spec:
        raise CompilationError('Spec is required')
    if not compiler:
        return partial(register, spec=spec)
    return Factory.register(spec, compiler)
