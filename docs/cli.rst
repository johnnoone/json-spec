======================
Command-line interface
======================

All commands are suitable for bash scriptings :

- they return real error code.
- json documents can be feed with pipelines.


json add
--------

Transform a json document.

**Usage**

::

    json add [-h] [--document-json <doc> | --document-file <doc>]
             [--fragment-json <fragment> | --fragment-file <fragment>]
             [--indent <indentation>]
             <pointer>

**Examples**

.. code-block:: bash

    json add '#/foo/1' --fragment-file=fragment.json --document-json='{"foo": ["bar", "baz"]}'
    echo '{"foo": ["bar", "baz"]}' | json add '#/foo/1' --fragment-json='first'
    json add '#/foo/1' --fragment-file=fragment.json --document-file=doc.json
    json add '#/foo/1' --fragment-file=fragment.json < doc.json


json check
----------

Tests that a value at the target location is equal to a specified value.

**Usage**

::

    json check [-h] [--document-json <doc> | --document-file <doc>]
               [--fragment-json <fragment> | --fragment-file <fragment>]
               <pointer>

**Examples**

.. code-block:: bash

    json check '#/foo/1' --fragment-file=fragment.json --document-json='{"foo": ["bar", "baz"]}'
    echo '{"foo": ["bar", "baz"]}' | json check '#/foo/1' --fragment-file=fragment.json
    json check '#/foo/1' --fragment-file=fragment.json --document-file=doc.json
    json check '#/foo/1' --fragment-file=fragment.json < doc.json


json copy
---------

Copies the value at a specified location to the target location.

**Usage**

::

    json copy [-h] [--document-json <doc> | --document-file <doc>]
              [-t <target>] [--indent <indentation>]
              <pointer>

**Examples**

.. code-block:: bash

    json copy '#/foo/1' --target='#/foo/2' --document-json='{"foo": ["bar", "baz"]}'
    echo '{"foo": ["bar", "baz"]}' | json copy '#/foo/1' --target='#/foo/2'
    json copy '#/foo/1' --target='#/foo/2' --document-file=doc.json
    json copy '#/foo/1' --target='#/foo/2' < doc.json


json extract
------------

Extract a fragment from a json document.

**Usage**

::

    json extract [-h] [--document-json <doc> | --document-file <doc>]
                 [--indent <indentation>]
                 <pointer>

**Examples**

.. code-block:: bash

    json extract '#/foo/1' --document-json='{"foo": ["bar", "baz"]}'
    echo '{"foo": ["bar", "baz"]}' | json extract '#/foo/1'
    json extract '#/foo/1' --document-file=doc.json
    json extract '#/foo/1' < doc.json


json move
---------

Removes the value at a specified location and adds it to the target location.

**Usage**

::

    json move [-h] [--document-json <doc> | --document-file <doc>]
              [-t <target>] [--indent <indentation>]
              <pointer>

**Examples**

.. code-block:: bash

    json move '#/foo/2' --target='#/foo/1' --document-json='{"foo": ["bar", "baz"]}'
    echo '{"foo": ["bar", "baz"]}' | json move '#/foo/2' --target='#/foo/1'
    json move '#/foo/2' --target='#/foo/1' --document-file=doc.json
    json move '#/foo/2' --target='#/foo/1' < doc.json


json remove
-----------

Removes the value at a specified location and adds it to the target location.

**Usage**

::

    json remove [-h] [--document-json <doc> | --document-file <doc>]
                [--indent <indentation>]
                <pointer>

**Examples**

.. code-block:: bash

    json remove '#/foo/1' --document-json='{"foo": ["bar", "baz"]}'
    echo '{"foo": ["bar", "baz"]}' | json remove '#/foo/1'
    json remove '#/foo/1' --document-file=doc.json
    json remove '#/foo/1' < doc.json


json replace
------------

Removes the value at a specified location and adds it to the target location.

**Usage**

::

    json replace [-h] [--document-json <doc> | --document-file <doc>]
                 [--fragment-json <fragment> | --fragment-file <fragment>]
                 [--indent <indentation>]
                 <pointer>

**Examples**

.. code-block:: bash

    json replace '#/foo/1' --fragment-file=fragment.json --document-json='{"foo": ["bar", "baz"]}'
    echo '{"foo": ["bar", "baz"]}' | json replace '#/foo/1' --fragment-file=fragment.json
    json replace '#/foo/1' --fragment-file=fragment.json --document-file=doc.json
    json replace '#/foo/1' --fragment-file=fragment.json < doc.json


json validate
-------------

Validate document against a schema.

**Usage**

::

    json validate [-h] [--document-json <doc> | --document-file <doc>]
                  [--schema-json <schema> | --schema-file <schema>]
                  [--indent <indentation>]

**Examples**

.. code-block:: bash

  json validate --schema-file=schema.json --document-json='{"foo": ["bar", "baz"]}'
  echo '{"foo": ["bar", "baz"]}' | json validate --schema-file=schema.json
  json validate --schema-file=schema.json --document-file=doc.json
  json validate --schema-file=schema.json < doc.json
