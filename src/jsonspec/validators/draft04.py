"""
    jsonspec.validators.draft04
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Implements JSON Schema draft04.
"""

__all__ = ['compile']

import json
import logging
import os.path
import re
from copy import deepcopy
from decimal import Decimal
from six import integer_types, string_types, text_type
from six.moves.urllib.parse import urljoin
from .bases import ReferenceValidator, Validator, error
from .exceptions import CompilationError
from .factorize import register
from jsonspec.validators.exceptions import ValidationError

sequence_types = (list, set, tuple)
number_types = (integer_types, float, Decimal)
logger = logging.getLogger(__name__)


@register(spec='http://json-schema.org/draft-04/schema#')
def compile(schema, pointer, context, scope=None):
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

    schm = deepcopy(schema)

    scope = urljoin(scope or str(pointer), schm.pop('id', None))

    if '$ref' in schema:
        return ReferenceValidator(urljoin(scope, schema['$ref']), context)

    attrs = {}

    if 'additionalItems' in schm:
        sub_uri = os.path.join(pointer, 'additionalItems')
        attrs['additional_items'] = schm.pop('additionalItems')
        if isinstance(attrs['additional_items'], dict):
            # value must be a json schema
            attrs['additional_items'] = compile(attrs['additional_items'], sub_uri, context, scope)
        elif not isinstance(attrs['additional_items'], bool):
            # should be a boolean
            raise CompilationError('wrong type for {}'.format('additional_items'), schema)  # noqa

    if 'additionalProperties' in schm:
        sub_uri = os.path.join(pointer, 'additionalProperties')
        attrs['additional_properties'] = schm.pop('additionalProperties')
        if isinstance(attrs['additional_properties'], dict):
            # value must be a json schema
            attrs['additional_properties'] = compile(attrs['additional_properties'], sub_uri, context, scope)
        elif not isinstance(attrs['additional_properties'], bool):
            # should be a boolean
            raise CompilationError('wrong type for {}'.format('additional_properties'), schema)  # noqa
    if 'allOf' in schm:
        sub_uri = os.path.join(pointer, 'allOf')
        attrs['all_of'] = schm.pop('allOf')
        if isinstance(attrs['all_of'], (list, tuple)):
            # each value must be a json schema
            attrs['all_of'] = [compile(element, sub_uri, context, scope) for element in attrs['all_of']]
        else:
            # should be a boolean
            raise CompilationError('wrong type for {}'.format('allOf'), schema)  # noqa
    if 'anyOf' in schm:
        sub_uri = os.path.join(pointer, 'anyOf')
        attrs['any_of'] = schm.pop('anyOf')
        if isinstance(attrs['any_of'], (list, tuple)):
            # each value must be a json schema
            attrs['any_of'] = [compile(element, sub_uri, context, scope) for element in attrs['any_of']]
        else:
            # should be a boolean
            raise CompilationError('wrong type for {}'.format('anyOf'), schema)  # noqa
    if 'default' in schm:
        attrs['default'] = schm.pop('default')
    if 'dependencies' in schm:
        attrs['dependencies'] = schm.pop('dependencies')
        if not isinstance(attrs['dependencies'], dict):
            raise CompilationError('dependencies must be an object')
        for key, value in attrs['dependencies'].items():
            if isinstance(value, dict):
                attrs['dependencies'][key] = compile(value,
                                                     os.path.join(pointer, 'dependencies', key),  # noqa
                                                     context, scope)
            elif not isinstance(value, sequence_types):
                raise CompilationError('dependencies must be an array or object', schema)
    if 'enum' in schm:
        attrs['enum'] = schm.pop('enum')
        if not isinstance(attrs['enum'], sequence_types):
            raise CompilationError('enum must be a sequence')
    if 'exclusiveMaximum' in schm:
        attrs['exclusive_maximum'] = schm.pop('exclusiveMaximum')
        if not isinstance(attrs['exclusive_maximum'], bool):
            raise CompilationError('exclusiveMaximum must be a boolean')
    if 'exclusiveMinimum' in schm:
        attrs['exclusive_minimum'] = schm.pop('exclusiveMinimum')
        if not isinstance(attrs['exclusive_minimum'], bool):
            raise CompilationError('exclusiveMinimum must be a boolean')
    if 'format' in schm:
        attrs['format'] = schm.pop('format')
        if not isinstance(attrs['format'], string_types):
            raise CompilationError('format must be a string')
    if 'items' in schm:
        sub_uri = os.path.join(pointer, 'items')
        attrs['items'] = schm.pop('items')
        if isinstance(attrs['items'], (list, tuple)):
            # each value must be a json schema
            attrs['items'] = [compile(element, sub_uri, context, scope) for element in attrs['items']]
        elif isinstance(attrs['items'], dict):
            # value must be a json schema
            attrs['items'] = compile(attrs['items'], sub_uri, context, scope)
        else:
            # should be a boolean
            raise CompilationError('wrong type for {}'.format('items'), schema)  # noqa
    if 'maximum' in schm:
        attrs['maximum'] = schm.pop('maximum')
        if not isinstance(attrs['maximum'], number_types):
            raise CompilationError('maximum must be a number')
    if 'maxItems' in schm:
        attrs['max_items'] = schm.pop('maxItems')
        if not isinstance(attrs['max_items'], integer_types):
            raise CompilationError('maxItems must be integer')
    if 'maxLength' in schm:
        attrs['max_length'] = schm.pop('maxLength')
        if not isinstance(attrs['max_length'], integer_types):
            raise CompilationError('maxLength must be integer')
    if 'maxProperties' in schm:
        attrs['max_properties'] = schm.pop('maxProperties')
        if not isinstance(attrs['max_properties'], integer_types):
            raise CompilationError('maxProperties must be integer')
    if 'minimum' in schm:
        attrs['minimum'] = schm.pop('minimum')
        if not isinstance(attrs['minimum'], number_types):
            raise CompilationError('minimum must be a number')
    if 'minItems' in schm:
        attrs['min_items'] = schm.pop('minItems')
        if not isinstance(attrs['min_items'], integer_types):
            raise CompilationError('minItems must be integer')
    if 'minLength' in schm:
        attrs['min_length'] = schm.pop('minLength')
        if not isinstance(attrs['min_length'], integer_types):
            raise CompilationError('minLength must be integer')
    if 'minProperties' in schm:
        attrs['min_properties'] = schm.pop('minProperties')
        if not isinstance(attrs['min_properties'], integer_types):
            raise CompilationError('minProperties must be integer')
    if 'multipleOf' in schm:
        attrs['multiple_of'] = schm.pop('multipleOf')
        if not isinstance(attrs['multiple_of'], number_types):
            raise CompilationError('multipleOf must be a number')
    if 'not' in schm:
        attrs['not'] = schm.pop('not')
        if not isinstance(attrs['not'], dict):
            raise CompilationError('not must be an object', schema)
        attrs['not'] = compile(attrs['not'], os.path.join(pointer, 'not'), context, scope)
    if 'oneOf' in schm:
        sub_uri = os.path.join(pointer, 'oneOf')
        attrs['one_of'] = schm.pop('oneOf')
        if isinstance(attrs['one_of'], (list, tuple)):
            # each value must be a json schema
            attrs['one_of'] = [compile(element, sub_uri, context, scope) for element in attrs['one_of']]
        else:
            # should be a boolean
            raise CompilationError('wrong type for {}'.format('oneOf'), schema)  # noqa
    if 'pattern' in schm:
        attrs['pattern'] = schm.pop('pattern')
        if not isinstance(attrs['pattern'], string_types):
            raise CompilationError('pattern must be a string')
    if 'properties' in schm:
        attrs['properties'] = schm.pop('properties')
        if not isinstance(attrs['properties'], dict):
            raise CompilationError('properties must be an object')
        for subname, subschema in attrs['properties'].items():
            attrs['properties'][subname] = compile(subschema,
                                                   os.path.join(pointer, 'properties', subname),
                                                   context, scope)
    if 'patternProperties' in schm:
        attrs['pattern_properties'] = schm.pop('patternProperties')
        if not isinstance(attrs['pattern_properties'], dict):
            raise CompilationError('patternProperties must be an object')
        for subname, subschema in attrs['pattern_properties'].items():
            attrs['pattern_properties'][subname] = compile(subschema,
                                                   os.path.join(pointer, 'patternProperties', subname),
                                                   context, scope)
    if 'required' in schm:
        attrs['required'] = schm.pop('required')
        if not isinstance(attrs['required'], list):
            raise CompilationError('required must be a list')
        if len(attrs['required']) < 1:
            raise CompilationError('required cannot be empty')
    if 'type' in schm:
        attrs['type'] = schm.pop('type')
        if isinstance(attrs['type'], string_types):
            attrs['type'] = [attrs['type']]
        elif not isinstance(attrs['type'], sequence_types):
            raise CompilationError('type must be string or sequence')
    if 'uniqueItems' in schm:
        attrs['unique_items'] = schm.pop('uniqueItems')
        if not isinstance(attrs['unique_items'], bool):
            raise CompilationError('type must be boolean')
    return Draft04Validator(attrs, scope, context.formats)


class Draft04Validator(Validator):
    def __init__(self, attrs, uri=None, formats=None):
        self.formats = formats or {}
        self.attrs = attrs
        self.uri = uri
        self.default = self.attrs.get('default', None)

    @error
    def validate(self, obj):
        obj = deepcopy(obj)
        obj = self.validate_enum(obj)
        obj = self.validate_type(obj)
        obj = self.validate_not(obj)
        obj = self.validate_all_of(obj)
        obj = self.validate_any_of(obj)
        obj = self.validate_one_of(obj)

        if self.is_array(obj):
            obj = self.validate_items(obj)
            obj = self.validate_max_items(obj)
            obj = self.validate_min_items(obj)
            obj = self.validate_unique_items(obj)
        elif self.is_number(obj):
            obj = self.validate_maximum(obj)
            obj = self.validate_minimum(obj)
            obj = self.validate_multiple_of(obj)
        elif self.is_object(obj):
            obj = self.validate_required(obj)
            obj = self.validate_max_properties(obj)
            obj = self.validate_min_properties(obj)
            obj = self.validate_dependencies(obj)
            obj = self.validate_properties(obj)
            obj = self.validate_default_properties(obj)
        elif self.is_string(obj):
            obj = self.validate_max_length(obj)
            obj = self.validate_min_length(obj)
            obj = self.validate_pattern(obj)
            obj = self.validate_format(obj)

        return obj

    def is_array(self, obj):
        return isinstance(obj, sequence_types)

    def is_boolean(self, obj):
        return isinstance(obj, bool)

    def is_integer(self, obj):
        return isinstance(obj, integer_types) and not isinstance(obj, bool)

    def is_number(self, obj):
        return isinstance(obj, number_types) and not isinstance(obj, bool)

    def is_object(self, obj):
        return isinstance(obj, dict)

    def is_string(self, obj):
        return isinstance(obj, string_types)

    def has_default(self):
        return 'default' in self.attrs

    @error
    def validate_all_of(self, obj):
        for validator in self.attrs.get('all_of', []):
            obj = validator.validate(obj)
        return obj

    @error
    def validate_any_of(self, obj):
        if 'any_of' in self.attrs:
            for validator in self.attrs['any_of']:
                try:
                    obj = validator.validate(obj)
                    return obj
                except ValidationError:
                    pass
            raise ValidationError('{!r} not in any_of'.format(obj))
        return obj

    @error
    def validate_default_properties(self, obj):
        """
        Reinject defaults from properties.
        """
        for name, validator in self.attrs.get('properties', {}).items():
            if name not in obj and validator.has_default():
                obj[name] = deepcopy(validator.default)
        return obj

    @error
    def validate_dependencies(self, obj):
        for key, dependencies in self.attrs.get('dependencies', {}).items():
            if key in obj:
                if isinstance(dependencies, sequence_types):
                    if set(dependencies) - set(obj.keys()):
                        raise ValidationError('{!r} missing dependencies {}'.format(obj, dependencies))
                else:
                    dependencies.validate(obj)
        return obj

    @error
    def validate_enum(self, obj):
        if 'enum' in self.attrs:
            if obj not in self.attrs['enum']:
                raise ValidationError('{!r} not in enum {}'.format(obj, self.attrs['enum']))
        return obj

    @error
    def validate_format(self, obj):
        if 'format' in self.attrs:
            try:
                return self.formats[self.attrs['format']](obj)
            except KeyError:
                logger.warning('format {} is not '
                               'defined.'.format(self.format))
            # if obj not in self.attrs['format']:
            #     raise ValidationError('{!r} not in format {}'.format(obj, self.attrs['format']))
        return obj

    @error
    def validate_one_of(self, obj):
        if 'one_of' in self.attrs:
            validated = 0
            for validator in self.attrs['one_of']:
                try:
                    obj1 = validator.validate(obj)
                    validated += 1
                except ValidationError:
                    pass
            if not validated:
                raise ValidationError('{!r} not in one_of'.format(obj))
            if validated == 1:
                return
            else:
                raise ValidationError('{!r} validates too much one_of'.format(obj))
        return obj

    @error
    def validate_not(self, obj):
        if 'not' in self.attrs:
            try:
                validator = self.attrs['not']
                validator.validate(obj)
            except ValidationError:
                return obj
            else:
                raise ValidationError('{!r} is forbidden'.format(obj))
        return obj

    @error
    def validate_maximum(self, obj):
        if 'maximum' in self.attrs:
            m = self.attrs['maximum']
            if obj < m:
                return obj
            exclusive = self.attrs.get('exclusive_maximum', True)
            if not exclusive and (obj == m):
                return obj
            raise ValidationError(m, obj)
        return obj

    @error
    def validate_minimum(self, obj):
        if 'minimum' in self.attrs:
            m = self.attrs['minimum']
            if obj > m:
                return obj
            exclusive = self.attrs.get('exclusive_minimum', True)
            if not exclusive and (obj == m):
                return obj
            raise ValidationError(m, obj)
        return obj

    @error
    def validate_items(self, obj):
        if 'items' in self.attrs:
            items = self.attrs['items']
            if isinstance(items, Validator):
                validator = items
                for index, element in enumerate(obj):
                    obj[index] = validator.validate(element)
                return obj
            elif isinstance(items, (list, tuple)):
                additionals = self.attrs.get('additional_items', True)  # True by default
                validators = items
                for index, element in enumerate(obj):
                    try:
                        validator = validators[index]
                    except IndexError:
                        if additionals is True:
                            return obj
                        elif additionals is False:
                            raise ValidationError('{!r} does not allow additional elements'.format(obj))
                        validator = additionals
                    obj[index] = validator.validate(element)
                return obj
            else:
                raise NotImplementedError(items)
        return obj

    @error
    def validate_max_items(self, obj):
        if 'max_items' in self.attrs:
            if len(obj) > self.attrs['max_items']:
                raise ValidationError('{!r} has to much elements'.format(obj))
        return obj

    @error
    def validate_min_items(self, obj):
        if 'min_items' in self.attrs:
            if len(obj) < self.attrs['min_items']:
                raise ValidationError('{!r} has to few elements'.format(obj))
        return obj

    @error
    def validate_max_length(self, obj):
        if 'max_length' in self.attrs:
            if len(text_type(obj)) > self.attrs['max_length']:
                raise ValidationError('{!r} is too long'.format(obj))
        return obj

    @error
    def validate_max_properties(self, obj):
        if 'max_properties' in self.attrs:
            if len(obj) > self.attrs['max_properties']:
                raise ValidationError('{!r} has too much properties'.format(obj))
        return obj

    @error
    def validate_min_length(self, obj):
        if 'min_length' in self.attrs:
            if len(text_type(obj)) < self.attrs['min_length']:
                raise ValidationError('{!r} is too short'.format(obj))
        return obj

    @error
    def validate_min_properties(self, obj):
        if 'min_properties' in self.attrs:
            if len(obj) < self.attrs['min_properties']:
                raise ValidationError('{!r} has too few properties'.format(obj))
        return obj

    @error
    def validate_multiple_of(self, obj):
        if 'multiple_of' in self.attrs:
            a, b = Decimal(str(obj)), Decimal(str(self.attrs['multiple_of']))
            if a % b != 0:
                raise ValidationError('{!r} is not a multiple of {}'.format(obj, self.attrs['multiple_of']))
        return obj

    @error
    def validate_pattern(self, obj):
        if 'pattern' in self.attrs:
            pattern = self.attrs['pattern']
            if re.search(pattern, obj):
                return obj
            raise ValidationError('{!r} does not match pattern {}'.format(obj, pattern))
        return obj

    @error
    def validate_properties(self, obj):
        validated = set()
        response = {}

        if not obj:
            return response

        for name, validator in self.attrs.get('properties', {}).items():
            if name in obj:
                response[name] = validator.validate(obj[name])
                validated.add(name)

        for pattern, validator in self.attrs.get('pattern_properties', {}).items():
            for name in sorted(obj.keys()):
                if re.search(pattern, name):
                    response[name] = validator.validate(obj[name])
                    validated.add(name)

        for name in validated:
            obj.pop(name, None)
        if not obj:
            return response

        additionals = self.attrs.get('additional_properties', True)  # additionalProperties True by default
        if additionals is True:
            return obj
        if additionals is False:
            raise ValidationError('{!r} does not allow additional properties'.format(obj))
        validator = additionals
        for name in sorted(obj.keys()):
            response[name] = validator.validate(obj.pop(name))
            validated.add(name)
        return obj

    @error
    def validate_required(self, obj):
        if 'required' in self.attrs:
            for name in self.attrs['required']:
                if name not in obj:
                    raise ValidationError('{!r} is missing {}'.format(name, obj))
        return obj

    @error
    def validate_type(self, obj):
        if 'type' in self.attrs:
            types = self.attrs['type']
            if isinstance(types, string_types):
                types = [types]

            for t in types:
                if t == 'array' and self.is_array(obj):
                    return obj
                if t == 'boolean' and self.is_boolean(obj):
                    return obj
                if t == 'integer' and self.is_integer(obj):
                    return obj
                if t == 'number' and self.is_number(obj):
                    return obj
                if t == 'null' and obj is None:
                    return obj
                if t == 'object' and self.is_object(obj):
                    return obj
                if t == 'string' and self.is_string(obj):
                    return obj
            print('type does not match', types, obj, self.attrs)
            raise ValidationError('type does not match', types, obj)
        return obj

    @error
    def validate_unique_items(self, obj):
        if self.attrs.get('unique_items'):
            if len(obj) > len(set(json.dumps(element) for element in obj)):
                raise ValidationError('Elements must be unique! {!r}'.format(obj))
        return obj
