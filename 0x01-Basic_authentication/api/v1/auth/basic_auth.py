#!/usr/bin/env python3
"""
basic authentication module
"""
import base64
import binascii
from typing import TypeVar

from models.user import User
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """the class to be used for basic authentication"""

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """extracts the base64 authorization header"""
        if authorization_header is None or type(authorization_header) \
                is not str:
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str) \
            -> str:
        """decodes the base64 authorization header"""
        if base64_authorization_header is None \
                or type(base64_authorization_header) is not str:
            return None
        try:
            credential = base64.b64decode(base64_authorization_header
                                          ).decode("utf-8")
            return credential
        except (binascii.Error, UnicodeDecodeError, TypeError):
            None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str)\
            -> (str, str):
        """extracts user credentials from the base64 encoded data"""
        if not decoded_base64_authorization_header \
                or type(decoded_base64_authorization_header) is not str:
            return None, None
        if ":" not in decoded_base64_authorization_header:
            return None, None
        email, passwd = decoded_base64_authorization_header.split(":")
        return email, passwd

    def user_object_from_credentials(self, user_email: str, user_pwd: str)\
            -> TypeVar('User'):
        """finds the User based on the credentials provided"""
        if not user_pwd or not user_email or type(user_email) is not str \
                or type(user_pwd) is not str:
            return None
        result = User.search({'email': user_email})
        if len(result) == 0:
            return None
        for user in result:
            if user.is_valid_password(user_pwd):
                return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """overloads the auth class.
        returns the current user based on the rquest header"""
        if request is None:
            return None
        header = self.authorization_header(request)
        if header is None:
            return None
        base64_header = self.extract_base64_authorization_header(header)
        if base64_header is None:
            return None
        decoded_header = self.decode_base64_authorization_header(base64_header)
        if decoded_header is None:
            return None
        credentials = self.extract_user_credentials(decoded_header)
        if None in credentials:
            return None
        email, passwd = credentials
        user = self.user_object_from_credentials(email, passwd)
        return user
