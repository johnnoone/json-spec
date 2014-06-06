"""
    json.schema.bases
    ~~~~~~~~~~~~~~~~~

"""

from __future__ import absolute_import, print_function, unicode_literals

__all__ = ['BaseValidator']

from abc import abstractmethod


class Validator(object):
    @abstractmethod
    def has_default(self):
        pass

    @abstractmethod
    def validate(self, obj):
        pass


class ReferenceValidator(Validator):
    """
    Loads lately validator.
    """

    def __init__(self, uri, factory, spec=None):
        self.uri = uri
        self.factory = factory
        self.spec = spec

    @property
    def validator(self):
        if not hasattr(self, '_validator'):
            self._validator = self.factory.load(self.uri, self.spec)

        return self._validator

    def has_default(self):
        return self.validator.has_default()

    @property
    def default(self):
        return self.validator.default

    def validate(self, obj):
        return self.validator.validate(obj)
