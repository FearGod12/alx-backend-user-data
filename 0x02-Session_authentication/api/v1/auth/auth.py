#!/usr/bin/env python3
"""the Authentication module"""
import os
from typing import List, TypeVar

from flask import request


class Auth:
    """class to be used for authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        check if path require authentication
        :param path:
        :param excluded_paths:
        :return: False/True
        """
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        if path in excluded_paths or ((path + "/") in excluded_paths):
            return False
        for each in excluded_paths:
            if each.endswith("*"):
                if path.startswith(each[:-1]):
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """

        :param request: the flask request object
        :return: the authorization header
        """
        if request is None or request.headers.get("Authorization", None)\
                is None:
            return None
        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """
        returns the current authenticated user
        :param request: flask request object
        :return: the user
        """
        return None

    def session_cookie(self, request=None):
        """
        returns the session cookie value from  request
        :param request: the request object
        :return: cookie value
        """
        if request is None:
            return None
        my_session_id = os.getenv("SESSION_NAME")
        return request.cookies.get(my_session_id)
