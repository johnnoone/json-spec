.. module: json.pointer

============
Json Pointer
============

This module implements `JSON Pointer`_.

Basic
-----

.. code-block:: python

    from json.pointer import extract, Pointer
    document = {
        'foo': ['bar', 'baz', {
            '$ref': 'obj2#/sub'
        }]
    }
    assert 'baz' == extract(document, '/foo/1')

    # or iteratively

    obj = document
    for token in Pointer('/foo/1'):
        obj = token.extract(obj)
    assert 'baz' == obj

By default when a JSON Reference is encountered an exception is raised.
This behavior can be desactivated by setting ``bypass_ref=True``.

.. code-block:: python

    assert 'obj2#/sub' == extract(document, '/foo/2/$ref', bypass_ref=True)


Low level
---------

.. autofunction:: pointer.extract

.. autoclass:: pointer.DocumentPointer
    :members:

.. autoclass:: pointer.Pointer
    :members:

.. autoclass:: pointer.PointerToken
    :members:


Exceptions
----------

.. autoclass:: pointer.ExtractError


.. _`JSON Pointer`: http://tools.ietf.org/html/rfc6901