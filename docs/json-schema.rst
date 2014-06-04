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

.. autofunction:: json.schema.load

.. autofunction:: json.schema.load_from_file

.. autofunction:: json.schema.factory

.. automodule:: json.schema.bases
   :members:
   :undoc-members:

.. automodule:: json.schema.draft04
   :members:

.. automodule:: json.schema.exceptions
   :members:
   :undoc-members:

.. automodule:: json.schema.util
   :members:
   :undoc-members:

.. _`specification`: http://json-schema.org
