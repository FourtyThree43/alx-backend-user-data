#!/usr/bin/env python3
""" Module of Basic auth
"""
from api.v1.auth.auth import Auth
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

    print(a.decode_base64_authorization_header(None))
    print(a.decode_base64_authorization_header(89))
    print(a.decode_base64_authorization_header("Holberton School"))
    print(a.decode_base64_authorization_header("SG9sYmVydG9u"))
    print(a.decode_base64_authorization_header("SG9sYmVydG9uIFNjaG9vbA=="))
    print(
        a.decode_base64_authorization_header(
            a.extract_base64_authorization_header(
                "Basic SG9sYmVydG9uIFNjaG9vbA==")))
