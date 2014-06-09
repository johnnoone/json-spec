.. _json-reference:
.. module: jsonspec.reference

==============
Json Reference
==============

This module implements `JSON Reference`_.

Basic
-----

.. code-block:: python

    from jsonspec.reference import resolve

    obj = {
        'foo': ['bar', {'$ref': '#/sub'}, {'$ref': 'obj2#/sub'}],
        'sub': 'baz'
    }

    assert 'bar' == resolve(obj, '#/foo/0')
    assert 'baz' == resolve(obj, '#/foo/1')
    assert 'quux' == resolve(obj, '#/foo/2', {
        'obj2': {'sub': 'quux'}
    })


Low level
---------

.. autofunction:: reference.resolve

.. autoclass:: reference.Registry
    :members:

.. autoclass:: reference.LocalRegistry
    :members:


Utils
-----

.. automodule:: reference.util
   :members:



Exceptions
----------

.. autoclass:: reference.NotFound
.. autoclass:: reference.Forbidden


Defining providers
------------------

TODO


.. _`JSON Reference`: http://tools.ietf.org/html/draft-pbryan-zyp-json-ref-03