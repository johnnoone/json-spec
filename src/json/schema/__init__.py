"""
    json.schema
    ~~~~~~~~~~~

    JSON Schema defines the media type "application/schema+json",
    a JSON based format for defining the structure of JSON data.

    JSON Schema provides a contract for what JSON data is required
    for a given application and how to interact with it.

    JSON Schema is intended to define validation, documentation,
    hyperlink navigation, and interaction control of JSON data.

"""

from __future__ import absolute_import, print_function, unicode_literals

__all__ = ['load', 'load_from_file', 'factory']

from copy import deepcopy
from json import load as file_load

from .exceptions import CompilationError
from .draft04 import compile, Draft04Validator
from .bases import Validator, ReferenceValidator


def load(schema, **kwargs):
    """load schema from a python object

    :param schema: The schema
    :type schema: dict
    :return: The validator instance
    :rtype: Validator
    :raises CompilationError: Whole or part of schema failed to be loaded.
    """
    return factory(schema, '<document>#', **kwargs)


def load_from_file(filename, **kwargs):
    """load schema from a file

    :param filename: the json file to be loaded
    :type filename: str
    :return: The validator instance
    :rtype: Validator
    :raises CompilationError: Whole or part of schema failed to be loaded.
    """
    with open(filename, 'r') as file:
        schema = file_load(file)
    return factory(schema, '<document>#', **kwargs)


def factory(schema, uri, default_spec=None, loader=None):

    instance = Factory(loader)
    return instance(schema, uri)

    default_spec = default_spec or 'http://json-schema.org/draft-04/schema#'
    spec = schema.get('$schema', default_spec)
    if spec != 'http://json-schema.org/draft-04/schema#':
        raise CompilationError('can parse draft-04 only', schema)

    loader = loader or {}
    loader[uri] = deepcopy(schema)

    return compile(schema, uri, loader)

class Factory(object):

    def __init__(self, loader=None, spec=None):
        self.loader = loader or {}
        self.spec = spec or 'http://json-schema.org/draft-04/schema#'
        self.compilers = {
            'http://json-schema.org/draft-04/schema#': compile,
        }

    def __call__(self, schema, uri, spec=None):

        spec = schema.get('$schema', spec or self.spec)

        try:
            compiler = self.compilers[spec]
        except KeyError:
            raise CompilationError('spec {!r} not implemented'.format(spec), schema)

        self.loader[uri] = deepcopy(schema)

        return compile(schema, uri, self)

    def get(self, document):
        return self.loader.get('{}#'.format(document))

    def load(self, uri, spec=None):
        doc, _, pointer = uri.partition('#')
        doc = doc or '<document>'
        fragment = self.loader.get('{}#'.format(doc))
        pointer = pointer.lstrip('/')
        while pointer:
            member, _, pointer = pointer.partition('/')
            fragment = fragment[member]
        return self.__call__(fragment, uri, self.spec)
