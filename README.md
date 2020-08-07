# Sharp

Sharp is an automatic API generation library for Python Flask and JavaScript.

You write functions in the backend, and Sharp generates the necessary JavaScript to make
API calls to those functions. Sharp also validates argument types based on Python type
hints,

```python
@sharp.function()
def add(a: int, b: int):
    return a + b

sharp.generate("api.js")
```

Now `api.js` can be used from a JavaScript client,

```js
const result = await API.add(4, 3);
```

## Install

```
pip install Flask-Sharp
```

## Basic Example

Server-side code,

```python
app = Flask(__name__)
sharp = Sharp(app)

@sharp.function()
def add(a: int, b: int):
    return a + b
```

Sharp can be combined with a modern frontend framework and any web asset bundler, the code-gen is emmitted to a standalone JavaScript file,

```python
sharp.generate("src/js/sharp.gen.js")
```

And your front-end JavaScript is automatically generated and can be used as,

```js
const result = await API.add(4, 3);
```

On the backend Sharp will automatically validate that both `a` and `b` parameters are valid `ints`.

All Sharp messages are in plain JSON, producing human-readable messages and API routes.

For a more fully fledged example, please see the `example/` directory.

## Naming Routes

By default Sharp will try to name routes by combining the prefix with the function name.
However, Sharp can also name routes based on filenames and any arbitrary custom naming
function,

```python
from sharp import Sharp, naming

srp = Sharp(app, prefix="/api", naming=naming.file_based)
```

In this example, Sharp will name a function names `add` in a file called `math.py`
as `/api/math/add`.

## Type Checking

Sharp can verify basic Python type-hints and deal with default variables,

```python
@srp.function()
def repeat(name: str, times: int = 5):
    return name * times


@srp.function()
def reverse(names: List[str]):
    return names[::-1]
```

## Errors

If Sharp notices a missing parameter or a wrong type, it will generate a JSON response
body `{"error": "Message"}` with a response code 400. To throw errors within a sharp
function,

```python
from sharp.error import error

@sharp.function()
def add(a: int, b: int):
    if a < 0:
        return error("a cannot be negative.")

    return {
        "result": a + b,
    }
```

All API calls from the client return a promise. Errors can be caught with a try-catch or
a `catch` promise callback.

```js
API.add(-4, 3).then((r) => {
    // r is the result of the function.
}).catch((e) => {
    // e is the error message.
});
```

## License

Copyright (c) 2020 Shreyas Kapur. Released under MIT License.
