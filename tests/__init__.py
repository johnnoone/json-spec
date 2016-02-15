"""
    tests
    ~~~~~
"""

__all__ = ['fixture', 'fixture_dir', 'TestCase', 'TestMappingType', 'TestSequenceType']

import json
import logging
import os.path
import unittest
from contextlib import contextmanager
from collections import MutableMapping, MutableSequence

logging.basicConfig(level=logging.INFO)

here = os.path.dirname(os.path.abspath(__file__))
fixture_dir = os.path.join(here, 'fixtures')


def fixture(filename):
    fullpath = os.path.join(here, 'fixtures', filename)
    with open(fullpath, 'r') as file:
        return json.load(file)


@contextmanager
def move_cwd():
    cwd = os.getcwd()
    os.chdir(here)
    yield cwd
    os.chdir(cwd)


class TestCase(unittest.TestCase):
    pass


class TestMappingType(dict, MutableMapping):
    def copy(self):
        if self.__class__ is UserDict:
            return UserDict(self.data.copy())
        import copy
        data = self.data
        try:
            self.data = {}
            c = copy.copy(self)
        finally:
            self.data = data
        c.update(self)
        return c


class TestSequenceType(list, MutableSequence):
    def copy(self):
        return self.__class__(self)
