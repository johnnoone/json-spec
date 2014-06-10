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
