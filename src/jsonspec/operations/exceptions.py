"""
    jsonspec.operations.exceptions
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

__all__ = ["Error", "NonexistentTarget"]


class Error(LookupError):
    pass


class NonexistentTarget(Error):
    """Raised when trying to get a non existent target"""

    pass
