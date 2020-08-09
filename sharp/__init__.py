from flask import request, jsonify
from functools import wraps
from typeguard import check_type

import inspect
import sharp.naming

from sharp.error import error
from sharp.codegen import codegen
from sharp.function import Function

__version__ = "0.0.6"


class Sharp(object):
    """Public sharp interface.
    """

    def __init__(self, flask_app, prefix="", naming=sharp.naming.default):
        """Initialize a new Sharp object.

        Args:
            flask_app: The flask app object.
            prefix (optional): Will be prefixed to all API routes. For instance, you can
                choose to make this `/api` and all routes will start with `/api`.
            naming: A function that accepts (prefix, function) as parameters and decides
                the route name. Check the `naming` directory for examples.
        """

        self.flask_app = flask_app
        self.prefix = prefix
        self.naming = naming
        self.stubs = {}

    def function(self, route=None):
        """Decorator for defining a new Sharp function.

        Args:
            route (optional): Expose this function at a specific API route, ignores the
                prefix supplied in the `Sharp(prefix="/api")` constructor.
        """

        def decorator(f):
            if not route:
                rule = self.naming(self.prefix, f)
            else:
                rule = route

            self.stubs[f.__name__] = Function(rule, f)

            self.flask_app.add_url_rule(rule, None, wrapper(f), methods=["POST"])
            return f

        return decorator

    def generate(self, output_js_filename, verbose=True):
        """Emit JavaScript API stubs to the supplied filename.
        """

        if verbose:
            for k, v in self.stubs.items():
                print(
                    "[Sharp] Generating definitions for %s at route %s." % (k, v.rule)
                )

        with open(output_js_filename, "w") as f:
            f.write(codegen(list(self.stubs.values())))

        if verbose:
            print("[Sharp] Done code generating client to %s" % (output_js_filename))


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
                    value = payload.get(parameter.name, parameter.default)

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

        return jsonify({"result": rv}), code

    return new_func
