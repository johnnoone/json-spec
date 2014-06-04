"""
    json.schema.exceptions
    ~~~~~~~~~~~~~~~~~~~~~~

"""

__all__ = ['CompilationError', 'ReferenceError', 'ValidationError']


class CompilationError(Exception):
    """Raised while schema parsing"""
    def __init__(self, message, schema):
        super(CompilationError, self).__init__(message, schema)
        self.schema = schema


class ReferenceError(Exception):
    """Raised while reference error"""
    def __init__(self, *args):
        super(ReferenceError, self).__init__(*args)


class ValidationError(Exception):
    """Raised while validating an obj with JsonSchema"""
    def __init__(self, message, obj=None, rule=None):
        super(ValidationError, self).__init__(message)
        self.obj = obj
        self.rule = rule
