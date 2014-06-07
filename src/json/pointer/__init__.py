"""
    json.pointer
    ~~~~~~~~~~~~

    JSON Pointer defines a string syntax for identifying a specific value
    within a JavaScript Object Notation (JSON) document.

"""

from __future__ import absolute_import, print_function, unicode_literals

__all__ = ['extract', 'DocumentPointer',
           'Pointer', 'PointerToken', 'ExtractError']

import logging
from .bases import DocumentPointer, Pointer, PointerToken
from .exceptions import ExtractError

logger = logging.getLogger(__name__)


def extract(obj, pointer, bypass_ref=False):
    """Extract member or attributes from a pointer"""
    return Pointer(pointer).extract(obj, bypass_ref)

