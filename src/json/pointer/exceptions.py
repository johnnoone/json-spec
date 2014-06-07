"""
    json.pointer.exceptions
    ~~~~~~~~~~~~~~~~~~~~~~~

"""

__all__ = ['ExtractError']


class ExtractError(Exception):
    def __init__(self, obj, *args):
        super(ExtractError, self).__init__(*args)
        self.obj = obj
