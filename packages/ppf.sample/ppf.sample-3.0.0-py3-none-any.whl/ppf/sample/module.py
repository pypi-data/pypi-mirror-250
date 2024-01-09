# -*- coding: utf-8 -*-
"""
A module providing functions, classes to be included in the package.
"""

import numpy as np
from .utils import export


@export    # adds myFunction to __all__
def my_function(x):
    """Returns root of x."""

    return np.sqrt(x)
