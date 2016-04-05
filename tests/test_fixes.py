from jsonspec.validators import load


def test_tuple():
    doc = {
        'default': {
            'ipv4': ('10.140.65.1', 'en4')
        },
        'ipv4': [
            ('10.140.65.1', 'en4', True),
            ('10.140.66.1', 'en0', False)
        ]
    }
    assert load({
        'type': 'object',
        'properties': {
            'default': {
                'type': 'object',
                'properties': {
                    'ipv4': {
                        'type': 'array',
                        'items': [
                            {'type': 'string', 'format': 'ipv4'},
                            {'type': 'string'},
                        ]
                    },
                    'ipv6': {
                        'type': 'array',
                        'items': [
                            {'type': 'string', 'format': 'ipv6'},
                            {'type': 'string'},
                        ]
                    }
                }
            },
            'ipv4': {
                'type': 'array',
                'items': {
                    'type': 'array',
                    'items': [
                        {'type': 'string', 'format': 'ipv4'},
                        {'type': 'string'},
                        {'type': 'boolean'},
                    ]
                }
            },
            'ipv6': {
                'type': 'array',
                'items': {
                    'type': 'array',
                    'items': [
                        {'type': 'string', 'format': 'ipv6'},
                        {'type': 'string'},
                        {'type': 'boolean'},
                    ]
                }
            }
        },
        'required': ['default']
    }).validate(doc)
