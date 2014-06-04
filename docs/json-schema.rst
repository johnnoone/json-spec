.. module: json.schema

===========
Json Schema
===========

This document describes use to use Json Schema in this library and not the specification_ itself.


Basic
-----

.. code-block:: python

    from json.schema import load

    # data will validate against this schema
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

    # validate this data
    validator.validate({
        'firstName': 'John',
        'lastName': 'Noone',
        'age': 33,
    })


Low level
---------

.. autofunction:: schema.load

.. autofunction:: schema.load_from_file

.. autofunction:: schema.factory


Draft 04
--------

.. autofunction:: schema.draft04.compile

.. autoclass:: schema.draft04.Validator


Exceptions
----------

.. autoclass:: schema.exceptions.CompilationError

.. autoclass:: schema.exceptions.ReferenceError

.. autoclass:: schema.exceptions.ValidationError


Utils
-----

.. automodule:: schema.util
   :members:

.. _`specification`: http://json-schema.org
