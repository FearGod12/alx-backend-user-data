#!/usr/bin/env python3
"""
the authentication module
"""

import bcrypt


def _hash_password(password: str) -> bytes:
    """
    hashes a password
    :param password: a string representing the password
    :return: a salted hashed password in  bytes
    """
    if password:
        hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        return hashed
