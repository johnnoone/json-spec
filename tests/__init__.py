"""
    tests
    ~~~~~
"""

__all__ = ['fixture', 'fixture_dir', 'TestCase']

import json
import logging
import os.path
import unittest
from contextlib import contextmanager

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
