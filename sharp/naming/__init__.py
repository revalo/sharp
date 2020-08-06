"""Collection of ways to name API routes.
"""

import inspect
import os


def default(prefix, func):
    """Default naming scheme, uses the function name in front of the prefix.
    """

    return "/".join([prefix, func.__name__])


def file_based(prefix, func):
    """Adds the name of the file the function is defined in as part of the prefix.

    For instance, a sharp function `add` in `math.py` would have a route, `/math/add`
    """

    full_path = inspect.getfile(func)
    filename, _ = os.path.splitext(os.path.basename(full_path))

    return "/".join([prefix, filename, func.__name__])
