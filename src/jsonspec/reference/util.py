"""
    jsonspec.reference.util
    ~~~~~~~~~~~~~~~~~~~~~~~

"""

__all__ = ["ref", "Mapping", "MutableMapping"]


def ref(obj):
    """Extracts $ref of object."""
    try:
        return obj["$ref"]
    except (KeyError, TypeError):
        return None


from collections.abc import Mapping, MutableMapping
