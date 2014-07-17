"""
    jsonspec.validators.bases
    ~~~~~~~~~~~~~~~~~~~~~~~~~

"""

__all__ = ['error', 'ValidationError', 'Validator', 'ReferenceValidator']

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
        """shortcut for validate()"""
        return self.validate(obj)


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
        Validate object against validator

        :param obj: the object to validate
        """
        return self.validator.validate(obj)
