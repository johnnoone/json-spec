"""
    jsontools.schema
    ~~~~~~~~~~~~~~~~

    Describes your JSON data format
"""

from __future__ import absolute_import, print_function, unicode_literals

__all__ = ['load', 'loads']

from jsontools import parser
from .validators import factory


def load(file):
    """load schema from a file"""
    dataset = parser.load(file)
    return loads(dataset)


def loads(dataset):
    """load schema from a dataset"""
    return factory(dataset, '<document>#')

shared_loader = {}
