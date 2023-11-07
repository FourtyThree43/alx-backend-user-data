#!/usr/bin/env python3
""" Module of Basic auth
"""
from api.v1.auth.auth import Auth
from models.user import User
from typing import Tuple, TypeVar
import base64


class BasicAuth(Auth):
    """ Class of Basic auth
    """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """ Method that returns the Base64 part of the Authorization header
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if authorization_header[:6] != "Basic ":
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """ Method that returns the decoded value of a Base64 string
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            return base64.b64decode(
                base64_authorization_header.encode('utf-8')).decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> Tuple[str, str]:
        """ Method that returns the user email and password from the
            Base64 decoded value
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None

        u_email, u_pwd = decoded_base64_authorization_header.split(':', 1)

        return u_email, u_pwd

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """ Method that returns the User instance based on his email and
            password
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        try:
            users = User.search({'email': user_email})
        except Exception:
            return None

        for user in users:
            if user.is_valid_password(user_pwd):
                return user

        return None


if __name__ == "__main__":

    a = BasicAuth()

    # print(a.extract_base64_authorization_header(None))
    # print(a.extract_base64_authorization_header(89))
    # print(a.extract_base64_authorization_header("Holberton School"))
    # print(a.extract_base64_authorization_header("Basic Holberton"))
    # print(a.extract_base64_authorization_header("Basic SG9sYmVydG9u"))
    # print(
    #     a.extract_base64_authorization_header(
    #         "Basic SG9sYmVydG9uIFNjaG9vbA=="))
    # print(a.extract_base64_authorization_header("Basic1234"))

    # print(a.decode_base64_authorization_header(None))
    # print(a.decode_base64_authorization_header(89))
    # print(a.decode_base64_authorization_header("Holberton School"))
    # print(a.decode_base64_authorization_header("SG9sYmVydG9u"))
    # print(a.decode_base64_authorization_header("SG9sYmVydG9uIFNjaG9vbA=="))
    # print(
    #     a.decode_base64_authorization_header(
    #         a.extract_base64_authorization_header(
    #             "Basic SG9sYmVydG9uIFNjaG9vbA==")))

    print(a.extract_user_credentials(None))
    print(a.extract_user_credentials(89))
    print(a.extract_user_credentials("Holberton School"))
    print(a.extract_user_credentials("Holberton:School"))
    print(a.extract_user_credentials("bob@gmail.com:toto1234"))
