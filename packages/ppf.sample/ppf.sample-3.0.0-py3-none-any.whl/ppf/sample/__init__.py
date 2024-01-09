# -*- coding: utf-8 -*-
"""
Sample
++++++

Sample is a package demonstrating how to package Python code
"""

try:
    from importlib.metadata import version
except ImportError:
    from importlib_metadata import version


__version__ = version(__name__)

# import every function, class, etc. that should be visible in the package
from .module import *

del module
del utils
