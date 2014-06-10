"""
    tests
    ~~~~~
"""

__all__ = ['fixture', 'fixture_dirname', 'TestCase']

import os.path
import unittest
import json

import logging

logging.basicConfig(level=logging.INFO)

here = os.path.dirname(os.path.abspath(__file__))
fixture_dirname = os.path.join(here, 'fixtures')


def fixture(filename):
    fullpath = os.path.join(here, 'fixtures', filename)
    with open(fullpath, 'r') as file:
        return json.load(file)


class TestCase(unittest.TestCase):
    pass
