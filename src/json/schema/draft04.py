"""
    json.schema.draft04
    ~~~~~~~~~~~~~~~~~~~

    Implementation of JSON Schema draft04.

"""

from __future__ import absolute_import, print_function, unicode_literals

__all__ = ['compile', 'Validator']

from copy import deepcopy
import itertools
import logging
import os.path
import re

from six import integer_types, string_types, binary_type, PY2

from .exceptions import CompilationError, ValidationError
from .bases import BaseValidator
from .util import rfc3339_to_datetime

logger = logging.getLogger(__name__)


def absolute(src, dest):
    if not dest.startswith('#'):
        return dest

    a, _, b = src.partition('#')
    c, _, d = dest.partition('#')
    if not c:
        return '{}#{}'.format(a, d)
    return dest


def compile(schema, uri, loader):
    """
    Compile python object into a Validator instance.
    """

    if '$ref' in schema:
        return ReferenceValidator(absolute(uri, schema['$ref']), loader)

    schema = deepcopy(schema)
    attrs = {}
    attrs['title'] = schema.get('title', None)
    attrs['description'] = schema.get('description', None)
    if 'default' in schema:
        attrs['default'] = schema.get('default')
    attrs['uri'] = uri
    attrs['type'] = schema.get('type', None)

    if 'enum' in schema:
        attr = schema['enum']
        if not isinstance(attr, list):
            raise CompilationError('enum must be a list', schema)
        attrs['enum'] = attr

    if 'not' in schema:
        attr = schema['not']
        if not isinstance(attr, dict):
            raise CompilationError('not must be a dict', schema)
        attrs['not'] = compile(attr, os.path.join(uri, 'not'), loader)
    for name in ('allOf', 'anyOf', 'oneOf'):
        if name in schema:
            attr = schema[name]
            if not isinstance(attr, list):
                raise CompilationError('{} must be a list'.format(name),
                                       schema)
            sub_uri = os.path.join(uri, name)
            for i, element in enumerate(attr):
                attr[i] = compile(element, sub_uri, loader)
            attrs[name] = attr

    for name in ('items', 'additionalItems'):
        if name not in schema:
            continue

        attr = schema[name]
        sub_uri = os.path.join(uri, name)
        if isinstance(attr, list):
            # each value must be a json schema
            attr = [compile(attr, sub_uri, loader) for element in attr]
        elif isinstance(attr, dict):
            # value must be a json schema
            attr = compile(attr, sub_uri, loader)
        elif not isinstance(attr, bool):
            # should be a boolean
            raise CompilationError('wrong type for {}'.format(name), schema)  # noqa

        attrs[name] = attr

    for name in ('maxItems', 'minItems'):
        if name not in schema:
            continue
        attr = schema[name]
        if not isinstance(attr, int):
            # should be a boolean
            raise CompilationError('{} must be a integer'.format(name), schema)  # noqa
        if attr < 0:
            # should be a boolean
            raise CompilationError('{} must be greater than 0'.format(name), schema)  # noqa
        attrs[name] = attr

    if 'uniqueItems' in schema:
        attr = schema['uniqueItems']
        if not isinstance(attr, bool):
            raise CompilationError('{} must be a bool'.format(name), schema)  # noqa
        attrs[name] = attr

    for name in ('maxProperties', 'minProperties'):
        if name in schema:
            attr = schema[name]
            attrs[name] = attr

    for name in ('properties', 'patternProperties'):
        if name in schema:
            if not isinstance(schema[name], dict):
                raise CompilationError('{} must be a dict'.format(name),
                                       schema)
            attr = {}
            for subname, subschema in schema[name].items():
                attr[subname] = compile(subschema, os.path.join(uri, name),
                                        loader)
            attrs[name] = attr

    for name in ('maxProperties', 'minProperties'):
        if name in schema:
            attr = schema[name]
            if not isinstance(attr, integer_types):
                raise CompilationError('{} must be an integer'.format(name),
                                       schema)
            if attr < 0:
                raise CompilationError('{} must be greater than 0'.format(name),  # noqa
                                       schema)
            attrs[name] = attr

    if 'additionalProperties' in schema:
        attr = schema['additionalProperties']
        if isinstance(attr, dict):
            attr = compile(attr, os.path.join(uri, name), loader)
        elif attr is True:
            attr = compile({}, os.path.join(uri, name), loader)
        elif not isinstance(schema['additionalProperties'], bool):
            raise CompilationError('additionalProperties must be '
                                   'a dict or a bool', schema)
        attrs['additionalProperties'] = attr

    if 'required' in schema:
        attrs['required'] = schema['required'][:]

    if 'multipleOf' in schema:
        attr = schema['multipleOf']
        if not isinstance(attr, (int, float)):
            raise CompilationError('multipleOf must be a number', schema)
        if attr < 0:
            raise CompilationError('multipleOf must be greater than 0',
                                   schema)
        attrs['multipleOf'] = attr

    if 'minimum' in schema:
        attr = schema['minimum']
        if not isinstance(attr, (int, float)):
            raise CompilationError('minimum must be a number', schema)
        attrs['minimum'] = attr
    if 'exclusiveMinimum' in schema:
        attr = schema['exclusiveMinimum']
        if not isinstance(attr, bool):
            raise CompilationError('exclusiveMinimum must be a boolean',
                                   schema)
        if 'minimum' not in schema:
            raise CompilationError('exclusiveMinimum reclame maximum',
                                   schema)
        attrs['exclusiveMinimum'] = attr

    if 'maximum' in schema:
        attr = schema['maximum']
        if not isinstance(attr, (int, float)):
            raise CompilationError('maximum must be a number', schema)
        attrs['maximum'] = attr
    if 'exclusiveMaximum' in schema:
        attr = schema['exclusiveMaximum']
        if not isinstance(attr, bool):
            raise CompilationError('exclusiveMaximum must be a boolean',
                                   schema)
        if 'maximum' not in schema:
            raise CompilationError('exclusiveMaximum reclame maximum',
                                   schema)
        attrs['exclusiveMaximum'] = attr

    if 'maxLength' in schema:
        attr = 'maxLength'
        if not isinstance(attr, int):
            raise CompilationError('maxLength must be an integer', schema)
        if attr < 0:
            raise CompilationError('maxLength must be equal '
                                   'or greater than 0', schema)
        attrs['maxLength'] = attr

    if 'minLength' in schema:
        attr = 'minLength'
        if not isinstance(attr, int):
            raise CompilationError('minLength must be an integer', schema)
        if attr < 0:
            raise CompilationError('minLength must be equal '
                                   'or greater than 0', schema)
        attrs['minLength'] = attr

    for name in ('pattern', 'format'):
        if name in schema:
            attr = schema[name]
            if not isinstance(attr, string_types):
                raise CompilationError('{} must be a string'.format(name), schema)
            attrs[name] = attr

    return Validator(**attrs)


class Items(object):
    """
    Describes items and additionalItems rules
    """

    def __init__(self, key):
        self.key = key

    def __get__(self, obj, type=None):
        iterable = getattr(obj, self.key, [])
        if isinstance(iterable, Validator):
            return itertools.cycle([iterable])
        if not iterable:
            return []
        return iterable

    def __set__(self, obj, value):
        setattr(obj, self.key, value)


class Validator(BaseValidator):
    """
    Implements a draft04 validator.
    """

    items = Items('_items')
    additionalItems = Items('_additionalItems')

    def __init__(self, **attrs):
        self.id = attrs.pop('id', None)
        if self.id:
            logger.info('id is not implemented and is here for information purpose')
        self.uri = attrs.pop('uri', None)
        self.title = attrs.pop('title', None)
        self.description = attrs.pop('description', None)
        self.type = attrs.pop('type', None)
        self.default = attrs.pop('default', None)
        self.enum = attrs.pop('enum', [])
        self.negate = attrs.pop('not', None)
        self.allOf = attrs.pop('allOf', [])
        self.anyOf = attrs.pop('anyOf', [])
        self.oneOf = attrs.pop('oneOf', [])

        self.initialize_array(attrs)
        self.initialize_object(attrs)
        self.initialize_number(attrs)
        self.initialize_string(attrs)

    def initialize_array(self, attrs):
        self.items = attrs.pop('items', {})
        self.additionalItems = attrs.pop('additionalItems', False)
        self.maxItems = attrs.pop('maxItems', None)
        self.minItems = attrs.pop('minItems', 0)
        self.uniqueItems = attrs.pop('uniqueItems', None)

    def initialize_object(self, attrs):
        self.properties = attrs.pop('properties', {})
        self.patternProperties = attrs.pop('patternProperties', {})
        self.additionalProperties = attrs.pop('additionalProperties', {})
        self.maxProperties = attrs.pop('maxProperties', None)
        self.minProperties = attrs.pop('minProperties', None)
        self.required = attrs.pop('required', [])

    def initialize_number(self, attrs):
        self.minimum = attrs.pop('minimum', None)
        self.maximum = attrs.pop('maximum', None)
        self.exclusiveMinimum = attrs.pop('exclusiveMinimum', False)
        self.exclusiveMaximum = attrs.pop('exclusiveMaximum', False)
        self.multipleOf = attrs.pop('multipleOf', None)

    def initialize_string(self, attrs):
        self.maxLength = attrs.pop('maxLength', None)
        self.minLength = attrs.pop('minLength', None)
        self.pattern = attrs.pop('pattern', None)
        self.format = attrs.pop('format', None)

    def has_default(self):
        return getattr(self, 'default', False)

    def has_type(self, type):
        return self.type and (self.type == type or type in self.type)

    def validate(self, obj):
        """
        Validates obj.

        Note that the returned object is not the same as object.
        It may contains default values.

        :param obj: The object to validate
        :return: the validated obj
        :raises ValidationError: Whole or part of obj does not validate.
        """

        # common
        self.validate_enum(obj)
        self.validate_negate(obj)
        self.validate_and(obj)
        self.validate_or(obj)
        self.validate_xor(obj)

        # primitives
        if self.validate_array(obj):
            obj = self.validate_items(obj)

        if self.validate_boolean(obj):
            pass

        if self.validate_integer(obj):
            self.validate_minimum(obj)
            self.validate_maximum(obj)
            self.validate_multiple(obj)

        if self.validate_null(obj):
            pass

        if self.validate_number(obj):
            self.validate_minimum(obj)
            self.validate_maximum(obj)
            self.validate_multiple(obj)

        if self.validate_object(obj):
            obj = self.validate_properties(obj)

        if self.validate_string(obj):
            self.validate_length(obj)
            self.validate_pattern(obj)
            self.validate_format(obj)

        return obj

    def validate_enum(self, obj):
        if self.enum and obj not in self.enum:
            raise ValidationError('obj is not allowed', obj, rule=self.uri)

    def validate_array(self, obj):
        if isinstance(obj, list):
            return True
        elif self.has_type('array'):
            raise ValidationError('obj must be an array', obj, rule=self.uri)
        return False

    def validate_boolean(self, obj):
        if obj in (True, False):
            return True
        elif self.has_type('boolean'):
            raise ValidationError('obj must be a boolean', obj, rule=self.uri)
        return False

    def validate_integer(self, obj):
        if isinstance(obj, integer_types) and not isinstance(obj, bool):
            return True
        elif self.has_type('integer'):
            raise ValidationError('obj must be an integer', obj, rule=self.uri)
        return False

    def validate_null(self, obj):
        if obj is None:
            return True
        elif self.has_type('null'):
            raise ValidationError('obj must be null', obj, rule=self.uri)
        return False

    def validate_number(self, obj):
        if isinstance(obj, (integer_types, float)) and not isinstance(obj, bool):  # noqa
            return True
        elif self.has_type('number'):
            raise ValidationError('obj must be a number', obj, rule=self.uri)
        return False

    def validate_object(self, obj):
        if isinstance(obj, dict):
            return True
        elif self.has_type('object'):
            raise ValidationError('obj must be an object', obj, rule=self.uri)
        return False

    def validate_string(self, obj):
        if isinstance(obj, string_types):
            return True
        if PY2 and isinstance(obj, binary_type):
            return True
        elif self.has_type('string'):
            raise ValidationError('obj must be a string', obj, rule=self.uri)
        return False

    def validate_length(self, obj):
        l = len(obj)
        if self.minLength and l < self.minLength:
            raise ValidationError('length of obj must be greater or equal'
                                  ' than {}'.format(self.minLength), obj, rule=self.uri)
        if self.maxLength and l > self.maxLength:
            raise ValidationError('length of obj must be lesser or equal'
                                  ' than {}'.format(self.minLength), obj, rule=self.uri)

    def validate_pattern(self, obj):
        if self.pattern and not self.regex.match(obj):
            raise ValidationError('obj does not validate '
                                  '{!r} pattern'.format(self.pattern), obj, rule=self.uri)

    def validate_format(self, obj):
        if not self.format:
            return obj
        if self.format == 'date-time':
            return self.validate_datetime(obj)
        if self.format == 'email':
            return self.validate_email(obj)
        if self.format == 'hostname':
            return self.validate_hostname(obj)
        if self.format == 'ipv4':
            return self.validate_ipv4(obj)
        if self.format == 'ipv6':
            return self.validate_ipv6(obj)
        if self.format == 'uri':
            return self.validate_uri(obj)
        raise ValidationError('format {} is not '
                              'defined.'.format(self.pattern), obj, rule=self.uri)

    @property
    def regex(self):
        if not hasattr(self, '_regex'):
            setattr(self, '_regex', re.compile(self.pattern))
        return self._regex

    def validate_minimum(self, obj):
        if self.minimum is not None:
            if not obj >= self.minimum:
                raise ValidationError('object must be greater '
                                      'than {}'.format(self.minimum), obj, rule=self.uri)
            if self.exclusiveMinimum and obj == self.minimum:
                raise ValidationError('object must be greater '
                                      'than {}'.format(self.minimum), obj, rule=self.uri)

    def validate_maximum(self, obj):
        if self.maximum is not None:
            if not obj <= self.maximum:
                raise ValidationError('object must be lesser '
                                      'than {}'.format(self.maximum), obj, rule=self.uri)
            if self.exclusiveMaximum and obj == self.maximum:
                raise ValidationError('object must be lesser '
                                      'than {}'.format(self.maximum), obj, rule=self.uri)

    def validate_multiple(self, obj):
        if self.multipleOf and not obj % self.multipleOf == 0:
            raise ValidationError('object must be a multiple '
                                  'of {}'.format(self.multipleOf), obj, rule=self.uri)

    def validate_items(self, obj):
        l = len(obj)
        if self.minItems and l < self.minItems:
            raise ValidationError('object must have at least '
                                  '{} elements'.format(self.minItems), obj, rule=self.uri)
        if self.maxItems and l > self.maxItems:
            raise ValidationError('object must have less than '
                                  '{} elements'.format(self.maxItems), obj, rule=self.uri)

        if self._items == {}:
            # validation of the instance always succeeds
            # regardless of the value of "additionalItems"
            return obj
        if self._additionalItems in (True, {}):
            # validation of the instance always succeeds
            return obj

        schemas = itertools.chain(self.items, self.additionalItems)
        iteration = 0
        errors = []
        for sub, schema in zip(obj, schemas):
            iteration += 1
            try:
                if schema == {}:
                    continue
                else:
                    schema.validate(sub)
            except ValidationError as error:
                errors.append(error)
        if errors:
            raise ValidationError(errors)

        if iteration < len(obj):
            raise ValidationError('object has too much elements', obj, rule=self.uri)

        if self.uniqueItems and len(set(obj)) != len(obj):
            raise ValidationError('items must be unique', obj, rule=self.uri)

        return obj

    def validate_properties(self, obj):
        l = len(obj)
        if isinstance(self.maxProperties, integer_types) and l > self.maxProperties:  # noqa
            raise ValidationError('too much properties, '
                                  'max {}'.format(self.maxProperties), obj, rule=self.uri)
        if isinstance(self.minProperties, integer_types) and l < self.minProperties:  # noqa
            raise ValidationError('too few properties, '
                                  'min {}'.format(self.minProperties), obj, rule=self.uri)

        obj = deepcopy(obj)
        errors, missing = [], set(obj.keys())
        missing.update(self.required)
        missing.update(self.properties.keys())
        for member, schema in self.properties.items():
            if member in obj:
                try:
                    schema.validate(obj[member])
                    missing.discard(member)
                except ValidationError as error:
                    errors.append(error)
                except AttributeError:
                    raise
            elif schema.has_default():
                obj[member] = deepcopy(schema.default)
        if errors:
            raise ValidationError(errors)
        for pattern, schema in self.patternProperties.items():
            regex = re.compile(pattern)
            for member, value in obj.items():
                if regex.match(member):
                    try:
                        schema.validate(value)
                        missing.discard(member)
                    except ValidationError as error:
                        errors.append(error)
        if errors:
            raise ValidationError(errors)

        if missing:
            if self.additionalProperties in ({}, True):
                missing.clear()
            elif self.additionalProperties:
                schema = self.additionalProperties
                for member in missing:
                    try:
                        obj[member] = schema.validate(obj[member])
                        missing.discard(member)
                    except ValidationError as error:
                        errors.append(error)
        for member in self.required:
            if member not in obj:
                missing.add(member)
        if errors:
            raise ValidationError(errors, obj, rule=self.uri)

        if missing:
            raise ValidationError('missing definitions for {}'.format(missing), obj, rule=self.uri)

        return obj

    def validate_negate(self, obj):
        if self.negate:
            try:
                self.negate.validate(obj)
            except ValidationError:
                pass
            else:
                raise ValidationError('obj is not allowed', obj, rule=self.uri)

    def validate_and(self, obj):
        if self.allOf:
            errors = []
            for validator in self.allOf:
                try:
                    validator.validate(obj)
                except ValidationError as error:
                    errors.append(error)
            if errors:
                raise ValidationError(errors)
        return obj

    def validate_or(self, obj):
        if self.anyOf:
            errors = []
            for validator in self.anyOf:
                try:
                    return validator.validate(obj)
                except ValidationError as error:
                    errors.append(error)
            if errors:
                raise ValidationError(errors)
        return obj

    def validate_xor(self, obj):
        if self.oneOf:
            ok, errors = [], []
            for validator in self.oneOf:
                try:
                    ok.append(validator.validate(obj))
                except ValidationError as error:
                    errors.append(error)
            if len(ok) == 1:
                return ok.pop()
            if errors:
                raise ValidationError(errors)
        return obj

    def validate_datetime(self, obj):
        try:
            return rfc3339_to_datetime(obj)
        except ValueError:
            raise ValidationError('{!r} is not a valid datetime'.format(obj), obj, rule=self.uri)

    def validate_email(self, obj):
        pattern = re.compile('[^@]+@[^@]+\.[^@]+')
        if not pattern.match(obj):
            raise ValidationError('{!r} is not defined'.format(obj), obj, rule=self.uri)

    def validate_hostname(self, obj):
        try:
            host = deepcopy(obj)
            if len(host) > 255:
                raise ValueError
            if host[-1] == ".":
                host = host[:-1] # strip exactly one dot from the right, if present
            allowed = re.compile("(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
            if not all(allowed.match(x) for x in host.split(".")):
                raise ValueError
            return obj
        except ValueError:
            raise ValidationError('{!r} is not a valid hostname'.format(obj), obj, rule=self.uri)

    def validate_ipv4(self, obj):
        try:
            parts = obj.split('.', 3)
            for part in parts:
                part = int(part)
                if part > 127 or part < 0:
                    raise ValueError
        except ValueError:
            raise ValidationError('{!r} is not an ipv4'.format(obj), obj, rule=self.uri)

    def validate_ipv6(self, obj):
        raise ValidationError('{!r} is not defined'.format(obj), obj, rule=self.uri)

    def validate_uri(self, obj):
        raise ValidationError('{!r} is not defined'.format(obj), obj, rule=self.uri)


class ReferenceValidator(BaseValidator):
    """
    Loads lately validator.
    """

    def __init__(self, uri, loader):
        self.uri = uri
        self.loader = loader

    @property
    def validator(self):
        if not hasattr(self, '_validator'):
            doc, _, pointer = self.uri.partition('#')
            doc = doc or '<document>'

            fragment = self.loader.get('{}#'.format(doc))
            pointer = pointer.lstrip('/')
            while pointer:
                member, _, pointer = pointer.partition('/')
                fragment = fragment[member]
            self._validator = compile(fragment, self.uri, self.loader)

        return self._validator

    def has_default(self):
        return self.validator.has_default()

    @property
    def default(self):
        return self.validator.default

    def validate(self, obj):
        return self.validator.validate(obj)
