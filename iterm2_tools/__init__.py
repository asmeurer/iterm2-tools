"""
iTerm2 tools

License: MIT

"""
from .images import *
from .shell_integration import *

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
