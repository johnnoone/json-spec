"""
    jsonspec.validators
    ~~~~~~~~~~~~~~~~~~~

"""

__all__ = ['load', 'register', 'Factory', 'Validator', 'ReferenceValidator',
           'CompilationError', 'ReferenceError', 'ValidationError']

from .bases import error, Validator, ReferenceValidator, NotValidator
from .bases import CompoundValidator, AllValidator, AnyValidator, OneValidator
from .types import EnumValidator, StringValidator, NumberValidator
from .types import IntegerValidator, IntegerValidator, NullValidator
from .types import ArrayValidator, ObjectValidator, BooleanValidator
from .exceptions import CompilationError, ReferenceError, ValidationError
from .factorize import register, Context, Factory
from . import draft04  # noqa


def load(schema, uri=None, spec=None, provider=None):
    """Scaffold a validator against a schema.

    :param schema: the schema to compile into a Validator
    :type schema: Mapping
    :param uri: the uri of the schema.
                it may be ignored in case of not cross
                referencing.
    :type uri: Pointer, str
    :param spec: fallback to this spec if the schema does not provides ts own
    :type spec: str
    :param provider: the other schemas, in case of cross
                     referencing
    :type provider: Mapping, Provider...
    """
    factory = Factory(provider, spec)
    return factory(schema, uri or '#')
