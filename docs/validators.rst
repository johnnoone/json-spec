.. _schema:
.. module: jsonspec.validators

==========
Validators
==========

This document describes use to use Json Schema in this library, not the specification_ itself.


Basic
-----

.. code-block:: python

    from jsonspec.validators import load

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

.. autofunction:: validators.load

.. autoclass:: validators.Draft04Validator
    :members:

.. autoclass:: validators.ReferenceValidator
    :members:


Exceptions
----------

.. autoclass:: validators.CompilationError
    :members:

.. autoclass:: validators.ReferenceError
    :members:

.. autoclass:: validators.ValidationError
    :members:


.. _`specification`: http://json-schema.org
