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


API
---

.. autofunction:: validators.load

.. autofunction:: validators.draft04.compile

.. autofunction:: validators.register

.. autoclass:: validators.NotValidator
    :members:

.. autoclass:: validators.ReferenceValidator
    :members:

.. autoclass:: validators.AllValidator
    :members:

.. autoclass:: validators.AnyValidator
    :members:

.. autoclass:: validators.OneValidator
    :members:

.. autoclass:: validators.EnumValidator
    :members:

.. autoclass:: validators.StringValidator
    :members:

.. autoclass:: validators.NumberValidator
    :members:

.. autoclass:: validators.IntegerValidator
    :members:

.. autoclass:: validators.BooleanValidator
    :members:

.. autoclass:: validators.NullValidator
    :members:

.. autoclass:: validators.ArrayValidator
    :members:

.. autoclass:: validators.ObjectValidator
    :members:

.. autoclass:: validators.Context
    :members:

.. autoclass:: validators.Factory
    :members:


Exceptions
----------

.. autofunction:: validators.error

.. autoclass:: validators.CompilationError
    :members:

.. autoclass:: validators.ReferenceError
    :members:

.. autoclass:: validators.ValidationError
    :members:


.. _`specification`: http://json-schema.org
