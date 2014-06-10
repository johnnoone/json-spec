"""
    jsonspec.validators.bases
    ~~~~~~~~~~~~~~~~~~~~~~~~~

"""

__all__ = ['Validator', 'ReferenceValidator']

from abc import abstractmethod
from jsonspec.pointer import DocumentPointer


class Validator(object):

    @abstractmethod
    def has_default(self):
        pass

    @abstractmethod
    def validate(self, obj):
        pass


class ReferenceValidator(Validator):
    def __init__(self, pointer, factory, registry, spec=None):
        self.pointer = DocumentPointer(pointer)
        self.factory = factory
        self.registry = registry
        self.spec = spec

    @property
    def validator(self):
        if not hasattr(self, '_validator'):
            self._validator = self.factory(self.registry.resolve(self.pointer), self.spec)

        return self._validator

    def has_default(self):
        return self.validator.has_default()

    @property
    def default(self):
        return self.validator.default

    def validate(self, obj):
        return self.validator.validate(obj)