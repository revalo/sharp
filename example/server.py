from flask import Flask, render_template
from sharp import Sharp

import os

app = Flask(__name__)
srp = Sharp(app, prefix="/api")


@srp.function()
def repeat(name: str, times: int = 5):
    return name * times


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    srp.generate(os.path.join(os.path.dirname(__file__), "static", "sharp.gen.js"))
    app.run(debug=True)
