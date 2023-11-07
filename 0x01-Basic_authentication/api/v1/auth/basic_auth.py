#!/usr/bin/env python3
""" Module of Basic auth
"""
from api.v1.auth.auth import Auth


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


if __name__ == "__main__":

    a = BasicAuth()

    print(a.extract_base64_authorization_header(None))
    print(a.extract_base64_authorization_header(89))
    print(a.extract_base64_authorization_header("Holberton School"))
    print(a.extract_base64_authorization_header("Basic Holberton"))
    print(a.extract_base64_authorization_header("Basic SG9sYmVydG9u"))
    print(
        a.extract_base64_authorization_header(
            "Basic SG9sYmVydG9uIFNjaG9vbA=="))
    print(a.extract_base64_authorization_header("Basic1234"))
