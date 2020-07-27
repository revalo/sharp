# Sharp

Sharp is an automatic API generation library for Python Flask and JavaScript. You just define functions in the backend, and they are magically available to you on the frontend, with type checking built-in.

## Example

Server-side code,

```python
app = Flask(__name__)
sharp = Sharp(app)

@sharp.function()
def add(a: int, b: int):
    return {
        "result": a + b,
    }
```

And magically on your front-end,

```js
const result = await API.add(4, 3);
```

Sharp can be combined with a modern frontend framework and any web asset bundler, the code-gen is emmitted to a standalone JavaScript file,

```python
sharp.generate("src/js/sharp.gen.js")
```

All Sharp messages are in plain JSON, producing human-readable messages and API routes.

For a more fully fledged example, please see the `example/` directory.

## License

Copyright (c) 2020 Shreyas Kapur. Released under MIT License.
