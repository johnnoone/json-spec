Json Extensions
===============

.. image:: https://badge.fury.io/py/json-extensions.png
    :target: http://badge.fury.io/py/json-extensions

.. image:: https://travis-ci.org/johnnoone/json-extensions.png?branch=master
    :target: https://travis-ci.org/johnnoone/json-extensions

.. image:: https://pypip.in/d/json-extensions/badge.png
    :target: https://pypi.python.org/pypi/json-extensions

This library implements several JSON specs, like `JSON Schema`_,  `JSON Reference`_ and `JSON Pointer`_:

* It works on python 2.7, python 3.3 and above
* It is release under the `BSD license`_


Installation
------------

This library has no special dependencies. You can simply use pip:

.. code-block:: bash

    $ pip install json-extensions


Usage
-----

Let say you want to fetch / validate JSON like objects.

You can extract member of an object with `JSON Pointer`_::

    from json.pointer import extract

    obj = {
        'foo': ['bar', 'baz', 'quux']
    }
    assert 'baz' == extract(obj, '/foo/1')


You can resolve member of any object with `JSON Reference`_::

    from json.reference import resolve

    obj = {
        'foo': ['bar', 'baz', {
            '$ref': '#/sub'
        }],
        'sub': 'quux'
    }

    assert 'quux' == resolve(obj, '#/foo/2')


You can describe you data with `JSON Schema`_::

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

Other examples can be found in the documentation_ or in the tests_.

.. _`JSON Schema`: http://json-schema.org
.. _`JSON Reference`: http://tools.ietf.org/html/draft-pbryan-zyp-json-ref-03
.. _`JSON Pointer`: http://tools.ietf.org/html/rfc6901
.. _`BSD license`: LICENSE
.. _documentation: http://json-extensions.readthedocs.org
.. _tests: https://github.com/johnnoone/json-extensions/tree/master/tests
