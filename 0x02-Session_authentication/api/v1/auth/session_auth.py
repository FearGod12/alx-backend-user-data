#!/usr/bin/env python3
"""the session Authentication module
"""
import uuid

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
