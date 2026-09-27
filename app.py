import sys
from importlib.metadata import version

from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    return "AutoGSESec is running. Environment check passed."


@app.route("/health")
def health():
    return jsonify(
        status="ok",
        python_version=sys.version.split()[0],
        flask_version=version("flask"),
    )


if __name__ == "__main__":
    app.run(debug=True)