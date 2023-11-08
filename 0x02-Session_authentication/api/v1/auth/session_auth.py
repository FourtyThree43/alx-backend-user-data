#!/usr/bin/env python3
""" Module of Session Auth
"""
from typing import Dict
from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    """ Session Auth class
    """
    user_id_by_session_id: Dict = {}

    def create_session(self, user_id: str = None) -> str:
        """ Create session
        """
        if user_id is None or isinstance(user_id, str) is False:
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id

        return session_id
