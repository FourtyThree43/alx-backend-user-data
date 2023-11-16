#!/usr/bin/env python3
""" Auth Module
"""
from typing import Optional
from sqlalchemy.orm.exc import NoResultFound
import bcrypt
import uuid

from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """Returns the hashed version of a password"""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def _generate_uuid() -> str:
    """Returns a string representation of a new UUID"""
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registers a user"""
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
        else:
            raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """ Credentials validation.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        else:
            return bcrypt.checkpw(password.encode("utf-8"),
                                  user.hashed_password)

    def create_session(self, email: str) -> str:
        """ Create a session ID for the user
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        else:
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)

            return session_id

    def get_user_from_session_id(self, session_id: str) -> Optional[str]:
        """ Get user from session ID
        """
        if session_id is None:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        else:
            return user

    def destroy_session(self, user_id: int) -> None:
        """ Destroy a session
        """
        if user_id is None:
            return None

        try:
            user = self._db.find_user_by(id=user_id)
        except NoResultFound:
            return None
        else:
            self._db.update_user(user.id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """ Get reset password token
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError
        else:
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)

            return reset_token
