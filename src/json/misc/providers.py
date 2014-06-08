"""
    json.misc.providers
    ~~~~~~~~~~~~~~~~~~~
"""

__all__ = ['SpecProvider']

from json.reference.providers import FilesystemProvider
import os

here = os.path.realpath(os.path.dirname(__file__))


class SpecProvider(FilesystemProvider):
    """
    Provides specs of http://json-schema.org/
    """

    def __init__(self):
        src = os.path.join(here, 'schemas/')
        prefix = 'http://json-schema.org/'
        super(SpecProvider, self).__init__(src, prefix)
