#!/usr/bin/env python3
"""session expiration module
"""
import os
from datetime import datetime, timedelta

from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """implements the mechanism to expire a session cookie
    """
    def __init__(self):
        """class constructor
        """
        try:
            self.session_duration = int(os.getenv("SESSION_DURATION"))
        except (ValueError, TypeError):
            self.session_duration = 0

    def create_session(self, user_id=None):
        """overloads the parent method and
        creates a new session
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        self.user_id_by_session_id[session_id] = {"user_id": user_id,
                                                  "created_at": datetime.now()}
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        finds the user id for the current session
        :param session_id: the session id
        :return: the user id
        """
        if session_id is None:
            return None

        session_dict = self.user_id_by_session_id.get(session_id)
        if session_dict is None:
            return None

        if self.session_duration <= 0:
            return session_dict.get("user_id")

        created_at = session_dict.get("created_at")
        if created_at is None:
            return None
        expiration_time = created_at + timedelta(seconds=self.session_duration)
        if expiration_time < datetime.now():
            return None
        return session_dict.get("user_id")
