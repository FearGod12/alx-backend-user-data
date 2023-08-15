#!/usr/bin/env python3
"""
the authentication module
"""

import bcrypt
from sqlalchemy.orm.exc import NoResultFound

from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """
    hashes a password
    :param password: a string representing the password
    :return: a salted hashed password in  bytes
    """
    if password:
        hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        return hashed


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """class constructor
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        registers a user
        :param email: users email
        :param password: users password
        :return: the user instance
        """
        try:
            user = self._db.find_user_by(email=email)
            if user is not None:
                raise ValueError("User {} already".format(email))
        except NoResultFound:
            hashed = _hash_password(password)
            user = self._db.add_user(email, hashed)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """checks if login credentials are valid
        """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode("utf-8"),
                                  user.hashed_password)
        except Exception:
            return False
