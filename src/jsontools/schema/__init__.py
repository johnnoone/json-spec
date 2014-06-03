"""
    jsontools.schema
    ~~~~~~~~~~~~~~~~

    JSON Schema defines the media type "application/schema+json",
    a JSON based format for defining the structure of JSON data.

    JSON Schema provides a contract for what JSON data is required
    for a given application and how to interact with it.

    JSON Schema is intended to define validation, documentation,
    hyperlink navigation, and interaction control of JSON data.

"""

from __future__ import absolute_import, print_function, unicode_literals

__all__ = ['load', 'loads']

from copy import deepcopy

from jsontools import parser
from jsontools.exceptions import CompilationError
from .draft04 import compile


def load(file, **kwargs):
    """load schema from a file"""
    dataset = parser.load(file)
    return loads(dataset, **kwargs)


def loads(dataset, **kwargs):
    """load schema from a dataset"""
    return factory(dataset, '<document>#', **kwargs)


def factory(schema, uri, default_spec=None, loader=None):

    default_spec = default_spec or 'http://json-schema.org/draft-04/schema#'
    spec = schema.get('$schema', default_spec)
    if spec != 'http://json-schema.org/draft-04/schema#':
        raise CompilationError('can parse draft-04 only', schema)

    loader = loader or {}
    loader[uri] = deepcopy(schema)

    return compile(schema, uri, loader)
