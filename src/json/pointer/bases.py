"""
    json.pointer.bases
    ~~~~~~~~~~~~~~~~~~

"""


__all__ = ['DocumentPointer', 'Pointer', 'PointerToken']

import logging
from six import string_types
from .exceptions import ExtractError

logger = logging.getLogger(__name__)


class DocumentPointer(object):
    """Defines a document pointer

    :ivar document: document name
    :ivar pointer: pointer
    """

    def __init__(self, pointer):
        """
        :param pointer: a string or DocumentPointer instance
        """
        if isinstance(pointer, DocumentPointer):
            document, path = pointer
        elif '#' not in pointer:
            raise ValueError('# is missing')
        else:
            document, path = pointer.split('#', 1)
        self.document = document
        self.pointer = Pointer(path)

    def extract(self, obj, bypass_ref=False):
        """
        Extract subelement from obj, according to pointer.
        It assums that document is the object.

        :param obj: the object source
        :param bypass_ref: disable JSON Reference errors
        """
        return self.pointer.extract(obj, bypass_ref)

    def is_inner(self):
        """Tells if pointer refers to an inner document
        """
        return self.document == ''

    def __iter__(self):
        return iter([self.document, self.pointer])

    def __eq__(self, other):
        if isinstance(other, string_types):
            return other == self.__str__()
        return super(Pointer, self).__eq__(other)

    def __str__(self):
        return '{}#{}'.format(self.document, self.pointer)


class Pointer(object):
    """Defines a pointer

    :ivar tokens: list of PointerToken
    """

    def __init__(self, pointer):
        """
        :param pointer: a string or Pointer instance
        """
        if isinstance(pointer, Pointer):
            tokens = pointer.tokens[:]
        elif pointer == '':
            tokens = []
        elif not pointer.startswith('/'):
            raise ValueError('pointer must start with /', pointer)
        else:
            # decode now
            tokens = []
            for part in pointer[1:].split('/'):
                part = part.replace('~1', '/')
                part = part.replace('~0', '~')
                tokens.append(PointerToken(part))
        self.tokens = tokens

    def extract(self, obj, bypass_ref=False):
        """
        Extract subelement from obj, according to tokens.

        :param obj: the object source
        :param bypass_ref: disable JSON Reference errors
        """
        for token in self.tokens:
            obj = token.extract(obj, bypass_ref)
        return obj

    def __iter__(self):
        return iter(self.tokens)

    def __eq__(self, other):
        if isinstance(other, string_types):
            return other == self.__str__()
        return super(Pointer, self).__eq__(other)

    def __str__(self):
        output = ''
        for part in self.tokens:
            part = part.replace('~', '~0')
            part = part.replace('/', '~1')
            output += '/' + part
        return output

    def __repr__(self):
        return '<{}({!r})>'.format(self.__class__.__name__, self.__str__())


class PointerToken(str):
    """
    A single token
    """

    def extract(self, obj, bypass_ref=False):
        """
        Extract subelement from obj, according to current token.

        :param obj: the object source
        :param bypass_ref: disable JSON Reference errors
        """
        try:
            if isinstance(obj, dict):
                if not bypass_ref and '$ref' in obj:
                    raise ValueError('presence of a $ref member')
                obj = self.extract_mapping(obj)
            elif isinstance(obj, (list, tuple)):
                obj = self.extract_sequence(obj)
            else:
                raise TypeError('not for this kind', self, obj)

            if isinstance(obj, dict):
                if not bypass_ref and '$ref' in obj:
                    raise ValueError('presence of a $ref member', bypass_ref)
            return obj
        except Exception as error:
            logger.exception(error)
            args = [arg for arg in error.args if arg not in (self, obj)]
            raise ExtractError(obj, *args)

    def extract_mapping(self, obj):
        if self in obj:
            return obj[self]

        if self.isdigit():
            key = int(self)
            if key in obj:
                return obj[key]

        raise KeyError('member not found', self, obj)

    def extract_sequence(self, obj):
        if self == '-':
            raise ValueError('refers to a nonexistent array element')
        if not self.isdigit():
            raise TypeError('not for this kind', self, obj)
        try:
            return obj[int(self)]
        except IndexError:
            raise IndexError('element not found', self, obj)

    def __repr__(self):
        return '<{}({!r})>'.format(self.__class__.__name__, str(self))
