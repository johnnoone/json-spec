"""
    json.schema.bases
    ~~~~~~~~~~~~~~~~~

"""

from __future__ import absolute_import, print_function, unicode_literals

__all__ = ['BaseValidator']

from abc import abstractmethod


class BaseValidator(object):
    @abstractmethod
    def validate(self, obj):
        pass
