"""
    jsontools.schema
    ~~~~~~~~~~~~~~~~

    Describes your JSON data format
"""

from __future__ import absolute_import, print_function, unicode_literals

__all__ = ['load', 'loads']

from jsontools import parser
from jsontools.exceptions import ReferenceError, SchemaError
from .validators import Validator, factory


def load(file):
    """load schema from a file"""
    dataset = parser.load(file)
    return loads(dataset)


def loads(dataset):
    """load schema from a dataset"""
    return Validator(dataset)


class Validator(object):
    def __init__(self, dataset=None, uri=None):
        if dataset:
            uri = uri or '#'
            self.schemas = {
                uri: factory(dataset, uri)
            }
        elif uri in ('#', None):
            raise ReferenceError('uri or dataset must be provided')

        self.dataset = dataset
        self.uri = uri


    def validate(self, obj):
        """
        Validate any object.
        """
        return self.schemas['#'].validate(obj)
