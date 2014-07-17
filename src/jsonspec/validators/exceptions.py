
__all__ = ['error', 'CompilationError', 'ReferenceError', 'ValidationError']

from six import wraps


def error(meth):
    @wraps(meth)
    def wrapper(self, obj, *args, **kwargs):
        try:
            return meth(self, obj, *args, **kwargs)
        except ValidationError as error:
            if not error.obj:
                error.obj = obj
            if not error.rule:
                error.rule = self.uri
            raise
    return wrapper


class CompilationError(Exception):
    """Raised while schema parsing"""
    def __init__(self, message, schema):
        super(CompilationError, self).__init__(message, schema)
        self.schema = schema


class ReferenceError(Exception):
    """Raised while reference error"""
    def __init__(self, *args):
        super(ReferenceError, self).__init__(*args)


class ValidationError(ValueError):
    """Raised when validation fails"""
    def __init__(self, reason, obj=None, rule=None, error=None):
        """
        :param reason: the reason failing
        :param obj: the obj that fails
        :param error: sub errors, if they exists
        """
        super(ValidationError, self).__init__(reason, obj)
        self.obj = obj
        self.rule = rule

        self.error = set()
        if isinstance(error, (list, tuple, set)):
            self.error.update(error)
        elif isinstance(error, Exception):
            self.error.add(error)
