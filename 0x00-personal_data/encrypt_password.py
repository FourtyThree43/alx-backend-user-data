#!/usr/bin/env python3
""" Module for encrypt_password
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """ Method that takes in a password string arguments and returns
        a salted, hashed password, which is a byte string.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ Method that checks if a provided password matches the hashed password.
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
