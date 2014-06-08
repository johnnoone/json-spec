"""
    json.reference.util
    ~~~~~~~~~~~~~~~~~~~

"""

__all__ = ['ref', 'MutableMapping']


def ref(obj):
    """Extracts $ref of object."""
    try:
        return obj['$ref']
    except (KeyError, TypeError):
        return None

try:
    # py3
    from collections.abc import MutableMapping
except ImportError:
    # py2
    from collections import MutableMapping
