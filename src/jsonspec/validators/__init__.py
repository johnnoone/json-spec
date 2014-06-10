__all__ = ['load', 'register', 'Factory',
           'Validator', 'ReferenceValidator', 'Draft04Validator',
           'CompilationError', 'ReferenceError', 'ValidationError', 
          ]

from .bases import Validator, ReferenceValidator
from .exceptions import CompilationError, ReferenceError, ValidationError
from .factorize import register, Factory
from .draft04 import Draft04Validator

def load(schema, uri=None, spec=None, provider=None):
    """Scaffold a validator against a schema.

    :param schema: the schema to compile into a Validator
    :param uri: the uri of the schema.
                it may be ignored in case of not cross
                referencing.
    :param spec:  the default spec of the schema, if it's
                  not provided
    :param provider: the other schemas, in case of cross
                     referencing
    """
    factory = Factory(provider, spec)
    return factory(schema, uri or '#')
