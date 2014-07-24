"""
    tests.tests_errors
    ~~~~~~~~~~~~~~~~~~

"""


import pytest
from jsonspec.validators import load
from jsonspec.validators.exceptions import ValidationError
from . import TestCase, fixture


schema = {
    'type': 'object',
    'properties': {
        'foo': {
            'type': 'integer',
            'minimum': -2,
            'maximum': 12,
        },
        'bar': {
            'type': 'string'
        },
        'baz': {
            'type': 'null'
        },
    },
    'dependencies': {
        'baz': ['bar']
    },
    'required': ['foo'],
    'additionalProperties': False
}

scenarii = [
    # Pointer scenarii
    ('foo', {'#/': {'Wrong type'}}, 'object required'),
    ({'foo': 'data'}, {'#/foo': {'Wrong type'}}, 'integer required'),
    ({'bar': 'foo'}, {'#/': {"Missing property"}}, 'string required'),
    ({'foo': 12, 'baz': None}, {'#/': {"Missing property"}}, 'miss a dependencies'),
    ({'foo': 42}, {'#/foo': {"Exceeded maximum"}}, 'too big'),
    ({'foo': 12, 'baz': None, 'quux': True}, {
        '#/': {'Forbidden additional properties', 'Missing property'}
     }, 'too big'),
    ({'foo': 42, 'baz': None, 'quux': True}, {
        '#/': {'Forbidden additional properties', 'Missing property'},
        '#/foo': {'Exceeded maximum'}
     }, 'too big'),
]


@pytest.mark.parametrize('document, expected, reason', scenarii)
def test_errors_object(document, expected, reason):
    try:
        load(schema).validate(document)
        assert False, 'error expected: {}'.format(reason)
    except ValidationError as error:
        f = error.flatten()
        assert f == expected, (reason, expected, f)





schema2 = {
    'type': 'array',
    'items': [
        {
            'type': 'integer',
            'minimum': -2,
            'maximum': 12,
        },
        {
            'type': 'string'
        },
        {
            'type': 'null'
        }
    ],
    'minItems': 2,
    'additionalItems': False
}

scenarii2 = [
    # Pointer scenarii
    ('foo', {'#/': {'Wrong type'}}, 'array required'),
    (['foo', 12], {'#/0': {'Wrong type'}, '#/1': {'Wrong type'}}, 'multiple errors'),
    ([12], {'#/': {'Too few elements'}}, 'string required'),
    ([12, 12, 12, 12], {
        '#/3': {'Forbidden value'},
        '#/1': {'Wrong type'},
        '#/2': {'Wrong type'}
     }, 'string required'),
]


@pytest.mark.parametrize('document, expected, reason', scenarii2)
def test_errors_array(document, expected, reason):
    try:
        load(schema2).validate(document)
        assert False, 'error expected: {}'.format(reason)
    except ValidationError as error:
        f = error.flatten()
        assert f == expected, (reason, expected, f)
