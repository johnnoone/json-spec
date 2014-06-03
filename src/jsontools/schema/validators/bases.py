"""
    jsontools.schema.validators.bases
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""

from __future__ import absolute_import, print_function, unicode_literals

__all__ = ['factory', 'CompoundValidator', 'Validator']

from abc import ABCMeta, abstractmethod
from copy import deepcopy
import logging
import os.path

from six import add_metaclass
from jsontools.exceptions import CompilationError, ValidationError

logger = logging.getLogger(__name__)
registry = {}


class EMPTY(object): pass


def factory(schema, uri, loader=None):
    spec = schema.get('$schema', 'http://json-schema.org/draft-04/schema#')
    if spec != 'http://json-schema.org/draft-04/schema#':
        raise CompilationError('can parse draft-04 only', schema)

    loader = loader or {}
    loader[uri] = deepcopy(schema)

    if '$ref' in schema:
        return ReferenceValidator(schema['$ref'], loader)

    if 'type' in schema:
        t = schema['type']
        if isinstance(t, dict):
            schema.update(t)
            del schema['type']

    if 'type' in schema:
        if isinstance(schema['type'], str):
            # direct schema
            return registry[schema['type']].compile(schema, uri, loader)
        elif isinstance(schema['type'], list):
            # multi schema
            return CompoundValidator(registry[t].compile(schema, uri, loader) for t in schema['type'])
    elif isinstance(schema, dict):
        return Validator(**Validator.compile(schema, uri, loader=loader))

    # not implemented yet
    logger.error('what the fuck %s', schema)


class ValidatorBase(ABCMeta):
    def __new__(cls, clsname, bases, attrs):
        proto = super(ValidatorBase, cls).__new__(cls, clsname, bases, attrs)
        if getattr(proto, 'type', None):
            registry[proto.type] = proto
        return proto


@add_metaclass(ValidatorBase)
class Validator(object):
    def __init__(self, **attrs):
        if 'id' in attrs:
            logger.info('id is not implemented')
        self.uri = attrs.pop('uri', None)
        self.title = attrs.pop('title', None)
        self.description = attrs.pop('description', None)
        self.default = attrs.pop('default', None)
        self.enum = attrs.pop('enum', [])
        self.opposite = attrs.pop('not', None)
        self.allOf = attrs.pop('allOf', [])
        self.anyOf = attrs.pop('anyOf', [])
        self.oneOf = attrs.pop('oneOf', [])

    @classmethod
    def compile(cls, schema, uri, loader):
        """Compile the current schema"""
        attrs = {}
        attrs['title'] = schema.get('title', None)
        attrs['description'] = schema.get('description', None)
        attrs['default'] = schema.get('default', EMPTY)
        attrs['uri'] = uri
        if 'enum' in schema:
            if not isinstance(enum, list):
                raise CompilationError('enum must be a list', schema)
            attrs['enum'] = schema['enum']
        if 'not' in schema:
            if not isinstance(enum, dict):
                raise CompilationError('not must be a dict', schema)
            attrs['not'] = factory(schema['not'], os.path.join(uri, 'not'), loader)
        for name in ('allOf', 'anyOf', 'oneOf'):
            if name in schema:
                attr = schema[name]
                if not isinstance(attr, list):
                    raise CompilationError('{} must be a list'.format(name), schema)
                sub_uri = os.path.join(uri, name)
                attr = []
                for element in attr:
                    element.setdefault('type', schema['type'])
                    attr.append(factory(element, sub_uri, loader))
                attrs[name] = attr
        return attrs

    def has_default(self):
        return self.default != EMPTY

    def validate(self, obj):
        self.validate_enum(obj)
        self.validate_opposite(obj)
        self.validate_all_of(obj)
        self.validate_any_of(obj)
        self.validate_one_of(obj)

    def validate_enum(self, obj):
        if self.enum and obj not in self.enum:
            raise ValidationError('obj is not allowed', obj)

    def validate_opposite(self, obj):
        if self.opposite:
            try:
                self.opposite.validate(obj)
            except ValidationError:
                pass
            else:
                raise ValidationError('obj is not allowed', obj)

    def validate_all_of(self, obj):
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

    def validate_any_of(self, obj):
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

    def validate_one_of(self, obj):
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


class ReferenceValidator(Validator):
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
            self._validator = factory(fragment, self.uri, self.loader)

        return self._validator

    def has_default(self):
        return self.validator.has_default()

    @property
    def default(self):
        return self.validator.default

    @classmethod
    def compile(cls, schema, uri, loader):
        raise RuntimeError('Not necessary here')

    def validate(self, obj):
        return self.validator.validate(obj)


class CompoundValidator(Validator):
    def __init__(self, **attrs):
        super().__init__(**attrs)
        self.validators = attrs.pop('validators', [])

    @classmethod
    def compile(cls, validators, uri, loader):
        return cls(validators)

    def validate(self, obj):
        errors = []
        for validator in self.validators:
            try:
                return validator.validate(obj)
            except ValidationError as error:
                errors.append(error)

        if errors:
            raise ValidationError(errors)
        return obj
