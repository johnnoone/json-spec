"""
    jsonspec.validators.draft04
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Implements JSON Schema draft04.
"""

__all__ = ['compile']

from copy import deepcopy
import logging
import os.path

from .bases import ReferenceValidator, AllValidator, AnyValidator, OneValidator, NotValidator  # noqa
from .types import EnumValidator, StringValidator, NumberValidator
from .types import IntegerValidator, BooleanValidator, NullValidator
from .types import ArrayValidator, ObjectValidator
from .exceptions import CompilationError
from .factorize import register

from six import integer_types, string_types

logger = logging.getLogger(__name__)


@register(spec='http://json-schema.org/draft-04/schema#')
def compile(schema, pointer, context):
    """
    Compiles schema with `JSON Schema`_ draft-04.

    :param schema: obj to compile
    :type schema: Mapping
    :param pointer: uri of the schema
    :type pointer: Pointer, str
    :param context: context of this schema
    :type context: Context

    .. _`JSON Schema`: http://json-schema.org
    """

    if '$ref' in schema:
        return ReferenceValidator(schema['$ref'], context)
    schema = deepcopy(schema)

    attrs = {}
    attrs['title'] = schema.pop('title', None)
    attrs['description'] = schema.pop('description', None)
    attrs['uri'] = pointer

    if 'not' in schema:
        attr = schema.pop('not')
        if not isinstance(attr, dict):
            raise CompilationError('not must be a dict', schema)
        validator = compile(attr, os.path.join(pointer, 'not'), context)
        return NotValidator(validator, **attrs)

    for name in ('allOf', 'anyOf', 'oneOf'):
        if name in schema:
            attr = schema.pop(name)
            if not isinstance(attr, list):
                raise CompilationError('{} must be a list'.format(name),
                                       schema)
            validators = set()
            for i, element in enumerate(attr):
                sub_uri = os.path.join(pointer, name, str(i))
                validator = compile(element, sub_uri, context)
                validators.add(validator)
            if name == 'allOf':
                return AllValidator(validators, **attrs)
            if name == 'anyOf':
                return AnyValidator(validators, **attrs)
            if name == 'oneOf':
                return OneValidator(validators, **attrs)

    if 'default' in schema:
        attrs['default'] = schema.pop('default')

    if 'enum' in schema:
        attr = schema.pop('enum')
        if not isinstance(attr, list):
            raise CompilationError('enum must be a list', schema)
        attrs['enum'] = attr
        return EnumValidator(**attrs)

    if 'type' not in schema:
        logger.warn('you should set type %s', schema)
    attrs['type'] = schema.pop('type', None)

    for name in ('items', 'additionalItems'):
        if name not in schema:
            continue

        attr = schema.pop(name)
        sub_uri = os.path.join(pointer, name)
        if isinstance(attr, list):
            # each value must be a json schema
            attr = [compile(attr, sub_uri, context) for element in attr]
        elif isinstance(attr, dict):
            # value must be a json schema
            attr = compile(attr, sub_uri, context)
        elif not isinstance(attr, bool):
            # should be a boolean
            raise CompilationError('wrong type for {}'.format(name), schema)  # noqa

        attrs[{'additionalItems': 'additional_items'}.get(name, name)] = attr

    for name in ('maxItems', 'minItems'):
        if name in schema:
            attr = schema.pop(name)
            if not isinstance(attr, int):
                # should be a boolean
                raise CompilationError('{} must be a integer'.format(name), schema)  # noqa
            if attr < 0:
                # should be a boolean
                raise CompilationError('{} must be greater than 0'.format(name), schema)  # noqa
            attrs[{'maxItems': 'max_items',
                   'minItems': 'min_items'}.get(name, name)] = attr

    if 'uniqueItems' in schema:
        attr = schema.pop('uniqueItems')
        if not isinstance(attr, bool):
            raise CompilationError('{} must be a bool'.format(name), schema)  # noqa
        attrs['unique_items'] = attr

    for name in ('properties', 'patternProperties'):
        if name in schema:
            attr = schema.pop(name)

            if not isinstance(attr, dict):
                raise CompilationError('{} must be a dict'.format(name),
                                       schema)
            for subname, subschema in attr.items():
                attr[subname] = compile(subschema, os.path.join(pointer, name, subname),
                                        context)
            attrs[{'patternProperties': 'pattern_properties'}.get(name, name)] = attr

    for name in ('maxProperties', 'minProperties'):
        if name in schema:
            attr = schema.pop(name)
            if not isinstance(attr, integer_types):
                raise CompilationError('{} must be an integer'.format(name),
                                       schema)
            if attr < 0:
                raise CompilationError('{} must be greater than 0'.format(name),  # noqa
                                       schema)
            attrs[{'maxProperties': 'max_properties',
                   'minProperties': 'min_properties'}.get(name, name)] = attr

    if 'additionalProperties' in schema:
        attr = schema.pop('additionalProperties')
        if isinstance(attr, dict):
            attr = compile(attr, os.path.join(pointer, name), context)
        elif attr is True:
            attr = compile({}, os.path.join(pointer, name), context)
        elif not isinstance(attr, bool):
            raise CompilationError('additionalProperties must be '
                                   'a dict or a bool', schema)
        attrs['additional_properties'] = attr

    if 'required' in schema:
        attrs['required'] = schema.pop('required')

    if 'multipleOf' in schema:
        attr = schema.pop('multipleOf')
        if not isinstance(attr, (int, float)):
            raise CompilationError('multipleOf must be a number', schema)
        if attr < 0:
            raise CompilationError('multipleOf must be greater than 0',
                                   schema)
        attrs['multiple_of'] = attr

    if 'minimum' in schema:
        attr = schema.pop('minimum')
        if not isinstance(attr, (int, float)):
            raise CompilationError('minimum must be a number', schema)
        attrs['minimum'] = attr
    if 'exclusiveMinimum' in schema:
        attr = schema.pop('exclusiveMinimum')
        if not isinstance(attr, bool):
            raise CompilationError('exclusiveMinimum must be a boolean',
                                   schema)
        if 'minimum' not in attrs:
            raise CompilationError('exclusiveMinimum reclame maximum',
                                   schema)
        attrs['exclusive_minimum'] = attr

    if 'maximum' in schema:
        attr = schema.pop('maximum')
        if not isinstance(attr, (int, float)):
            raise CompilationError('maximum must be a number', schema)
        attrs['maximum'] = attr
    if 'exclusiveMaximum' in schema:
        attr = schema.pop('exclusiveMaximum')
        if not isinstance(attr, bool):
            raise CompilationError('exclusiveMaximum must be a boolean',
                                   schema)
        if 'maximum' not in attrs:
            raise CompilationError('exclusiveMaximum reclame maximum',
                                   schema)
        attrs['exclusive_maximum'] = attr

    if 'maxLength' in schema:
        attr = schema.pop('maxLength')
        if not isinstance(attr, int):
            raise CompilationError('maxLength must be an integer', schema)
        if attr < 0:
            raise CompilationError('maxLength must be equal '
                                   'or greater than 0', schema)
        attrs['max_length'] = attr

    if 'minLength' in schema:
        attr = schema.pop('minLength')
        if not isinstance(attr, int):
            raise CompilationError('minLength must be an integer', schema)
        if attr < 0:
            raise CompilationError('minLength must be equal '
                                   'or greater than 0', schema)
        attrs['min_length'] = attr

    for name in ('pattern', 'format'):
        if name in schema:
            attr = schema.pop(name)
            if not isinstance(attr, string_types):
                raise CompilationError('{} must be a string'.format(name), schema)
            attrs[name] = attr

    if not attrs['type']:
        t = ['null', 'boolean', 'number', 'string', 'array', 'object']
    elif isinstance(attrs['type'], list):
        t = attrs['type']
    else:
        t = [attrs['type']]

    validators = set()
    for s in t:
        validator = {
            'null': NullValidator,
            'boolean': BooleanValidator,
            'number': NumberValidator,
            'integer': IntegerValidator,
            'string': StringValidator,
            'array': ArrayValidator,
            'object': ObjectValidator,
        }[s](**attrs)
        validators.add(validator)
    if len(validators) == 1:
        return validators.pop()
    if validators:
        return AnyValidator(validators, **attrs)
