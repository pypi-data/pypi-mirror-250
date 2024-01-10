from . import _version

__version__ = _version.get_versions()["version"]

from .batman import batman as batman  # noqa: F401
