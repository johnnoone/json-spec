from __future__ import print_function

import errno
import os
import stat
import sys
import logging
from functools import wraps
from jsonspec import driver
from .parsers import extract_parser, validate_parser

try:
    from termcolor import colored
except ImportError:

    def colored(string, *args, **kwargs):
        return string


def disable_logging(func):
    """
    Temporary disable logging.
    """
    handler = logging.NullHandler()

    @wraps(func)
    def wrapper(*args, **kwargs):
        logger = logging.getLogger()
        logger.addHandler(handler)
        resp = func(*args, **kwargs)
        logger.removeHandler(handler)
        return resp
    return wrapper


def format_output(func):
    """
    Format output.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            response = func(*args, **kwargs)
        except Exception as error:
            print(colored(error, 'red'), file=sys.stderr)
            sys.exit(1)
        else:
            print(response)
            sys.exit(0)
    return wrapper


@disable_logging
@format_output
def extract_cmd():
    """
    Extract fragment from document.
    """
    from jsonspec.pointer import extract
    from jsonspec.pointer import ExtractError, ParseError

    parser = extract_parser()
    args = parser.parse_args()

    try:
        pointer = args.pointer
        if pointer.startswith('#/'):
            pointer = pointer[1:]
        document = parse_document(args, parser)
        fragment = extract(document, pointer)
        return driver.dumps(fragment, indent=args.indent)
    except ExtractError:
        raise Exception('{} does not match'.format(args.pointer))
    except ParseError:
        raise Exception('{} is not a valid pointer'.format(args.pointer))


@disable_logging
@format_output
def validate_cmd():
    """
    Validate document against a schema.
    """
    from jsonspec.validators import load
    from jsonspec.validators import ValidationError

    parser = validate_parser()
    args = parser.parse_args()

    try:
        document = parse_document(args, parser)
        schema = parse_schema(args, parser)
        validated = load(schema).validate(document)
        return driver.dumps(validated, indent=args.indent)
    except ValidationError as error:
        raise Exception('document does not validate with schema: {}'.format(error.rule))

def parse_document(args, parser):
    if args.document_json:
        return driver.loads(args.document_json)
    elif args.document_file:
        return read_file(args.document_file, 'document')
    else:
        mode = os.fstat(0).st_mode
        if stat.S_ISFIFO(mode):
            # cat doc.json | cmd
            return driver.load(sys.stdin)
        elif stat.S_ISREG(mode):
            # cmd < doc.json
            return driver.load(sys.stdin)

    parser.error('document is required')


def parse_schema(args, parser):
    if args.schema_json:
        try:
            return driver.loads(args.schema_json)
        except Exception:
            raise Exception('could not parse schema, is it a file maybe?')
    elif args.schema_file:
        return read_file(args.schema_file, 'schema')

    parser.error('schema is required')


def read_file(filename, placeholder=None):
    placeholder = placeholder or 'file'

    try:
        return driver.load(open(filename, 'r'))
    except OSError as error:
        if error.errno != errno.EEXIST:
            raise Exception('{} {} does not exists'.format(placeholder, filename))
    except Exception as error:
        raise error
