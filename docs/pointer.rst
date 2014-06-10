.. _pointer:
.. module: jsonspec.pointer

============
JSON Pointer
============

`JSON Pointer`_ defines a string syntax for identifying a specific value within a JSON document. The most common usage is this:

.. code-block:: python

    from jsonspec.pointer import extract, Pointer
    document = {
        'foo': ['bar', 'baz', {
            '$ref': 'obj2#/sub'
        }]
    }
    assert 'baz' == extract(document, '/foo/1')

But you can also iter throught the object:

.. code-block:: python

    obj = document
    for token in Pointer('/foo/1'):
        obj = token.extract(obj)
    assert 'baz' == obj

This module is event driven. It means that an event will be raised when it can't be explored.
Here is the most meaningful:

.. list-table::
    :header-rows: 1

    * - Event
      - meaning
    * - :class:`~pointer.RefError`
      - encountered a JSON Reference, :ref:`see <ajr>`.
    * - :class:`~pointer.LastElement`
      - asking for the last element of a sequence
    * - :class:`~pointer.OutOfBounds`
      - member does not exists into the current mapping
    * - :class:`~pointer.OutOfRange`
      - element does not exists into the current sequence


.. _ajr:

**About JSON Reference**

A :class:`pointer.RefError` is raised when when a JSON Reference is encountered.
This behavior can be desactivated by setting ``bypass_ref=True``.

.. code-block:: python

    assert 'obj2#/sub' == extract(document, '/foo/2/$ref', bypass_ref=True)

If you need to resolve JSON Reference, use can that a look at :doc:`reference`.

API
---

.. autofunction:: pointer.extract

.. autoclass:: pointer.DocumentPointer
    :members:

.. autoclass:: pointer.Pointer
    :members:

.. autoclass:: pointer.PointerToken
    :members:


Exceptions
~~~~~~~~~~

.. autoclass:: pointer.ExtractError

.. autoclass:: pointer.RefError

.. autoclass:: pointer.LastElement

.. autoclass:: pointer.OutOfBounds

.. autoclass:: pointer.OutOfRange

.. _`JSON Pointer`: http://tools.ietf.org/html/rfc6901