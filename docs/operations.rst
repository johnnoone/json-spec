.. _operations:
.. module: jsonspec.operations

==========
Operations
==========

Operations are inspired by the `JSON Patch`_ specification.

For example::

    from jsonspec import operations

    obj = {
        'foo': {
            'bar': 'baz',
            'waldo': 'fred'
        },
        'qux': {
            'corge': 'grault'
        }
    }
    assert operations.move(obj, '/qux/thud', '/foo/waldo') == {
        'foo': {
            'bar': 'baz'
        },
        'qux': {
            'corge': 'grault',
            'thud': 'fred'
        }
    }
    

Sources, destinations and locations are expressed with :class:`pointer.Pointer`.


Operations
----------

:add:

    The ``add`` operation performs one of the following functions, depending
    upon what the target location references:

    -   If the target location specifies an array index, a new value is
        inserted into the array at the specified index.
    -   If the target location specifies an object member that does not
        already exist, a new member is added to the object.
    -   If the target location specifies an object member that does exist,
        that member's value is replaced.

    For example::

        # add or replace a mapping
        operations.add({'foo': 'bar'}, '/baz', 'qux') == {
            'baz': 'qux',
            'foo': 'bar'
        }

        # add into a sequence
        operations.add(['foo', 'bar'], '/1', 'qux') == ['foo', 'qux', 'bar']


:remove:

    The ``remove`` operation removes the value at the target location::

        # remove a mapping member
        operations.remove({
            'baz': 'qux',
            'foo': 'bar'
        }, '/baz') == {'foo': 'bar'}

        # remove a sequence element
        operations.remove(['bar', 'qux', 'baz'], '/1') == ['bar', 'baz']

:replace:

    The ``replace`` operation replaces the value at the target location
    with a new value::

        operations.replace({
            'baz': 'qux',
            'foo': 'bar'
        }, '/baz', 'boo') == {
            'baz': 'boo',
            'foo': 'bar'
        }

:move:

    The ``move`` operation removes the value at a specified location and
    adds it to the target location::

        # move a value into a mapping
        operations.move({
            'foo': {
                'bar': 'baz',
                'waldo': 'fred'
            },
            'qux': {
                'corge': 'grault'
            }
        }, '/qux/thud', '/foo/waldo') == {
            'foo': {
                'bar': 'baz'
            },
            'qux': {
                'corge': 'grault',
                'thud': 'fred'
            }
        }

        # move an array element
        operations.move([
            'all', 'grass', 'cows', 'eat'
        ], '/3', '/1') == [
            'all', 'cows', 'eat', 'grass'
        ]

:copy:

    The ``copy`` operation copies the value at a specified location to the
    target location::

        operations.copy({
            'foo': {'bar': 42}, 
        }, 'baz', '/foo/bar') == {
            'foo': {'bar': 42}, 'baz': 42
        }

:check:

    The ``test`` operation tests that a value at the target location is
    equal to a specified value::

        # testing a value with success
        obj = {
            'baz': 'qux',
            'foo': ['a', 2, 'c']
        }
        assert operations.check(obj, '/baz', 'qux')
        assert operations.check(obj, '/foo/1', 2)

        # testing a value with error
        assert not operations.check({'baz': 'qux'}, '/baz', 'bar')


API
---

.. autofunction:: operations.check

.. autofunction:: operations.remove

.. autofunction:: operations.add

.. autofunction:: operations.replace

.. autofunction:: operations.move

.. autofunction:: operations.copy

.. autoclass:: operations.Target
    :members:


.. _`JSON Patch`: http://tools.ietf.org/html/rfc6902
