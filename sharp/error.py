"""Utilities to generate errors within functions.
"""


def error(message, code=400):
    """Generate an error message.
    """

    return {"error": message}, code
