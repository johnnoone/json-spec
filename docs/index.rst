Welcome to JSON Spec
====================

JSON Spec implements several JSON specification for Python >= 2.7.
These specifications include `JSON Schema`_:

.. code-block:: python

    from jsonspec.schema import load

    # data will validate against this schema
    validator = load_from_file('schema.json')

    # validate this data
    validator.validate({
        'firstName': 'John',
        'lastName': 'Noone',
        'age': 33,
    })


**Features:**

*   json-pointer
*   json-reference
*   json-schema


Documentation
-------------

.. toctree::
   :maxdepth: 2

   installation
   json-pointer
   json-reference
   json-schema

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

.. _`JSON Schema`: http://json-schema.org
