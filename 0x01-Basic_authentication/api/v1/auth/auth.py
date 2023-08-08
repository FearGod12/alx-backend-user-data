#!/usr/bin/env python3
"""the Authentication module"""
from typing import List, TypeVar

from flask import request


class Auth:
    """class to be used for authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        check if path require authentication
        :param path:
        :param excluded_paths:
        :return: False
        """
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        if path in excluded_paths or ((path + "/") in excluded_paths):
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """

        :param request: the flask request object
        :return: None
        """

    def current_user(self, request=None) -> TypeVar('User'):
        """
        returns the current authenticated user
        :param request: flask request object
        :return: the user
        """
        return None
