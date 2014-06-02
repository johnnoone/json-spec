"""
    jsontools.parser
    ~~~~~~~~~~~~~~~~

    Parse json document.
"""


try:
    # it is well-known that the simplejson librarie is faster
    # than the Pyhon one.
    from simplejson import *
except ImportError:
    from json import *
