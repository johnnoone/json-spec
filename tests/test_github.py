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
