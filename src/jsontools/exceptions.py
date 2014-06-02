"""
    jsontools.exceptions
    ~~~~~~~~~~~~~~~~~~~~

"""

__all__ = ['ReferenceError', 'SchemaError']


class SchemaError(Exception):
    """Raised while schema parsing"""
    def __init__(self, message, schema):
        super(SchemaError, self).__init__(message, schema)
        self.schema = schema


class ReferenceError(Exception):
    """Raised while reference error"""
    def __init__(self, *args):
        super(ReferenceError, self).__init__(*args)


class ValidationError(Exception):
    """Raised while validating an obj with JsonSchema"""
    def __init__(self, message, reference=None):
        super(ValidationError, self).__init__(message)
        self.message = message
        self.reference = reference
