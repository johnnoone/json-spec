"""
    tests.tests_github
    ~~~~~~~~~~~~~~~~~~

"""

import pytest
from jsonspec.validators import load, ValidationError


def test_issue4():
    validator = load({
        '$schema': 'http://json-schema.org/draft-04/schema#',
        'type': 'object',
        'properties': {
            'props': {
                'type': 'array',
                'items': {
                    'oneOf': [
                        {'type': 'string'},
                        {'type': 'number'}
                    ]
                }
            }
        }
    })

    assert {'props': ['hello']} == validator.validate({'props': ['hello']})

    assert {'props': [42, 'you']} == validator.validate({'props': [42, 'you']})

    with pytest.raises(ValidationError):
        validator.validate({
            'props': [None]
        })

    with pytest.raises(ValidationError):
        validator.validate({
            'props': None
        })

    with pytest.raises(ValidationError):
        validator.validate({
            'props': 'hello'
        })

    with pytest.raises(ValidationError):
        validator.validate({
            'props': 42
        })


def test_issue5():
    import os

    try:
        prev_sep = os.sep
        os.sep = '\\'

        validator = load({
            '$schema': 'http://json-schema.org/draft-04/schema#',
            'type': 'object',
            'definitions': {
                'test': {
                    'type': 'object',
                    'properties': {
                        'foo': {'type': 'string'}
                    },
                    'additionalProperties': False
                }
            },
            'properties': {
                'bar': {
                    '$ref': '#/definitions/test'
                }
            }
        })

        assert {'bar': {'foo': 'test'}} == validator.validate({
            'bar': {
                'foo': 'test',
            }
        })

        with pytest.raises(ValidationError):
            validator.validate({
                'bar': {
                    'foo': 'test',
                    'more': 2
                }
            })

    finally:
        os.sep = prev_sep
