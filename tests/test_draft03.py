"""
    tests.tests_dratf04
    ~~~~~~~~~~~~~~~~~~~~~~

    Test against `Common test suite`_.

    .. _`Common test suite`:: https://github.com/json-schema/JSON-Schema-Test-Suite
"""

from jsonspec.validators import load, ValidationError, CompilationError
from jsonspec.reference.providers import SpecProvider, ProxyProvider
from jsonspec import driver as json

import io
import os
import pytest
import logging
from six import PY2
logger = logging.getLogger(__name__)
here = os.path.dirname(os.path.abspath(__file__))


def contents(*paths):
    fullpath = os.path.join(here, 'suite', *paths)
    print("fullp", fullpath)
    d = len(fullpath) + 1
    for dirpath, dirnames, filenames in os.walk(fullpath):
        for filename in filenames:
            if filename.endswith('.json'):
                filepath = os.path.join(dirpath, filename)
                with io.open(filepath, 'r', encoding='utf-8') as file:
                    yield json.load(file), filepath[d:]


provider = ProxyProvider(SpecProvider())
for data, src in contents('remotes'):
    provider[os.path.join('http://localhost:1234', src)] = data


def scenarios(draft):
    for data, src in contents('tests', draft):
        # no ECMA 262 regex parser
        skip = ['optional/jsregex.json']
        if PY2:
            # json module cannot handle well unicode strings
            skip.extend(('minLength.json', 'maxLength.json'))
        if src in skip:
            continue

        for block in data:
            for test in block['tests']:
                yield block['schema'], test['description'], test['data'], test['valid'], src


@pytest.mark.parametrize('schema, description, data, valid, src', scenarios('draft3'))
def test_common(schema, description, data, valid, src):
    try:
        load(schema, provider=provider, spec='http://json-schema.org/draft-03/schema#').validate(data)
        if not valid:
            assert False, description
    except (ValidationError, CompilationError) as error:
        if valid:
            logger.exception(error)
            assert False, description
