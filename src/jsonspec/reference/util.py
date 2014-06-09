"""
    jsonspec.reference.util
    ~~~~~~~~~~~~~~~~~~~~~~~

"""

__all__ = ['ref', 'loop', 'Mapping', 'MutableMapping']

import fnmatch
import os
import re


def ref(obj):
    """Extracts $ref of object."""
    try:
        return obj['$ref']
    except (KeyError, TypeError):
        return None


def loop(directory, pattern='*'):
    regex = fnmatch.translate(pattern)
    matcher = re.compile(regex)

    def _loop(directory):
        for file in os.listdir(directory):
            path = os.path.join(directory, file)
            if os.path.isfile(path) and matcher.match(path):
                yield path
            elif os.path.isdir(path):
                for subpath in loop(path):
                    yield subpath
    return _loop(directory)


try:
    # py3
    from collections.abc import MutableMapping, Mapping
except ImportError:
    # py2
    from collections import MutableMapping, Mapping
