#!/usr/bin/env python3
""" Auth Module
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """ Returns the hashed version of a password
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
