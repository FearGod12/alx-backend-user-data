#!/usr/bin/env python3
"""the flask app module
"""

from flask import Flask, jsonify, request, abort, redirect
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


@app.route('/sessions', methods=["DELETE"], strict_slashes=False)
def logout():
    """
    logs out a user and delete the session id
    """
    session_id = request.cookies.get("session_id")
    if session_id is not None:
        user = AUTH.get_user_from_session_id(session_id)
        if user is not None:
            AUTH.destroy_session(user.id)
            return redirect('/')
    abort(403)


@app.route('/profile', methods=["GET"], strict_slashes=False)
def profile():
    """returns details about a user based on the session id
    """
    session_id = request.cookies.get("session_id")
    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            return jsonify({"email": "{}".format(user.email)}), 200
    abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
