"""
    jsontools.schema
    ~~~~~~~~~~~~~~~~

    Describes your JSON data format
"""

from __future__ import absolute_import, print_function, unicode_literals

__all__ = ['load', 'loads']

from jsontools import parser
from .validators import factory


def load(file, **kwargs):
    """load schema from a file"""
    dataset = parser.load(file)
    return loads(dataset, **kwargs)


def loads(dataset, **kwargs):
    """load schema from a dataset"""
    return factory(dataset, '<document>#', **kwargs)

shared_loader = {}
