#!/usr/bin/env python3
"""the test integration module to test all the endpoints in the flask app
"""

import requests


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"

base_url = "http://127.0.0.1:5000"


def register_user(email: str, password: str) -> None:
    """registers a user
    """
    data = {"email": email, "password": password}
    endpoint = base_url + "/users"
    resp = requests.post(endpoint, data)
    content = resp.json()
    assert resp.status_code == 200
    assert content == {"email": "{}".format(email), "message": "user created"}


def log_in_wrong_password(email: str, password: str) -> None:
    """check if using wrong credentials to login
    returns the right message and status code"""
    data = {"email": email, "password": password}
    endpoint = base_url + "/sessions"
    resp = requests.post(endpoint, data)
    assert resp.status_code == 401


def log_in(email: str, password: str) -> str:
    """
    checks if login endpoint works as expected
    :param email: user email
    :param password: user password
    :return: json data
    """
    data = {"email": email, "password": password}
    endpoint = base_url + "/sessions"
    resp = requests.post(endpoint, data)
    assert resp.status_code == 200
    assert resp.json() == {"email": "{}".format(email), "message": "logged in"}
    assert resp.cookies.get("session_id") is not None
    return resp.cookies.get("session_id")


def profile_unlogged() -> None:
    """Test user's profile unlogged
    """
    url = base_url + "/profile"
    cookies = {'session_id': ""}
    resp = requests.get(url, cookies=cookies)
    assert resp.status_code == 403


def profile_logged(session_id: str) -> None:
    """tests if profile is logged
    """
    url = base_url + "/profile"
    cookies = {"session_id": session_id}
    resp = requests.get(url, cookies=cookies)
    assert resp.json() == {"email": "{}".format(EMAIL)}
    assert resp.status_code == 200


def log_out(session_id: str) -> None:
    """test if log_out works as expected
    """
    url = base_url + "/sessions"
    cookies = {"session_id": session_id}
    resp = requests.delete(url, cookies=cookies)
    assert resp.status_code == 200


def reset_password_token(email: str) -> str:
    """
    tests users reset password token
    :param email: user email
    :return: the reset token
    """
    url = base_url + "/reset_password"
    data = {"email": email}
    resp = requests.post(url, data)
    token = resp.json().get("reset_token")
    assert resp.json() == {"email": "{}".format(email),
                           "reset_token": "{}".format(token)}
    assert resp.status_code == 200
    return token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """ test the endpoint for updating password"""
    url = base_url + "/reset_password"
    data = {"email": email, "reset_token": reset_token,
            "new_password": new_password}
    resp = requests.put(url, data)
    assert resp.json() == {"email": "{}".format(email),
                           "message": "Password updated"}
    assert resp.status_code == 200


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
