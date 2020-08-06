"""Modules related to generating JavaScript stubs based on functions.
"""

from jinja2 import Template
import os
import inspect


# Load JS Jinja2 templates.
JS_DIR = os.path.join(os.path.dirname(__file__), "js")

with open(os.path.join(JS_DIR, "function.js")) as f:
    function_template = Template(f.read())

with open(os.path.join(JS_DIR, "class.js")) as f:
    class_template = Template(f.read())


def gen_function(function):
    """Generate JavaScript stub for a single function.
    """

    signature = inspect.signature(function.f)
    parameters = [x for x in signature.parameters]

    return function_template.render(
        name=function.f.__name__, parameters=parameters, route=function.rule
    )


def codegen(functions):
    """Generate JavaScript for a list of functions and encapsulate in a static class.

    Args:
        functions: List of Sharp Function Metadata objects.

    Returns:
        String of generate client-side code.
    """

    functions = "\n\n".join(gen_function(f) for f in functions)
    return class_template.render(functions=functions)
