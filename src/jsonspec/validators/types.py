"""
    jsonspec.validators.types
    ~~~~~~~~~~~~~~~~~~~~~~~~~

"""


__all__ = ['EnumValidator', 'StringValidator', 'NumberValidator',
           'IntegerValidator', 'BooleanValidator', 'NullValidator',
           'ArrayValidator', 'ObjectValidator']

from abc import abstractmethod
from copy import deepcopy
from six import integer_types
from six import string_types

import itertools
import logging
import pkg_resources
import re

from .bases import error, Validator
from .collections import Items
from .exceptions import ValidationError

logger = logging.getLogger(__name__)


class DataValidator(Validator):
    """Common validator
    """
    def __init__(self, **attrs):
        self.uri = attrs.pop('uri', None)
        self.title = attrs.pop('title', None)
        self.description = attrs.pop('description', None)
        if 'id' in attrs:
            self.id = attrs.pop('id')
            logger.info('id is not implemented and is '
                        'here for information purpose')


class EnumValidator(DataValidator):
    """Must match one of the values

    :ivar enum: the value set
    """
    def __init__(self, **attrs):
        super(EnumValidator, self).__init__(**attrs)
        self.enum = attrs.pop('enum', [])

    def has_default(self):
        return False

    @error
    def validate(self, obj):
        if obj not in self.enum:
            raise ValidationError('obj is not allowed')
        return deepcopy(obj)


class TypeValidator(DataValidator):
    def __init__(self, **attrs):
        super(TypeValidator, self).__init__(**attrs)
        if 'default' in attrs:
            self.default = attrs.pop('default')
        self._has_default = 'default' in attrs

    def has_default(self):
        return self._has_default

    @error
    def validate(self, obj):
        return self.validate_type(obj)

    @abstractmethod
    def validate_type(self, obj):
        """Must validate against this type"""


class StringValidator(TypeValidator):
    """Validate against string

    :ivar min_length: minimum length of obj
    :ivar max_length: maximum length of obj
    :ivar pattern: regex pattern
    :ivar format: format to validate against to
    """

    def __init__(self, **attrs):
        super(StringValidator, self).__init__(**attrs)
        self.min_length = attrs.pop('min_length', None)
        self.max_length = attrs.pop('max_length', None)
        self.pattern = attrs.pop('pattern', None)
        self.format = attrs.pop('format', None)

    @property
    def regex(self):
        if not hasattr(self, '_regex'):
            setattr(self, '_regex', re.compile(self.pattern))
        return self._regex

    @property
    def formats(self):
        """
        Formats are loaded with pkg_resources
        under `jsonspec.schema.formats` namespace
        """
        print('LOAD FORMATS')
        if not hasattr(self, '_formats'):
            data = {}
            ns = 'jsonspec.validators.formats'
            entrypoints = pkg_resources.iter_entry_points(ns)
            for entrypoint in entrypoints:
                data[entrypoint.name] = entrypoint.load()
            self._formats = data
        return self._formats

    def validate_type(self, obj):
        logger.debug('%s validates %s', self, obj)
        if not isinstance(obj, string_types):
            raise ValidationError('obj must be a string')
        obj = self.validate_length(obj)
        obj = self.validate_pattern(obj)
        obj = self.validate_format(obj)
        return obj

    def validate_length(self, obj):
        min, max, length = self.min_length, self.max_length, len(obj)
        if min is not None and length < min:
            raise ValidationError('length of obj must be greater or equal'
                                  ' than {}'.format(min))
        if max is not None and length > max:
            raise ValidationError('length of obj must be lesser or equal'
                                  ' than {}'.format(max))
        return obj

    def validate_pattern(self, obj):
        if self.pattern and not self.regex.search(obj):
            raise ValidationError('obj does not validate '
                                  '{!r} pattern'.format(self.pattern))
        return obj

    def validate_format(self, obj):
        if not self.format:
            return obj
        try:
            return self.formats[self.format](obj)
        except KeyError:
            raise ValidationError('format {} is not '
                                  'defined.'.format(self.format))


class NumberValidator(TypeValidator):
    """Validate against number

    :ivar minimum: minimum of obj
    :ivar maximum: maximum of obj
    :ivar exclusive_minimum:
    :ivar exclusive_maximum:
    :ivar multiple_of:
    """

    def __init__(self, **attrs):
        super(NumberValidator, self).__init__(**attrs)
        self.minimum = attrs.pop('minimum', None)
        self.maximum = attrs.pop('maximum', None)
        self.exclusive_minimum = attrs.pop('exclusive_minimum', False)
        self.exclusive_maximum = attrs.pop('exclusive_maximum', False)
        self.multiple_of = attrs.pop('multiple_of', None)

    def validate_type(self, obj):
        logger.debug('%s validates %s', self, obj)
        if isinstance(obj, bool):
            raise ValidationError('obj must be a number')
        elif not isinstance(obj, (integer_types, float)):
            raise ValidationError('obj must be a number')
        obj = self.validate_size(obj)
        obj = self.validate_multiple(obj)
        return obj

    def validate_size(self, obj):
        min_fail, max_fail = False, False

        if self.minimum is not None:
            if obj < self.minimum:
                min_fail = True
            elif self.exclusive_minimum and obj == self.minimum:
                min_fail = True

        if self.maximum is not None:
            if obj > self.maximum:
                max_fail = True
            elif self.exclusive_maximum and obj == self.maximum:
                max_fail = True

        if min_fail and max_fail:
            raise ValidationError('object must be between {}'
                                  'and {}'.format(self.minimum, self.maximum))
        if min_fail:
            raise ValidationError('object must be greater '
                                  'than {}'.format(self.minimum))
        if max_fail:
            raise ValidationError('object must be lesser '
                                  'than {}'.format(self.maximum))
        return obj

    def validate_multiple(self, obj):
        if self.multiple_of is not None and obj % self.multiple_of:
            raise ValidationError('object must be a multiple '
                                  'of {}'.format(self.multiple_of))
        return obj


class IntegerValidator(NumberValidator):
    """Validate against integer

    :ivar minimum: minimum of obj
    :ivar maximum: maximum of obj
    :ivar exclusive_minimum:
    :ivar exclusive_maximum:
    :ivar multiple_of:
    """

    def validate_type(self, obj):
        logger.debug('%s validates %s', self, obj)
        if not isinstance(obj, integer_types):  # noqa
            raise ValidationError('obj must be an integer')
        return super(IntegerValidator, self).validate_type(obj)


class BooleanValidator(TypeValidator):
    """Validate against boolean
    """

    def validate_type(self, obj):
        logger.debug('%s validates %s', self, obj)
        if isinstance(obj, bool):
            return obj
        raise ValidationError('obj must be a boolean')


class NullValidator(TypeValidator):
    """Validate against boolean"""

    def validate_type(self, obj):
        logger.debug('%s validates %s', self, obj)
        if obj is None:
            return obj
        raise ValidationError('obj must be a boolean')


class ArrayValidator(TypeValidator):
    """Validate against array

    :ivar min_items:
    :ivar max_items:
    :ivar items:
    :ivar additional_items:
    :ivar unique_items:
    """

    items = Items('_items')
    additionalItems = Items('_additionalItems')

    def __init__(self, **attrs):
        super(ArrayValidator, self).__init__(**attrs)
        self.min_items = attrs.pop('min_items', None)
        self.max_items = attrs.pop('max_items', None)
        self._items = attrs.pop('items', {})
        self._additional_items = attrs.pop('additional_items', {})
        self.unique_items = attrs.pop('unique_items', False)

    def validate_type(self, obj):
        logger.debug('%s validates %s', self, obj)
        if not isinstance(obj, list):
            raise ValidationError('obj must be an array')
        obj = deepcopy(obj)
        obj = self.validate_total_items(obj)
        obj = self.validate_unique_items(obj)
        obj = self.validate_items(obj)
        return obj

    def validate_total_items(self, obj):
        count = len(obj)
        if self.min_items and count < self.min_items:
            raise ValidationError('object must have at least '
                                  '{} elements'.format(self.min_items))
        if self.max_items and count > self.max_items:
            raise ValidationError('object must have less than '
                                  '{} elements'.format(self.max_items))
        return obj

    def validate_unique_items(self, obj):
        if self.unique_items and len(set(obj)) != len(obj):
            raise ValidationError('items must be unique')
        return obj

    def validate_items(self, obj):
        if self._items == {}:
            # validation of the instance always succeeds
            # regardless of the value of "additional_items"
            return obj
        if self._additional_items in (True, {}):
            # validation of the instance always succeeds
            return obj

        validators = itertools.chain(self.items, self.additional_items)
        iteration = 0
        errors = []
        for i, (sub, validator) in enumerate(zip(obj, validators)):
            iteration += 1
            try:
                if validator == {}:
                    continue
                else:
                    obj[i] = validator(sub)
            except ValidationError as error:
                errors.append(error)
        if errors:
            raise ValidationError(errors)

        if iteration < len(obj):
            raise ValidationError('object has too much elements')

        return obj


class ObjectValidator(TypeValidator):
    """Validate against object

    :ivar properties:
    :ivar pattern_properties:
    :ivar additional_properties:
    :ivar max_properties:
    :ivar min_properties:
    """

    def __init__(self, **attrs):
        super(ObjectValidator, self).__init__(**attrs)
        self.properties = attrs.pop('properties', {})
        self.pattern_properties = attrs.pop('pattern_properties', {})
        self.additional_properties = attrs.pop('additional_properties', {})
        self.max_properties = attrs.pop('max_properties', None)
        self.min_properties = attrs.pop('min_properties', None)
        self.required = attrs.pop('required', [])

    def validate_type(self, obj):
        logger.debug('%s validates %s', self, obj)
        if not isinstance(obj, dict):
            raise ValidationError('obj must be an object')
        obj = deepcopy(obj)
        obj = self.validate_total_properties(obj)
        obj = self.validate_properties(obj)
        return obj

    def validate_total_properties(self, obj):
        total = len(obj)
        logger.debug('%s total properties %s', self, total)
        if isinstance(self.max_properties, integer_types) and total > self.max_properties:  # noqa
            raise ValidationError('too much properties, '
                                  'max {}'.format(self.max_properties))
        if isinstance(self.min_properties, integer_types) and total < self.min_properties:  # noqa
            raise ValidationError('too few properties, '
                                  'min {}'.format(self.min_properties))
        return obj

    def validate_properties(self, obj):
        logger.debug('%s properties %s %s', self, obj.keys(), self.required)
        errors, missing = [], set(obj.keys())
        missing.update(self.required)
        missing.update(self.properties.keys())
        for member, validator in self.properties.items():
            if member in obj:
                try:
                    validator(obj[member])
                    missing.discard(member)
                except ValidationError as error:
                    errors.append(error)
                except AttributeError:
                    raise
            elif validator.has_default():
                obj[member] = deepcopy(validator.default)
        if errors:
            raise ValidationError(errors)
        for pattern, validator in self.pattern_properties.items():
            regex = re.compile(pattern)
            for member, value in obj.items():
                if regex.match(member):
                    try:
                        validator(value)
                        missing.discard(member)
                    except ValidationError as error:
                        errors.append(error)
        if errors:
            raise ValidationError('Properties does not validate', error=errors)

        if missing:
            if self.additional_properties in ({}, True):
                missing.clear()
            elif self.additional_properties:
                validator = self.additional_properties
                for member in missing:
                    try:
                        obj[member] = validator(obj[member])
                        missing.discard(member)
                    except ValidationError as error:
                        errors.append(error)
        for member in self.required:
            if member not in obj:
                missing.add(member)
        if errors:
            raise ValidationError('Properties does not validate', error=errors)

        if missing:
            raise ValidationError('Missing definitions for {}'.format(missing))

        return obj
