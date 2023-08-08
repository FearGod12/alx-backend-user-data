#!/usr/bin/env python3
"""
basic authentication module
"""
import base64
import binascii

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
        except binascii.Error:
            None
