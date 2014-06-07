.. module: json.pointer

============
Json Pointer
============


Basic
-----

.. code-block:: python

    from json.pointer import extract
    document = {
        'foo': ['bar', 'baz', {
            '$ref': 'obj2#/sub'
        }]
    }
    assert 'baz' == extract(document, '/foo/1')

or

.. code-block:: python

    obj = document
    for token in Pointer('/foo/1'):
        obj = token.extract(obj)
    assert 'baz' == obj


Low level
---------

.. autofunction:: pointer.extract

.. autoclass:: pointer.DocumentPointer

.. autoclass:: pointer.Pointer

.. autoclass:: pointer.PointerToken


Exceptions
----------

.. autoclass:: pointer.ExtractError


.. _`JSON Pointer`: http://tools.ietf.org/html/rfc6901