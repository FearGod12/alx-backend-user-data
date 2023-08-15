#!/usr/bin/env python3
"""the flask app module
"""

from flask import Flask, jsonify, request
from auth import Auth

AUTH = Auth()
app = Flask(__name__)


@app.route('/', methods=["GET"], strict_slashes=False)
def message():
    """returns a message"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=["POST"], strict_slashes=False)
def users():
    """registers a user iof it does not exist
    """
    email = request.form.get("email")
    password = request.form.get("password")
    if email is None or password is None:
        return
    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": "{}".format(email), "message":
                        "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
