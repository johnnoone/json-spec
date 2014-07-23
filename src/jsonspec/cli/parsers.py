__all__ = ['extract_parser', 'validate_parser']

import argparse
from textwrap import dedent


def extract_parser():
    """docstring for extract_parser"""

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='Extract a fragment from a json document.',
        epilog=dedent("""\
            examples:
              %(prog)s '#/foo/1' --document-json='{"foo": ["bar", "baz"]}'
              echo '{"foo": ["bar", "baz"]}' | %(prog)s '#/foo/1'
              %(prog)s '#/foo/1' --document-file=doc.json
              %(prog)s '#/foo/1' < doc.json

            """))
    parser.add_argument('pointer', help='a valid json pointer')
    parser.add_argument('--document-json', help='json structure')
    parser.add_argument('--document-file', help='filename')
    parser.add_argument('--indent', type=int, help='indentation')
    return parser


def validate_parser():
    """docstring for extract_parser"""
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='Validate document against a schema.',
        epilog=dedent("""\
            examples:
              %(prog)s --schema-file=schema.json --document-json='{"foo": ["bar", "baz"]}'
              echo '{"foo": ["bar", "baz"]}' | %(prog)s --schema-file=schema.json
              %(prog)s --schema-file=schema.json --document-file=doc.json
              %(prog)s --schema-file=schema.json < doc.json

            """))
    parser.add_argument('--document-json')
    parser.add_argument('--document-file')
    parser.add_argument('--schema-json')
    parser.add_argument('--schema-file')
    parser.add_argument('--indent', type=int, help='indentation')
    return parser
