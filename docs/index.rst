Welcome to JSON Spec
====================

This library implements tools inspired by several cleaver specifications around JSON.

**Features:**

:jsonspec.pointer:

    Implements `JSON Pointer`_ and offers a way to target a subelement.

:jsonspec.reference:

    Implements `JSON Reference`_ and offers a way to cross reference json documents.

:jsonspec.operations:

    Inspired by `JSON Patch`_, it gives the ability to manipulate the document tree.

:jsonspec.validators:

    Implements `JSON Schema`_ draft04, adds the power of document validation.

Of course, it works for Python 2.7, Python 3.3 and Python 3.4.

.. code-block:: python

    from jsonspec.validators import load

    # data will validate against this schema
    validator = load_from_file('schema.json')

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
