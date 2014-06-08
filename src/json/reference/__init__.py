"""
    json.reference
    ~~~~~~~~~~~~~~

    A JSON Reference is a JSON object, which contains a member named
    "$ref", which has a JSON string value.  Example:

    { "$ref": "http://example.com/example.json#/foo/bar" }

    If a JSON value does not have these characteristics, then it SHOULD
    NOT be interpreted as a JSON Reference.

"""

from __future__ import absolute_import, print_function, unicode_literals

__all__ = ['resolve', 'Registry', 'LocalRegistry', 'NotFound', 'Forbidden']

from .bases import Registry, LocalRegistry
from .exceptions import NotFound, Forbidden
from json.pointer import DocumentPointer


def resolve(obj, pointer, registry=None):
    """resolve a local object

    :param obj: the local object.
    :param pointer: the pointer
    :param registry: the registry.
                    It mays be omited if inner json references
                    document don't refer to other documents.
    """

    registry = LocalRegistry(obj, registry or {})
    local = DocumentPointer(pointer)

    if local.document:
        registry[local.document] = obj
    local.document = '<local>'
    return registry.resolve(local)
