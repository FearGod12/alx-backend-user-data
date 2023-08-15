#!/usr/bin/env python3
"""the flask app module
"""

from flask import Flask, jsonify, request, abort
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


@app.route('/sessions', methods=["POST"], strict_slashes=False)
def login():
    """ create a new session for the user, store it the session ID as
    a cookie with key "session_id" on the response"""
    email = request.form.get("email")
    password = request.form.get("password")
    if AUTH.valid_login(email, password) is True:
        sesseion_id = AUTH.create_session(email)
        resp = jsonify({"email": "<user email>", "message": "logged in"})
        resp.set_cookie("session_id", sesseion_id)
        return resp
    abort(401)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")