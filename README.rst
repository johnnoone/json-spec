===============
Json Extensions
===============

.. image:: https://badge.fury.io/py/jsontools.png
    :target: http://badge.fury.io/py/jsontools

.. image:: https://travis-ci.org/johnnoone/jsontools.png?branch=master
    :target: https://travis-ci.org/johnnoone/jsontools

.. image:: https://pypip.in/d/jsontools/badge.png
    :target: https://pypi.python.org/pypi/jsontools


* Free software: BSD license
* Documentation: http://jsonexts.readthedocs.org.

json.schema
-----------

`JSON Schema`_	describes your JSON data format

.. block-code: python

    from json.schema import load

    validator = load({
        'title': 'Example Schema',
        'type': 'object',
        'properties': {
            'age': {
                'description': 'Age in years',
                'minimum': 0,
                'type': 'integer'
            },
            'firstName': {
                'type': 'string'
            },
            'lastName': {
                'type': 'string'
            }
        },
        'required': [
            'firstName',
            'lastName'
        ]
    })

    validator.validate({
        'firstName': 'John',
        'lastName': 'Noone',
        'age': 33,
    })


:: _`JSON Schema`: http://json-schema.org
