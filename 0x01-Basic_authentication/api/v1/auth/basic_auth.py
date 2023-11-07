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

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """ Method that returns the user email and password from the Base64 decoded value
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        credentials = decoded_base64_authorization_header.split(':', 1)

        return credentials[0], credentials[1]


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
