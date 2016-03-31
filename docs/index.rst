Welcome to JSON Spec
====================

This library implements tools inspired by several cleaver specifications around JSON.

**Features:**

:jsonspec.cli:

Expose `JSON Pointer`_ , `JSON Schema`_ and `JSON Patch`_ to your console:

.. code-block:: bash

    json extract '#/foo/1' --document-json='{"foo": ["bar", "baz"]}'
    json validate --schema-file=schema.json < doc.json
    cat doc.json | json add '#/foo/1' --fragment='{"foo": ["bar", "baz"]}'

:jsonspec.pointer:

Implements `JSON Pointer`_ and `Relative JSON Pointer`_, it offers a way to target a subelement.

:jsonspec.reference:

Implements `JSON Reference`_ and offers a way to cross reference json documents.

:jsonspec.operations:

Inspired by `JSON Patch`_, it gives the ability to manipulate the document tree.

:jsonspec.validators:

Implements `JSON Schema`_, it adds the power of document validation.

Of course, it works for Python 2.7, Python 3.4 and Python 3.5.

.. code-block:: python

    from jsonspec.validators import load

    # data will validate against this schema
    validator = load({
        'type': 'object',
        'properties': {
            'firstName': {
                'type': 'string',
            },
            'lastName': {
                'type': 'string',
            },
            'age': {
                'type': 'integer'
            }
        },
        'required': ['firstName', 'lastName', 'age']
    })

    # validate this data
    validator.validate({
        'firstName': 'John',
        'lastName': 'Noone',
        'age': 33,
    })


Documentation
-------------

.. toctree::
   :maxdepth: 2

   installation
   cli
   pointer
   reference
   operations
   validators

Additional Information
----------------------

.. toctree::
   :maxdepth: 1

   contributing
   authors
   history

If you can't find the information you're looking for, have a look at the index or try to find it using the search function:


-   :ref:`genindex`
-   :ref:`search`

.. _`JSON Pointer`: http://tools.ietf.org/html/rfc6901
.. _`JSON Reference`: http://tools.ietf.org/html/draft-pbryan-zyp-json-ref-03
.. _`JSON Patch`: http://tools.ietf.org/html/rfc6902
.. _`JSON Schema`: http://json-schema.org
.. _`Relative JSON Pointer`: http://tools.ietf.org/html/draft-luff-relative-json-pointer-00
