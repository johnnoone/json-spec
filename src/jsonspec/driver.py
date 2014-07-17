"""
    jsonspec.driver
    ~~~~~~~~~~~~~~~

"""


try:
    from simplejson import *  # noqa
except ImportError:
    from json import *  # noqa
