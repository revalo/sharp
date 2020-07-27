"""Utility to generate errors within functions.
"""


def error(message, code=400):
    return {"error": message}, code
