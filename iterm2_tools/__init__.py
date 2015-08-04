"""
iTerm2 tools

License: MIT

"""
from .images import *

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
