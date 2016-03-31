Json Spec
=========

.. image:: https://badge.fury.io/py/json-spec.png
    :target: http://badge.fury.io/py/json-spec

.. image:: https://travis-ci.org/johnnoone/json-spec.png?branch=master
    :target: https://travis-ci.org/johnnoone/json-spec

This library implements several JSON specs, like `JSON Schema`_,
`JSON Reference`_ and `JSON Pointer`_:

* It works on python 2.7, python 3.3 and above
* It is release under the `BSD license`_


Installation
------------

This library has only weak dependencies. You can simply use pip::

    $ pip install json-spec

Regading you needs, you can install more features. For example, this command
will enable colorated messages::

    $ pip install json-spec[cli]

This one will enable ip format for json schema::

    $ pip install json-spec[ip]

...


CLI Usage
---------

This module expose 2 cli commands.


**json-extract** will extract parts of your json document::

    $ json-extract '#/foo/1' --document-json='{"foo": ["bar", "baz"]}'
    $ echo '{"foo": ["bar", "baz"]}' | json-extract '#/foo/1'
    $ json-extract '#/foo/1' --document-file=doc.json
    $ json-extract '#/foo/1' < doc.json

**json-validate** will validate your document against a schema::

    $ json-validate --schema-file=schema.json --document-json='{"foo": ["bar", "baz"]}'
    $ echo '{"foo": ["bar", "baz"]}' | json-validate --schema-file=schema.json
    $ json-validate --schema-file=schema.json --document-file=doc.json
    $ json-validate --schema-file=schema.json < doc.json


Library usage
-------------

Let say you want to fetch / validate JSON like objects in you python scripts.

You can extract member of an object with `JSON Pointer`_::

    from jsonspec.pointer import extract

    obj = {
        'foo': ['bar', 'baz', 'quux']
    }
    assert 'baz' == extract(obj, '/foo/1')


You can resolve member of any object with `JSON Reference`_::

    from jsonspec.reference import resolve

    obj = {
        'foo': ['bar', 'baz', {
            '$ref': '#/sub'
        }],
        'sub': 'quux'
    }

    assert 'quux' == resolve(obj, '#/foo/2')


You can describe you data with `JSON Schema`_::

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

Other examples can be found in the documentation_ or in the tests_.

.. _`JSON Schema`: http://json-schema.org
.. _`JSON Reference`: http://tools.ietf.org/html/draft-pbryan-zyp-json-ref-03
.. _`JSON Pointer`: http://tools.ietf.org/html/rfc6901
.. _`BSD license`: https://github.com/johnnoone/json-spec/blob/master/LICENSE
.. _documentation: http://py.errorist.io/json-spec/
.. _tests: https://github.com/johnnoone/json-spec/tree/master/tests
