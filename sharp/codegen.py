"""Modules related to generting JavaScript stubs based on functions.
"""

from jinja2 import Template
import os
import inspect

JS_DIR = os.path.join(os.path.dirname(__file__), "js")

with open(os.path.join(JS_DIR, "function.js")) as f:
    function_template = Template(f.read())

with open(os.path.join(JS_DIR, "class.js")) as f:
    class_template = Template(f.read())


def gen_function(function):
    signature = inspect.signature(function.f)
    parameters = [x for x in signature.parameters]

    return function_template.render(
        name=function.f.__name__, parameters=parameters, route=function.rule
    )


def codegen(functions):
    functions = "\n\n".join(gen_function(f) for f in functions)

    return class_template.render(functions=functions)
