import sys

__all__ = ["load_entry_points"]

if sys.version_info >= (3, 10):
    from importlib.metadata import entry_points as load_entry_points
    from importlib.metadata import PackageNotFoundError
else:
    from importlib_metadata import entry_points as load_entry_points
    from importlib_metadata import PackageNotFoundError
