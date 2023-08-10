#!/usr/bin/env python3
"""the session Authentication module
"""
import uuid
from models.user import User
from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """session authentication class
    to be used to authenticate users
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        creates a Session ID for a user_id
        :param user_id: user id
        :return: the session id or None
        """
        if user_id is None or type(user_id) != str:
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        retrieves the user id based on the session id
        :param session_id: session id
        :return: the user id or None
        """
        if session_id is None or type(session_id) != str:
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
        returns the current user
        :param request: the request object
        :return: the current authenticated user
        """
        if request is None:
            return None
        session_id = self.session_cookie(request)
        user_id = self.user_id_by_session_id.get(session_id)
        user = User.get(user_id)
        return user

    def destroy_session(self, request=None):
        """
        deletes the user session / logout:
        :param request: the reqest object
        :return: nothing
        """
        if request is None:
            return None
        cookie_value = self.session_cookie(request)
        if self.user_id_for_session_id(cookie_value) is None:
            return False
        self.user_id_by_session_id.pop(cookie_value)
        return True
