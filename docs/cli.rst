======================
Command-line interface
======================

json-extract
------------

Extract a fragment from a json document.

**Usage**

::

    json-extract [-h] [--document-json DOCUMENT_JSON]
                 [--document-file DOCUMENT_FILE] [--indent INDENT]
                 pointer

**Examples**

.. code-block:: bash

    json-extract '#/foo/1' --document-json='{"foo": ["bar", "baz"]}'
    echo '{"foo": ["bar", "baz"]}' | json-extract '#/foo/1'
    json-extract '#/foo/1' --document-file=doc.json
    json-extract '#/foo/1' < doc.json


json-validate
-------------

Validate document against a schema.

**Usage**

::

    json-validate [-h] [--document-json DOCUMENT_JSON]
                  [--document-file DOCUMENT_FILE]
                  [--schema-json SCHEMA_JSON] [--schema-file SCHEMA_FILE]
                  [--indent INDENT]

**Examples**

.. code-block:: bash

  json-validate --schema-file=schema.json --document-json='{"foo": ["bar", "baz"]}'
  echo '{"foo": ["bar", "baz"]}' | json-validate --schema-file=schema.json
  json-validate --schema-file=schema.json --document-file=doc.json
  json-validate --schema-file=schema.json < doc.json
