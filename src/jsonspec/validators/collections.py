__all__ = ['Items']

import itertools
from .bases import Validator


class Items(object):
    """
    Describes items and additionalItems rules
    """

    def __init__(self, key):
        self.key = key

    def __get__(self, obj, type=None):
        iterable = getattr(obj, self.key, [])
        if isinstance(iterable, Validator):
            return itertools.cycle([iterable])
        if not iterable:
            return []
        return iterable

    def __set__(self, obj, value):
        setattr(obj, self.key, value)
