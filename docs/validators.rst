.. _schema:
.. module: jsonspec.validators

==========
Validators
==========

This module implements `JSON Schema`_ draft03_ and draft04_.


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

Choose specification
~~~~~~~~~~~~~~~~~~~~

Schemas will be parsed by the draft04_ specification by default.
You can setup, or even better mix between draft03_ and draft04_.

Show these examples:

.. code-block:: python

    validator = load({
        'id': 'foo',
        'properties': {
            'bar': {
                'id': 'baz'
            },
        },
    })

:foo schema: parsed with draft04_
:baz schema: parsed with draft04_

.. code-block:: python

    validator = load({
        'id': 'foo',
        'properties': {
            'bar': {
                'id': 'baz'
            },
        },
    }, spec='http://json-schema.org/draft-03/schema#')

:foo schema: parsed with draft03_
:baz schema: parsed with draft03_

.. code-block:: python

    validator = load({
        'id': 'foo',
        'properties': {
            'bar': {
                '$schema': 'http://json-schema.org/draft-03/schema#',
                'id': 'baz'
            },
        },
    })

:foo schema: parsed with draft04_
:baz schema: parsed with draft03_

About format
~~~~~~~~~~~~

This module implements a lot of formats, exposed to every draft:

.. list-table::
    :header-rows: 1

    * - name
      - description
      - enabling
    * - email
      - validate email
      -
    * - hostname
      - validate hostname
      -
    * - ipv4
      - validate ipv4
      - pip install json-spec[ip]
    * - ipv6
      - validate ipv6
      - pip install json-spec[ip]
    * - regex
      - validate regex
      -
    * - uri
      - validate uri
      -
    * - css.color
      - validate css color
      -
    * - rfc3339.datetime
      - see rfc3339_
      -
    * - utc.datetime
      - YYYY-MM-ddThh:mm:SSZ
      -
    * - utc.date
      - YYYY-MM-dd
      -
    * - utc.time
      - hh:mm:SS
      -
    * - utc.millisec
      - any integer, float
      -


Some formats rely on external modules, and they are not enabled by default.

Each draft validator aliases they formats to these formats. See :meth:`draft04 <validators.Draft04Validator.validate_format>` and :meth:`draft03 <validators.Draft03Validator.validate_format>` methods for more details.


Regarding your needs, you can register your own formats. Use ``entry_points`` in your ``setup.py``. for example:

.. code-block:: ini

    [entry_points]

    jsonspec.validators.formats =
        my:format = my.module:validate_format


the function must have this signature:

.. code-block:: python

    from jsonspec.validators.exceptions import ValidationError

    def validate_format(obj):
        if obj == 'wrong':
            raise ValidationError('ojb cannot be wrong')
        return obj


API
---

.. autofunction:: validators.load

.. autofunction:: validators.draft04.compile

.. autofunction:: validators.register

.. autoclass:: validators.ReferenceValidator
    :members:

.. autoclass:: validators.Draft03Validator
    :members:

.. autoclass:: validators.Draft04Validator
    :members:

.. autoclass:: validators.Context
    :members:

.. autoclass:: validators.Factory
    :members:


Exceptions
----------

.. autoclass:: validators.CompilationError
    :members:

.. autoclass:: validators.ReferenceError
    :members:

.. autoclass:: validators.ValidationError
    :members:


.. _`JSON Schema`: http://json-schema.org
.. _`draft03`: http://tools.ietf.org/html/draft-zyp-json-schema-03
.. _`core draft04`: http://tools.ietf.org/html/draft-zyp-json-schema-04
.. _`draft04`: http://tools.ietf.org/html/draft-fge-json-schema-validation-00
.. _rfc3339: http://www.ietf.org/rfc/rfc3339.txt
