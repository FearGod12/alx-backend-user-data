#!/usr/bin/env python3
"""module for hashing of password using bycript
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """hashes a password with salt using bcrypt"""
    password = password.encode("utf-8")
    return bcrypt.hashpw(password, bcrypt.gensalt())
