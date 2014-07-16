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

If you need to resolve JSON Reference, you can that a look at :doc:`reference`.


**About relative JSON Reference**

`Relative JSON Pointer`_ are still experimental, but this library offers
an implementation of it.

It implies to convert the whole document into a staged document, and then follow
these rules:

.. code-block:: python

    from jsonspec.pointer import extract, stage

    staged_doc = stage({
        'foo': ['bar', 'baz'],
        'highly': {
            'nested': {
                'objects': True
            }
        }
    })

    baz_relative = extract(self.document, '/foo/1')

    # staged objects
    assert extract(baz_relative, '0') == 'baz'
    assert extract(baz_relative, '1/0') == 'bar'
    assert extract(baz_relative, '2/highly/nested/objects') == True  # `foo is True` won't work

    # keys, not staged
    assert extract(baz_relative, '0#') == 1
    assert extract(baz_relative, '1#') == 'foo'

    # unstage object
    assert extract(baz_relative, '0').obj == 'baz'
    assert extract(baz_relative, '1/0').obj == 'bar'
    assert extract(baz_relative, '2/highly/nested/objects').obj is True



API
---

.. autofunction:: pointer.extract

.. autoclass:: pointer.DocumentPointer
    :members:

.. autoclass:: pointer.Pointer
    :members:

.. autoclass:: pointer.PointerToken
    :members:

.. autofunction:: pointer.stage


Exceptions
~~~~~~~~~~

.. autoclass:: pointer.ExtractError

.. autoclass:: pointer.RefError

.. autoclass:: pointer.LastElement

.. autoclass:: pointer.OutOfBounds

.. autoclass:: pointer.OutOfRange

.. _`JSON Pointer`: http://tools.ietf.org/html/rfc6901
.. _`Relative JSON Pointer`: http://tools.ietf.org/html/draft-luff-relative-json-pointer-00