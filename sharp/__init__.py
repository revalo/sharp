from flask import request, jsonify
from functools import wraps
from typeguard import check_type

import inspect

from sharp.error import error
from sharp.codegen import codegen

__version__ = "0.0.3"


class Sharp(object):
    def __init__(self, flask_app, prefix=""):
        self.flask_app = flask_app
        self.prefix = prefix
        self.stubs = {}

    def function(self, route=None):
        """Decorator for functions.
        """

        def decorator(f):
            if not route:
                rule = self.prefix + "/" + f.__name__

            self.stubs[f.__name__] = Function(rule, f)

            self.flask_app.add_url_rule(rule, None, wrapper(f), methods=["POST"])
            return f

        return decorator

    def generate(self, output_js_filename):
        with open(output_js_filename, "w") as f:
            f.write(codegen(list(self.stubs.values())))


class Function(object):
    def __init__(self, rule, f):
        self.rule = rule
        self.f = f


def wrapper(f):
    """Internal wrapper, takes a function f, adds type checking and return handling.
    """

    signature = inspect.signature(f)

    @wraps(f)
    def new_func(*args, **kwargs):
        payload = request.json

        new_args = []
        new_kwargs = {}

        try:
            for name in signature.parameters:
                parameter = signature.parameters[name]

                if parameter.default != inspect.Parameter.empty:
                    # Optional parameter.
                    value = payload.get(
                        parameter.name, parameter.default
                    )

                    check_type(parameter.name, value, parameter.annotation)
                    new_kwargs[parameter.name] = value
                else:
                    # Required paramater.
                    if parameter.name not in payload:
                        rv, code = error("Missing parameter %s." % (parameter.name))
                        return jsonify(rv), code

                    value = payload[parameter.name]

                    check_type(parameter.name, value, parameter.annotation)
                    new_args.append(value)
        except TypeError as e:
            rv, code = error(str(e))
            return jsonify(rv), code

        rv = f(*new_args, **new_kwargs)
        code = 200

        if isinstance(rv, tuple):
            rv, code = rv

        return jsonify(rv), code

    return new_func
