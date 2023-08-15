#!/usr/bin/env python3
"""the flask app module
"""

from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/', methods=["GET"], strict_slashes=False)
def message():
    """returns a message"""
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
