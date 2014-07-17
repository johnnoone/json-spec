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

About format
~~~~~~~~~~~~

`Formats`_ are registered via ``entry_points`` in ``setup.py``:


.. code-block:: ini

    [entry_points]

    jsonspec.validators.formats =
        date-time = jsonspec.validators.util:validate_datetime
        email = jsonspec.validators.util:validate_email
        hostname = jsonspec.validators.util:validate_hostname
        ipv4 = jsonspec.validators.util:validate_ipv4 [ip]
        ipv6 = jsonspec.validators.util:validate_ipv6 [ip]
        uri = jsonspec.validators.util:validate_uri

You can expose yours with this technic.

Some formats rely on external modules, and they are not enabled by default.
For enabling them, uses these commands:


========= =========================
Format    Install command
--------- -------------------------
ipv4      pip install json-spec[ip]
ipv6      pip install json-spec[ip]
hostname  pip install json-spec
========= =========================

API
---

.. autofunction:: validators.load

.. autofunction:: validators.draft04.compile

.. autofunction:: validators.register

.. autoclass:: validators.ReferenceValidator
    :members:

.. autoclass:: validators.Draft04Validator
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
.. _`formats`: http://json-schema.org/latest/json-schema-validation.html#rfc.section.7
