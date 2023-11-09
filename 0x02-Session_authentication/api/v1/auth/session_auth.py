#!/usr/bin/env python3
""" Module of Session Auth
"""
from api.v1.auth.auth import Auth
from models.user import User
from typing import Dict
import uuid


class SessionAuth(Auth):
    """ Session Auth class
    """
    user_id_by_session_id: Dict[str, str] = {}

    def create_session(self, user_id: str = None) -> str:
        """ Create session
        """
        if user_id is None or isinstance(user_id, str) is False:
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ User ID for Session ID
        """
        if session_id is None or isinstance(session_id, str) is False:
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """ Current User
        """
        session_cookie = self.session_cookie(request)

        if session_cookie is None:
            return None

        user_id = self.user_id_for_session_id(session_cookie)

        return User.get(user_id)

    def destroy_session(self, request=None):
        """ Destroy Session
        """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)

        if (request is None or session_id is None) or user_id is None:
            return False
        if session_id in self.user_id_by_session_id:
            del self.user_id_by_session_id[session_id]

        return True
