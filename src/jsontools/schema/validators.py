
from abc import ABCMeta, abstractmethod
from itertools import chain
import logging
import os.path
import re

from jsontools.exceptions import SchemaError, ValidationError

logger = logging.getLogger(__name__)

registry = {}

def factory(schema, uri):
    spec = schema.get('$schema', 'http://json-schema.org/draft-04/schema#')
    if spec != 'http://json-schema.org/draft-04/schema#':
        raise SchemaError('can parse draft-04 only', dataset)

    if 'type' in schema:
        if isinstance(schema['type'], str):
            # direct schema
            try:
                return registry[schema['type']].compile(schema, uri)
            except KeyError:
                raise SchemaError('type {} is not defined'.format(schema['type']), schema)
        else:
            # multi schema
            raise NotImplementedError
    else:
        # not implemented yet
        pass


class ValidatorBase(ABCMeta):
    def __new__(cls, clsname, bases, attrs):
        newclass = super(ValidatorBase, cls).__new__(cls, clsname, bases, attrs)
        if getattr(newclass, 'type', None):
            registry[newclass.type] = newclass
        return newclass


class Validator(metaclass=ValidatorBase):

    @classmethod
    @abstractmethod
    def compile(cls, dataset, uri):
        """Compile the current schema"""
        raise NotImplementedError()

    @abstractmethod
    def validate(self, obj):
        pass


class ObjectValidator(Validator):
    type = 'object'

    def __init__(self, **attrs):
        self.properties = attrs.pop('properties', {})
        self.required = attrs.pop('required', [])

        if attrs:
            logger.warn('some of attrs are not mapped %s', attrs.keys())

    @classmethod
    def compile(cls, schema, uri):
        attrs, meta = {}, {}
        schema = schema.copy()

        meta['title'] = schema.pop('title', None)
        meta['description'] = schema.pop('description', None)
        meta['uri'] = uri

        if schema.pop('type', 'object') != 'object':
            raise SchemaError('type must be an object', schema)

        properties = {}
        for name, subschema in schema.pop('properties', {}).items():
            try:
                properties[name] = factory(subschema, os.path.join(uri, name))
            except NotImplementedError:
                raise
        attrs['required'] = schema.pop('required', [])

        if schema:
            raise Exception('Not implemented {}'.format(schema.keys()))

        attrs['properties'] = properties
        attrs['properties'] = properties
        attrs['properties'] = properties
        return cls(**attrs)

    def validate(self, obj):
        if not isinstance(obj, dict):
            yield ValidationError('object must be a dict', '/')
            raise StopIteration

        for member in self.required:
            if member not in obj:
                yield ValidationError('{!r} is required'.format(member), '/')

        for member, value in obj.items():
            if member in self.properties:
                for error in self.properties[member].validate(value):
                    yield error


class ArrayValidator(Validator):
    type = 'array'

    def __init__(self, **attrs):
        self.items = attrs.pop('items', {})
        self.additionalItems = attrs.pop('additionalItems', {})
        self.maxItems = attrs.pop('maxItems', None)
        self.minItems = attrs.pop('minItems', 0)
        self.uniqueItems = attrs.pop('uniqueItems', None)

        if attrs:
            logger.warn('some of attrs are not mapped %s', attrs.keys())

    @classmethod
    def compile(cls, schema, uri):
        attrs, meta = {}, {}
        schema = schema.copy()
        meta['title'] = schema.pop('title', None)
        meta['description'] = schema.pop('description', None)
        meta['uri'] = uri

        for name in ('items', 'additionalItems'):
            if name in schema:
                attr = schema[name]
                if isinstance(attr, list):
                    # each value must be a json schema
                    attr = [factory(attr, os.path.join(uri, name)) for element in attr]
                elif isinstance(attr, dict):
                    # value must be a json schema
                    attr = factory(attr, os.path.join(uri, name))
                elif not isinstance(attr, bool):
                    # should be a boolean
                    raise SchemaError('wrong type for {}'.format(name), schema)

                attrs[name] = attr

        for name in ('maxItems', 'minItems'):
            if name in schema:
                attr = schema[name]
                if not isinstance(attr, int):
                    # should be a boolean
                    raise SchemaError('{} must be a integer'.format(name), schema)
                if attr < 0:
                    # should be a boolean
                    raise SchemaError('{} must be greater than 0'.format(name), schema)
                attrs[name] = attr

        if 'uniqueItems' in schema:
            attr = schema['uniqueItems']
            if not isinstance(attr, bool):
                raise SchemaError('{} must be a bool'.format(name), schema)
            attrs[name] = attr

        return cls(**attrs)

    def validate(self, obj):
        self.validate_type(obj)
        self.validate_items(obj)

    def validate_type(self, obj):
        if not isinstance(obj, list):
            raise ValidationError('object must be a list')

    def validate_items(self, obj):
        if self.items == {}:
            # validation of the instance always succeeds, regardless of the value of "additionalItems"
            return
        if self.additionalItems in (True, {}):
            # validation of the instance always succeeds
            return

        schemas = []
        
        print(isinstance(self.items, list), len(obj))
        if isinstance(self.items, list) and len(obj) > len(self.items):
            if not self.additionalItems:
                raise ValidationError('obj has to much elements. max is {}'.format(len(self.items)))

        raise NotImplementedError


class NumberValidator(Validator):
    type = 'number'

    def __init__(self, **attrs):
        self.minimum = attrs.pop('minimum', None)
        self.maximum = attrs.pop('maximum', None)
        self.exclusiveMinimum = attrs.pop('exclusiveMinimum', False)
        self.exclusiveMaximum = attrs.pop('exclusiveMaximum', False)
        self.multipleOf = attrs.pop('multipleOf', None)

        if attrs:
            logger.warn('some of attrs are not mapped %s', attrs.keys())

    @classmethod
    def compile(cls, schema, uri):
        attrs, meta = {}, {}
        meta['title'] = schema.pop('title', None)
        meta['description'] = schema.pop('description', None)
        meta['uri'] = uri

        if 'multipleOf' in schema:
            attr = schema['multipleOf']
            if not isinstance(attr, (int, float)):
                raise SchemaError('multipleOf must be a number', schema)
            if attr < 0:
                raise SchemaError('multipleOf must be greater than 0', schema)
            attrs['multipleOf'] = attr

        if 'minimum' in schema:
            attr = schema['minimum']
            if not isinstance(attr, (int, float)):
                raise SchemaError('minimum must be a number', schema)
            attrs['minimum'] = attr
        if 'exclusiveMinimum' in schema:
            attr = schema['exclusiveMinimum']
            if not isinstance(attr, bool):
                raise SchemaError('exclusiveMinimum must be a boolean', schema)
            if 'minimum' not in schema:
                raise SchemaError('exclusiveMinimum reclame maximum', schema)
            attrs['exclusiveMinimum'] = attr

        if 'maximum' in schema:
            attr = schema['maximum']
            if not isinstance(attr, (int, float)):
                raise SchemaError('maximum must be a number', schema)
            attrs['maximum'] = attr
        if 'exclusiveMaximum' in schema:
            attr = schema['exclusiveMaximum']
            if not isinstance(attr, bool):
                raise SchemaError('exclusiveMaximum must be a boolean', schema)
            if 'maximum' not in schema:
                raise SchemaError('exclusiveMaximum reclame maximum', schema)
            attrs['exclusiveMaximum'] = attr

        return cls(**attrs)

    def validate(self, obj):
        self.validate_type(obj)
        self.validate_minimum(obj)
        self.validate_maximum(obj)
        self.validate_multiple(obj)

    def validate_type(self, obj):
        if not isinstance(obj, (int, float)):
            raise ValidationError('object must be a number')
        if isinstance(obj, bool):
            raise ValidationError('obj must be an int', obj)

    def validate_minimum(self, obj):
        if self.minimum is not None:
            if not obj >= self.minimum:
                raise ValidationError('object must be greater than {}'.format(self.minimum))
            if self.exclusiveMinimum and obj == self.minimum:
                raise ValidationError('object must be greater than {}'.format(self.minimum))

    def validate_maximum(self, obj):
        if self.maximum is not None:
            if not obj <= self.maximum:
                raise ValidationError('object must be lesser than {}'.format(self.maximum))
            if self.exclusiveMaximum and obj == self.maximum:
                raise ValidationError('object must be lesser than {}'.format(self.maximum))

    def validate_multiple(self, obj):
        if self.multipleOf and not obj % self.multipleOf == 0:
            raise ValidationError('object must be a multiple of {}'.format(self.multipleOf))


class IntegerValidator(NumberValidator):
    type = 'integer'

    def validate_type(self, obj):
        if not isinstance(obj, int):
            raise ValidationError('obj must be an int', obj)
        if isinstance(obj, bool):
            raise ValidationError('obj must be an int', obj)


class StringValidator(Validator):
    type = 'string'

    def __init__(self, **attrs):
        self.maxLength = attrs.pop('maxLength', None)
        self.minLength = attrs.pop('minLength', None)
        self.pattern = attrs.pop('pattern', None)

        if attrs:
            logger.warn('some of attrs are not mapped %s', attrs.keys())

    @classmethod
    def compile(cls, schema, uri):
        attrs, meta = {}, {}
        schema = schema.copy()
        meta['title'] = schema.pop('title', None)
        meta['description'] = schema.pop('description', None)
        meta['uri'] = uri

        if 'maxLength' in schema:
            attr = 'maxLength'
            if not isinstance(attr, int):
                raise SchemaError('maxLength must be an integer', schema)
            if attr < 0:
                raise SchemaError('maxLength must be equal or greater than 0', schema)
            attrs['maxLength'] = attr

        if 'minLength' in schema:
            attr = 'minLength'
            if not isinstance(attr, int):
                raise SchemaError('minLength must be an integer', schema)
            if attr < 0:
                raise SchemaError('minLength must be equal or greater than 0', schema)
            attrs['minLength'] = attr

        if 'pattern' in schema:
            attr = 'pattern'
            if not isinstance(attr, str):
                raise SchemaError('pattern must be an integer', schema)
            attrs['pattern'] = attr

        return cls(**attrs)

    def validate(self, obj):
        self.validate_type(obj)
        self.validate_length(obj)
        self.validate_pattern(obj)

    def validate_type(self, obj):
        if not isinstance(obj, str):
            raise ValidationError('obj must be a string', obj)

    def validate_length(self, obj):
        l = len(obj)
        if self.minLength and l < self.minLength:
            raise ValidationError('length of obj must be greater or equal'
                                   ' than {}'.format(self.minLength))
        if self.maxLength and l > self.maxLength:
            raise ValidationError('length of obj must be lesser or equal'
                                   ' than {}'.format(self.minLength))

    def validate_pattern(self, obj):
        if self.pattern and not self.regex.match(obj):
            raise ValidationError('obj does not validate {!r} pattern'.format(self.pattern))

    @property
    def regex(self):
        if not hasattr(self, '_regex'):
            setattr(self, '_regex', re.compile(self.pattern))
        return self._regex
