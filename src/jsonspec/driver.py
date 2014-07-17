"""
    jsonspec.driver
    ~~~~~~~~~~~~~~~

"""


try:
    from simplejson import *  # noqa
except ImportError:
    from json import *  # noqa

from functools import wraps


_load = load
_loads = loads

@wraps(_load)
def load(fp, *args, **kwargs):
    return _load(fp, *args, **kwargs)
load.original = _load


@wraps(_loads)
def loads(s, *args, **kwargs):
    # if not encoding:
    #     try:
    #         encoding = 'utf-16'
    #         return _loads(s, encoding, *args, **kwargs)
    #     except UnicodeDecodeError:
    #         encoding = 'utf-8'
    #         return _loads(s, encoding, *args, **kwargs)
    return _loads(s, *args, **kwargs)
loads.original = _loads
