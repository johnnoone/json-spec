"""
    tests
    ~~~~~
"""

__all__ = ['fixture', 'TestCase']

import os.path
import unittest
import json

here = os.path.dirname(os.path.abspath(__file__))


def fixture(filename):
    fullpath = os.path.join(here, 'fixtures', filename)
    with open(fullpath, 'r') as file:
        return json.load(file)


class TestCase(unittest.TestCase):
    pass
