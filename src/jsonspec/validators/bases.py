"""
    jsonspec.validators.bases
    ~~~~~~~~~~~~~~~~~~~~~~~~~

"""

__all__ = ['error', 'Validator', 'ReferenceValidator', 'NotValidator',
           'CompoundValidator', 'AllValidator', 'AnyValidator', 'OneValidator']

import logging
from abc import abstractmethod, ABCMeta
from six import add_metaclass
from jsonspec.pointer import DocumentPointer
from .exceptions import error, ValidationError


logger = logging.getLogger(__name__)


@add_metaclass(ABCMeta)
class Validator(object):
    """
    The mother of Validators.
    """
    #: indicates current uri
    uri = None

    default = None

    def __init__(self, **attrs):
        self.uri = attrs.pop('uri', None)

    @abstractmethod
    def has_default(self):
        pass

    @abstractmethod
    def validate(self, obj):
        pass

    def __call__(self, obj):
        return self.validate(obj)

    def __neg__(self):
        """-<Validator>"""
        return NotValidator(self)

    def __or__(self, validator):
        """<Validator> | <Validator>"""
        return AnyValidator(validators=[self, validator])

    def __xor__(self, validator):
        """<Validator> ^ <Validator>"""
        return OneValidator(validators=[self, validator])

    def __and__(self, validator):
        """<Validator> & <Validator>"""
        return AllValidator(validators=[self, validator])

    def __repr__(self):
        return '<{}(uri={!r})>'.format(
            self.__class__.__name__,
            self.uri
        )


class NotValidator(Validator):
    """Must no match to validator.

    :ivar validator: validator
    :type validator: Validator

    >>> validator = StringValidator('foo')
    >>> assert validator('foo')
    >>> # negate validation
    >>> assert NotValidate(validator)(42)
    >>> # works also with the minus sign
    >>> assert -(validator)(42)
    """
    def __init__(self, validator):
        self.validator = validator

    def has_default(self):
        return False

    @error
    def validate(self, obj):
        logger.debug('%s validates %s', self, obj)
        try:
            self.validator.validate(obj)
        except ValidationError:
            return obj
        else:
            raise ValidationError('Matched validator')

    def __neg__(self):
        return self.validator


class ReferenceValidator(Validator):
    """
    Reference a validator to his pointer.

    :ivar pointer: the pointer to the validator
    :ivar context: the context object
    :ivar default: return the default validator
    :ivar validator: return the lazy loaded validator

    >>> validator = ReferenceValidator('http://json-schema.org/geo#', context)
    >>> assert validator({
    >>>     'latitude': 0.0124,
    >>>     'longitude': 1.2345
    >>> })
    """
    def __init__(self, pointer, context):
        super(ReferenceValidator, self).__init__()
        self.pointer = DocumentPointer(pointer)
        self.context = context
        self.uri = str(self.pointer)

    @property
    def validator(self):
        if not hasattr(self, '_validator'):
            self._validator = self.context.resolve(self.pointer)
        return self._validator

    def has_default(self):
        return self.validator.has_default()

    @property
    def default(self):
        return self.validator.default

    def validate(self, obj):
        """
        Validate obj against validator
        """
        return self.validator.validate(obj)


class CompoundValidator(Validator):
    validators = None #: the validators set

    def __init__(self, validators, **attrs):
        super(CompoundValidator, self).__init__(**attrs)
        self.validators = set()
        self.validators.update(validators)

    def has_default(self):
        for validator in self.validators:
            if validator.has_default():
                return True


class AnyValidator(CompoundValidator):
    """Match against any validator.

    :ivar validators: validators set
    """

    @property
    def default(self):
        for validator in self.validators:
            if validator.has_default():
                return validator.default
        raise AttributeError('{!r} object has no attribute {!r}'.format(
            self.__class_.__name__, 'default'
        ))

    @error
    def validate(self, obj):
        logger.debug('%s validates %s', self, obj)
        errors = []
        for validator in self.validators:
            try:
                response = validator.validate(obj)
                logger.debug('%s gets %s', validator, obj)
                return response
            except ValidationError as error:
                logger.debug('%s fails %s', validator, obj)
                errors.append(error)
        raise ValidationError('None match', error=errors)

    def __or__(self, validator):
        """Validator() | Validator()"""
        self.validators.add(validator)
        return self


class AllValidator(CompoundValidator):
    """Match against all validator.

    :ivar validators: validators set
    """

    @error
    def validate(self, obj):
        logger.debug('%s validates %s', self, obj)
        try:
            for validator in self.validators:
                obj = validator.validate(obj)
                logger.debug('%s gets %s', validator, obj)
        except ValidationError as error:
            raise ValidationError('One validator failed at least',
                                  error=error)
        return obj

    def __and__(self, validator):
        """<Validator> & <Validator>"""
        self.validators.add(validator)
        return self


class OneValidator(CompoundValidator):
    """Match against one validator.

    :ivar validators: validators set
    """

    @error
    def validate(self, obj):
        logger.debug('%s validates %s', self, obj)
        response, count, errors = None, 0, []
        for validator in self.validators:
            try:
                response = validator.validate(obj)
                count += 1
            except ValidationError as error:
                errors.append(error)
            if count > 1:
                break

        if count == 1:
            return response
        if count:
            raise ValidationError('Matchs more than one validator')
        raise ValidationError('No match', error=errors)

    def __xor__(self, validator):
        """<Validator> ^ <Validator>"""
        self.validators.add(validator)
        return self
