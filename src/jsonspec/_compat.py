import sys

__all__ = ["load_entry_points"]

if sys.version_info >= (3, 10):
    from importlib.metadata import entry_points as load_entry_points
else:
    from importlib_metadata import entry_points as load_entry_points
