"""
    jsonspec.pointer.bases
    ~~~~~~~~~~~~~~~~~~~~~~

"""


__all__ = ['DocumentPointer', 'Pointer', 'PointerToken']

import logging
from six import string_types
from .exceptions import ExtractError, RefError, LastElement, OutOfBounds, OutOfRange, WrongType  # noqa

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

    def endswith(self, txt):
        """used by os.path.join"""
        return str(self).endswith(txt)

    def __iadd__(self, txt):
        """append fragments"""
        data = str(self) + txt
        return DocumentPointer(data)

    def __iter__(self):
        """Return document and pointer.
        """
        return iter([self.document, self.pointer])

    def __eq__(self, other):
        if isinstance(other, string_types):
            return other == self.__str__()
        return super(Pointer, self).__eq__(other)

    def __str__(self):
        return '{}#{}'.format(self.document, self.pointer)

    def __repr__(self):
        return '<DocumentPointer({})'.format(self)


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
                token = PointerToken(part)
                token.last = False
                tokens.append(token)
        self.tokens = tokens

        if self.tokens:
            self.tokens[-1].last = True

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
        """Walk thru tokens.
        """
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
                    raise RefError(obj, 'presence of a $ref member')
                obj = self.extract_mapping(obj)
            elif isinstance(obj, (list, tuple)):
                obj = self.extract_sequence(obj)
            else:
                raise WrongType(obj, '{!r} does not apply '
                                     'for {!r}'.format(str(self), obj))

            if isinstance(obj, dict):
                if not bypass_ref and '$ref' in obj:
                    raise RefError(obj, 'presence of a $ref member')
            return obj
        except ExtractError as error:
            logger.exception(error)
            raise
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

        raise OutOfBounds(obj, 'member {!r} not found'.format(str(self)))

    def extract_sequence(self, obj):
        if self == '-':
            raise LastElement(obj, 'last element is needed')
        if not self.isdigit():
            raise WrongType(obj, '{!r} does not apply '
                                 'for sequence'.format(str(self)))
        try:
            return obj[int(self)]
        except IndexError:
            raise OutOfRange(obj, 'element {!r} not found'.format(str(self)))

    def __repr__(self):
        return '<{}({!r})>'.format(self.__class__.__name__, str(self))
