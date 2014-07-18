"""
    jsonspec.validators.draft03
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Implements JSON Schema draft03.
"""

__all__ = ['compile', 'Draft03Validator']

import logging
import os.path
import re
from copy import deepcopy
from decimal import Decimal
from six import integer_types, string_types
from six.moves.urllib.parse import urljoin
from .bases import ReferenceValidator, Validator, error
from .exceptions import CompilationError
from .factorize import register
from jsonspec.validators.exceptions import ValidationError
from jsonspec.validators.util import uncamel
from jsonspec import driver as json

sequence_types = (list, set, tuple)
number_types = (integer_types, float, Decimal)
logger = logging.getLogger(__name__)


@register(spec='http://json-schema.org/draft-03/schema#')
def compile(schema, pointer, context, scope=None):
    """
    Compiles schema with `JSON Schema`_ draft-03.

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
        subpointer = os.path.join(pointer, 'additionalItems')
        attrs['additional_items'] = schm.pop('additionalItems')
        if isinstance(attrs['additional_items'], dict):
            compiled = compile(attrs['additional_items'],
                               subpointer,
                               context,
                               scope)
            attrs['additional_items'] = compiled
        elif not isinstance(attrs['additional_items'], bool):
            raise CompilationError('wrong type for {}'.format('additional_items'), schema)  # noqa

    if 'additionalProperties' in schm:
        attrs['additional_properties'] = schm.pop('additionalProperties')
        if isinstance(attrs['additional_properties'], dict):
            subpointer = os.path.join(pointer, 'additionalProperties')
            value = attrs['additional_properties']
            attrs['additional_properties'] = compile(value,
                                                     subpointer,
                                                     context,
                                                     scope)
        elif not isinstance(attrs['additional_properties'], bool):
            raise CompilationError('additionalProperties must be an object or boolean', schema)  # noqa

    if 'dependencies' in schm:
        attrs['dependencies'] = schm.pop('dependencies')
        if not isinstance(attrs['dependencies'], dict):
            raise CompilationError('dependencies must be an object', schema)
        for key, value in attrs['dependencies'].items():
            if isinstance(value, dict):
                subpointer = os.path.join(pointer, 'dependencies', key)
                attrs['dependencies'][key] = compile(value,
                                                     subpointer,
                                                     context,
                                                     scope)
            elif isinstance(value, sequence_types):
                continue
            elif not isinstance(value, string_types):
                raise CompilationError('dependencies must be an array, object or string', schema)  # noqa

    if 'disallow' in schm:
        attrs['disallow'] = schm.pop('disallow')
        if isinstance(attrs['disallow'], sequence_types):
            for index, value in enumerate(attrs['disallow']):
                if isinstance(value, dict):
                    subpointer = os.path.join(pointer, 'disallow', str(index))
                    attrs['disallow'][index] = compile(value,
                                                       subpointer,
                                                       context,
                                                       scope)
                elif not isinstance(value, string_types):
                    raise CompilationError('disallow must be an object or string', schema)  # noqa
        elif not isinstance(attrs['disallow'], string_types):
            raise CompilationError('disallow must be an array or string', schema)  # noqa

    if 'divisibleBy' in schm:
        attrs['divisible_by'] = schm.pop('divisibleBy')
        if not isinstance(attrs['divisible_by'], number_types):
            raise CompilationError('divisibleBy must be a number')

    if 'enum' in schm:
        attrs['enum'] = schm.pop('enum')
        if not isinstance(attrs['enum'], sequence_types):
            raise CompilationError('enum must be a sequence', schema)

    if 'exclusiveMaximum' in schm:
        attrs['exclusive_maximum'] = schm.pop('exclusiveMaximum')
        if not isinstance(attrs['exclusive_maximum'], bool):
            raise CompilationError('exclusiveMaximum must be a boolean', schema)  # noqa

    if 'exclusiveMinimum' in schm:
        attrs['exclusive_minimum'] = schm.pop('exclusiveMinimum')
        if not isinstance(attrs['exclusive_minimum'], bool):
            raise CompilationError('exclusiveMinimum must be a boolean', schema)  # noqa

    if 'extends' in schm:
        attrs['extends'] = schm.pop('extends')
        subpointer = os.path.join(pointer, 'extends')
        if isinstance(attrs['extends'], dict):
            attrs['extends'] = compile(attrs['extends'],
                                       subpointer,
                                       context,
                                       scope)
        elif isinstance(attrs['extends'], sequence_types):
            for index, value in enumerate(attrs['extends']):
                attrs['extends'][index] = compile(value,
                                                  subpointer,
                                                  context,
                                                  scope)
        else:
            raise CompilationError('extends must be an object or array', schema)  # noqa

    if 'format' in schm:
        attrs['format'] = schm.pop('format')
        if not isinstance(attrs['format'], string_types):
            raise CompilationError('format must be a string')

    if 'items' in schm:
        subpointer = os.path.join(pointer, 'items')
        attrs['items'] = schm.pop('items')
        if isinstance(attrs['items'], (list, tuple)):
            # each value must be a json schema
            attrs['items'] = [compile(element, subpointer, context, scope) for element in attrs['items']]  # noqa
        elif isinstance(attrs['items'], dict):
            # value must be a json schema
            attrs['items'] = compile(attrs['items'], subpointer, context, scope)  # noqa
        else:
            # should be a boolean
            raise CompilationError('wrong type for {}'.format('items'), schema)  # noqa

    if 'maximum' in schm:
        attrs['maximum'] = schm.pop('maximum')
        if not isinstance(attrs['maximum'], number_types):
            raise CompilationError('enum must be an integer', schema)

    if 'maxItems' in schm:
        attrs['max_items'] = schm.pop('maxItems')
        if not isinstance(attrs['max_items'], integer_types):
            raise CompilationError('maxItems must be an integer', schema)

    if 'maxLength' in schm:
        attrs['max_length'] = schm.pop('maxLength')
        if not isinstance(attrs['max_length'], integer_types):
            raise CompilationError('maxLength must be integer')

    if 'minimum' in schm:
        attrs['minimum'] = schm.pop('minimum')
        if not isinstance(attrs['minimum'], number_types):
            raise CompilationError('enum must be a number', schema)

    if 'minItems' in schm:
        attrs['min_items'] = schm.pop('minItems')
        if not isinstance(attrs['min_items'], integer_types):
            raise CompilationError('minItems must be an integer', schema)

    if 'minLength' in schm:
        attrs['min_length'] = schm.pop('minLength')
        if not isinstance(attrs['min_length'], integer_types):
            raise CompilationError('minLength must be integer')

    if 'pattern' in schm:
        attrs['pattern'] = schm.pop('pattern')
        if not isinstance(attrs['pattern'], string_types):
            raise CompilationError('pattern must be a string', schema)

    if 'patternProperties' in schm:
        attrs['pattern_properties'] = schm.pop('patternProperties')
        if not isinstance(attrs['pattern_properties'], dict):
            raise CompilationError('patternProperties must be an object', schema)  # noqa
        for name, value in attrs['pattern_properties'].items():
            subpointer = os.path.join(pointer, 'patternProperties', name)
            attrs['pattern_properties'][name] = compile(value,
                                                        subpointer,
                                                        context,
                                                        scope)

    if 'properties' in schm:
        attrs['properties'] = schm.pop('properties')
        if not isinstance(attrs['properties'], dict):
            raise CompilationError('properties must be an object', schema)
        for name, value in attrs['properties'].items():
            subpointer = os.path.join(pointer, 'properties', name)
            attrs['properties'][name] = compile(value,
                                                subpointer,
                                                context,
                                                scope)

    if 'required' in schm:
        attrs['required'] = schm.pop('required')
        if not isinstance(attrs['required'], bool):
            raise CompilationError('required must be a boolean', schema)

    if 'type' in schm:
        attrs['type'] = schm.pop('type')
        if isinstance(attrs['type'], sequence_types):
            for index, value in enumerate(attrs['type']):
                if isinstance(value, dict):
                    subpointer = os.path.join(pointer, 'type', str(index))
                    attrs['type'][index] = compile(value,
                                                   subpointer,
                                                   context,
                                                   scope)
                elif not isinstance(value, string_types):
                    raise CompilationError('type must be an object or string', schema)  # noqa
        elif not isinstance(attrs['type'], string_types):
            raise CompilationError('type must be an array or string', schema)  # noqa

    if 'uniqueItems' in schm:
        attrs['unique_items'] = schm.pop('uniqueItems')
        if not isinstance(attrs['unique_items'], bool):
            raise CompilationError('type must be boolean')

    return Draft03Validator(attrs, scope, context.formats)


class Draft03Validator(Validator):
    """
    Implements `JSON Schema`_ draft-03 validation.

    :ivar attrs: attributes to validate against
    :ivar uri: uri of the current validator
    :ivar formats: mapping of available formats

    >>> validator = Draft03Validator({'min_length': 4})
    >>> assert validator('this is sparta')

    .. _`JSON Schema`: http://json-schema.org
    """

    def __init__(self, attrs, uri=None, formats=None):
        attrs = {uncamel(k): v for k, v in attrs.items()}

        self.attrs = attrs
        self.attrs.setdefault('additional_items', True)
        self.attrs.setdefault('exclusive_maximum', False)
        self.attrs.setdefault('exclusive_minimum', False)
        self.uri = uri
        self.formats = formats or {}
        self.default = self.attrs.get('default', None)

    def is_array(self, obj):
        return isinstance(obj, sequence_types)

    def is_boolean(self, obj):
        return isinstance(obj, bool)

    def is_integer(self, obj):
        return isinstance(obj, integer_types) and not isinstance(obj, bool)

    def is_null(self, obj):
        return obj is None

    def is_number(self, obj):
        return isinstance(obj, number_types) and not isinstance(obj, bool)

    def is_object(self, obj):
        return isinstance(obj, dict)

    def is_string(self, obj):
        return isinstance(obj, string_types)

    @error
    def validate(self, obj):
        """
        Validate object against validator

        :param obj: the object to validate
        """
        obj = deepcopy(obj)
        obj = self.validate_enum(obj)
        obj = self.validate_type(obj)
        obj = self.validate_disallow(obj)
        obj = self.validate_extends(obj)

        if self.is_array(obj):
            obj = self.validate_max_items(obj)
            obj = self.validate_min_items(obj)
            obj = self.validate_items(obj)
            obj = self.validate_unique_items(obj)

        if self.is_number(obj):
            obj = self.validate_maximum(obj)
            obj = self.validate_minimum(obj)
            obj = self.validate_divisible_by(obj)

        if self.is_object(obj):
            obj = self.validate_dependencies(obj)
            obj = self.validate_properties(obj)

        if self.is_string(obj):
            obj = self.validate_max_length(obj)
            obj = self.validate_min_length(obj)
            obj = self.validate_pattern(obj)
            obj = self.validate_format(obj)
        return obj

    @error
    def validate_dependencies(self, obj):
        if 'dependencies' in self.attrs:
            missings = set()
            for name, dependencies in self.attrs['dependencies'].items():
                if name not in obj:
                    continue
                if isinstance(dependencies, Validator):
                    obj[name] = dependencies(obj)
                elif isinstance(dependencies, sequence_types):
                    for d in dependencies:
                        if d not in obj:
                            missings.add(d)
                elif dependencies not in obj:
                    missings.add(dependencies)
            if missings:
                missings = sorted(missings)
                raise ValidationError('Missing properties {}'.format(missings))
        return obj

    @error
    def validate_disallow(self, obj):
        if 'disallow' in self.attrs:
            disallows = self.attrs['disallow']
            if not isinstance(disallows, sequence_types):
                disallows = [disallows]
            disallowed = 0
            for type in disallows:
                try:
                    if isinstance(type, Validator):
                        type(obj)
                        disallowed += 1
                    elif type == "any":
                        disallowed += 1
                    elif type == "array" and self.is_array(obj):
                        disallowed += 1
                    elif type == "boolean" and self.is_boolean(obj):
                        disallowed += 1
                    elif type == "integer" and self.is_integer(obj):
                        disallowed += 1
                    elif type == "null" and self.is_null(obj):
                        disallowed += 1
                    elif type == "number" and self.is_number(obj):
                        disallowed += 1
                    elif type == "object" and self.is_object(obj):
                        disallowed += 1
                    elif type == "string" and self.is_string(obj):
                        disallowed += 1
                except ValidationError:
                    # let it, it may be good
                    pass
            if disallowed:
                raise ValidationError('Wrong type', obj)
        return obj

    @error
    def validate_divisible_by(self, obj):
        if 'divisible_by' in self.attrs:
            factor = Decimal(str(self.attrs['divisible_by']))
            orig = Decimal(str(obj))
            if orig % factor != 0:
                raise ValidationError('Not a multiple of {}'.format(factor))
        return obj

    @error
    def validate_enum(self, obj):
        if 'enum' in self.attrs:
            if not obj in self.attrs['enum']:
                raise ValidationError('Forbidden value')
        return obj

    @error
    def validate_extends(self, obj):
        if 'extends' in self.attrs:
            extends = self.attrs['extends']
            if not isinstance(extends, sequence_types):
                extends = [extends]
            for type in extends:
                obj = type(obj)
        return obj

    @error
    def validate_format(self, obj):
        """
        ================= ============
        Expected draft03  Alias of
        ----------------- ------------
        color             css:color
        date-time         utc:datetime
        date              utc:date
        time              utc:time
        utc-millisec      utc:millisec
        regex             regex
        style             css:style
        phone             phone
        uri               uri
        email             email
        ip-address        ipv4
        ipv6              ipv6
        host-name         hostname
        ================= ============

        """

        if 'format' in self.attrs:
            substituted = {
                'color': 'css:color',
                'date-time': 'utc:datetime',
                'date': 'utc:date',
                'time': 'utc:time',
                'utc-millisec': 'utc:millisec',
                'regex': 'regex',
                'style': 'css:style',
                'phone': 'phone',
                'uri': 'uri',
                'email': 'email',
                'ip-address': 'ipv4',
                'ipv6': 'ipv6',
                'host-name': 'hostname',
            }.get(self.attrs['format'], self.attrs['format'])
            logger.debug('use %s', substituted)
            return self.formats[substituted](obj)
        return obj

    @error
    def validate_items(self, obj):
        if 'items' in self.attrs:
            items = self.attrs['items']
            if isinstance(items, Validator):
                validator = items
                for index, element in enumerate(obj):
                    obj[index] = validator(element)
                return obj
            elif isinstance(items, (list, tuple)):
                additionals = self.attrs['additional_items']
                validators = items
                for index, element in enumerate(obj):
                    try:
                        validator = validators[index]
                    except IndexError:
                        if additionals is True:
                            return obj
                        elif additionals is False:
                            raise ValidationError('Additional elements are forbidden', obj)  # noqa
                        validator = additionals
                    obj[index] = validator(element)
                return obj
            else:
                raise NotImplementedError(items)
        return obj

    @error
    def validate_max_items(self, obj):
        if 'max_items' in self.attrs:
            count = len(obj)
            if count > self.attrs['max_items']:
                raise ValidationError('Too many items')
        return obj

    @error
    def validate_max_length(self, obj):
        if 'max_length' in self.attrs:
            length = len(obj)
            if length > self.attrs['max_length']:
                raise ValidationError('Too long {}'.format(length))
        return obj

    @error
    def validate_maximum(self, obj):
        if 'maximum' in self.attrs:
            if obj > self.attrs['maximum']:
                raise ValidationError('Too big number')
            if self.attrs['exclusive_maximum'] and obj == self.attrs['maximum']:  # noqa
                raise ValidationError('Too big number')
        return obj

    @error
    def validate_min_items(self, obj):
        if 'min_items' in self.attrs:
            count = len(obj)
            if count < self.attrs['min_items']:
                raise ValidationError('Too few items')
        return obj

    @error
    def validate_min_length(self, obj):
        if 'min_length' in self.attrs:
            length = len(obj)
            if length < self.attrs['min_length']:
                raise ValidationError('Too short {}'.format(length))
        return obj

    @error
    def validate_minimum(self, obj):
        if 'minimum' in self.attrs:
            if obj < self.attrs['minimum']:
                raise ValidationError('Too low number')
            if self.attrs['exclusive_minimum'] and obj == self.attrs['minimum']:  # noqa
                raise ValidationError('Too low number')
        return obj

    @error
    def validate_pattern(self, obj):
        if 'pattern' in self.attrs:
            regex = re.compile(self.attrs['pattern'])
            if not regex.search(obj):
                raise ValidationError('Does not match pattern')
        return obj

    @error
    def validate_properties(self, obj):
        validated = set()
        if 'properties' in self.attrs:
            for name, validator in self.attrs['properties'].items():
                if name in obj:
                    obj[name] = validator(obj[name])
                    validated.add(name)
                elif not validator.is_optional():
                    raise ValidationError('Required property')
        if 'pattern_properties' in self.attrs:
            for pattern, validator in self.attrs['pattern_properties'].items():
                regex = re.compile(pattern)
                for name, value in obj.items():
                    if regex.search(name):
                        obj[name] = validator(obj[name])
                        validated.add(name)

        if 'additional_properties' in self.attrs:
            if self.attrs['additional_properties'] is True:
                return obj

            if self.attrs['additional_properties'] is False:
                if len(obj) > len(validated):
                    raise ValidationError('Additional properties are forbidden')  # noqa

            validator = self.attrs['additional_properties']
            for name, value in obj.items():
                if name not in validated:
                    obj[name] = validator(value)
                    validated.add(name)

        return obj

    @error
    def validate_type(self, obj):
        if 'type' in self.attrs:
            types = self.attrs['type']
            if not isinstance(types, sequence_types):
                types = [types]
            for type in types:
                try:
                    if isinstance(type, Validator):
                        return type(obj)
                    elif type == "any":
                        return obj
                    elif type == "array" and self.is_array(obj):
                        return obj
                    elif type == "boolean" and self.is_boolean(obj):
                        return obj
                    elif type == "integer" and self.is_integer(obj):
                        return obj
                    elif type == "null" and self.is_null(obj):
                        return obj
                    elif type == "number" and self.is_number(obj):
                        return obj
                    elif type == "object" and self.is_object(obj):
                        return obj
                    elif type == "string" and self.is_string(obj):
                        return obj
                except ValidationError:
                    # let it, it may be good
                    pass
            raise ValidationError('Wrong type', obj)
        return obj

    @error
    def validate_unique_items(self, obj):
        if self.attrs.get('unique_items'):
            if len(obj) > len(set(json.dumps(element) for element in obj)):
                raise ValidationError('Elements must be unique', obj)
        return obj

    def has_default(self):
        """docstring for has_default"""
        return False

    def is_optional(self):
        """
        True by default.
        """
        return not self.attrs.get('required', False)
