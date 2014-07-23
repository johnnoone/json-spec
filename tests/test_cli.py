"""
    tests.tests_cli
    ~~~~~~~~~~~~~~~

"""

import os
import os.path
import pytest
from subprocess import Popen, PIPE
from jsonspec import cli
from . import TestCase, move_cwd


scenarii = [
    # Pointer scenarii

    # inline json
    ("""json-extract '#/foo/1' --document-json='{"foo": ["bar", "baz"]}'""", True),
    ("""echo '{"foo": ["bar", "baz"]}' | json-extract '#/foo/1'""", True),
    ("""json-extract '#/foo/2' --document-json='{"foo": ["bar", "baz"]}'""", False),
    ("""echo '{"foo": ["bar", "baz"]}' | json-extract '#/foo/2'""", False),

    # existant file
    ("""cat fixtures/first.data1.json | json-extract '#/name'""", True),
    ("""json-extract '#/name' < fixtures/first.data1.json""", True),
    ("""json-extract '#/name' --document-file=fixtures/first.data1.json""", True),

    # existant file, but pointer does not match
    ("""cat fixtures/first.data1.json | json-extract '#/foo/bar'""", False),
    ("""json-extract '#/foo/bar' < fixtures/first.data1.json""", False),
    ("""json-extract '#/foo/bar' --document-file=fixtures/first.data1.json""", False),

    # inexistant file
    ("""json-extract '#/foo/1' --document-file=doc.json""", False),
    ("""json-extract '#/foo/1' < doc.json""", False),
    ("""cat doc.json | json-extract '#/foo/1'""", False),

    # Schema scenarii

    #
    ("""json-validate --schema-file=fixtures/three.schema.json < fixtures/three.data1.json""", False),
    ("""json-validate --schema-file=fixtures/three.schema.json < fixtures/three.data2.json""", True),
]


@pytest.mark.parametrize('cmd, success', scenarii)
def test_cli(cmd, success):
    with move_cwd():
        proc = Popen(cmd, stderr=PIPE, stdout=PIPE, shell=True)
        stdout, stderr = proc.communicate()
        ret = proc.returncode

    if success and ret > 0:
        assert False, (ret, stdout, stderr)
    if not success and ret == 0:
        assert False, (ret, stdout, stderr)
