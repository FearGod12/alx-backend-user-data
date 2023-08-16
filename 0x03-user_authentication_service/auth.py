#!/usr/bin/env python3
"""
the authentication module
"""
import uuid

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


def _generate_uuid() -> str:
    """return a string representation of a new UUID
    """
    return str(uuid.uuid4())


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

    def create_session(self, email: str):
        """creates a new db section
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except Exception:
            return

    def get_user_from_session_id(self, session_id: str) -> User:
        """
        gets a user by using the session id
        :param session_id: session id
        :return: User or None
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return

    def destroy_session(self, user_id) -> None:
        """
        destroys a user session
        :param user_id:
        :return: None
        """
        if user_id is not None:
            self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """
        generates a resete token
        :param email: users email
        :return: the generated token
        """

        try:
            user = self._db.find_user_by(email=email)
            token = _generate_uuid()
            self._db.update_user(user.id, reset_token=token)
            return token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """updates the user password
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed = _hash_password(password)
            self._db.update_user(user.id, hashed_password=hashed,
                                 reset_token=None)
        except NoResultFound:
            raise ValueError
