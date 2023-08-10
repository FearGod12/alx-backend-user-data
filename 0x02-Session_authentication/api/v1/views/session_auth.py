#!/usr/bin/env python3
"""the module for handling authentication
"""
import os

from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> str:
    """

    :return:
    """
    email = request.form.get('email')
    if email is None or len(email) == 0:
        return jsonify({"error": "email missing"}), 400
    passwd = request.form.get('password')
    if passwd is None or len(passwd) == 0:
        return jsonify({"error": "password missing"}), 400
    user = None
    try:
        result = User.search({'email': email})
    except Exception:
        pass
    if len(result) == 0:
        return jsonify({"error": "no user found for this email"}), 404
    for each in result:
        if each.is_valid_password(passwd):
            user = each
    if user is None:
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    session_id = auth.create_session(user.id)
    resp = jsonify(user.to_json())
    session_name = os.getenv("SESSION_NAME")
    resp.set_cookie(session_name, session_id)
    return resp


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def logout() -> str:
    """logsout the current user
    """
    from api.v1.app import auth
    return_value = auth.destroy_session(request)
    if return_value is False:
        abort(404)
    return jsonify({}), 200
