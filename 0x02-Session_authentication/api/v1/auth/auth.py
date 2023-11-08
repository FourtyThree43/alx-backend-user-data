#!/usr/bin/env python3
""" Module of auth
"""
from flask import request
from typing import List, TypeVar
from os import getenv


class Auth:
    """ Auth class
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Require auth
        """
        if path is None or excluded_paths is None or excluded_paths == []:
            return True
        if path[-1] != '/':
            path += '/'
        if path in excluded_paths:
            return False
        for i in excluded_paths:
            if i[-1] == '*':
                if i[:-1] in path:
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """ Authorization header
        """
        if request is None:
            return None
        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        """ Current user
        """
        return None

    def session_cookie(self, request=None):
        """ Session cookie
        """
        if request is not None:
            cookie_name = getenv('SESSION_NAME')
            return request.cookies.get(cookie_name)
        return None
