.. _reference:
.. module: jsonspec.reference

==============
JSON Reference
==============

`JSON Reference`_ allows a JSON value to reference another value in a JSON document.
This module implements utilities for exploring these objects.

.. note::

    A JSON Reference is a mapping with a unique key ``$ref``, whose value is a :doc:`pointer`. For example, this object:

    .. code-block:: javascript

        {
          "foo": {"$ref": "#/bar"},
          "bar": true
        }

    Can be resolved as:

    .. code-block:: javascript

        {
          "foo": true,
          "bar": true
        }

They are some ways to resolve JSON Reference. The simplest one:


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


You may do not already know which documents you will need to resolve your document. For this case, you can plug providers. Actually, these are:

.. list-table::
    :header-rows: 1

    * - provider
      - usage
    * - :class:`~reference.providers.PkgProvider`
      - load any provider from setuptools entrypoints
    * - :class:`~reference.providers.FilesystemProvider`
      - load documents from filesystem
    * - :class:`~reference.providers.SpecProvider`
      - load latest JSON Schema specs.


For example, your document refer to stored documents on your filesystem:


.. code-block:: python

    from jsonspec.reference import Registry
    from jsonspec.reference.providers import FileSystemProvider

    obj = {
        'foo': {'$ref': 'my:doc#/sub'}
    }
    provider = FileSystemProvider('/path/to/my/doc', prefix='my:doc')

    resolve(obj, '#/foo/2', {
        'obj2': {'sub': 'quux'}
    })



API
---

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

.. autoclass:: reference.providers.PkgProvider
    :members:

.. autoclass:: reference.providers.FilesystemProvider
    :members:

.. autoclass:: reference.providers.SpecProvider
    :members:

.. _`JSON Reference`: http://tools.ietf.org/html/draft-pbryan-zyp-json-ref-03
