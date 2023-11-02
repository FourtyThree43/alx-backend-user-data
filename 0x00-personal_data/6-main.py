#!/usr/bin/env python3
"""
Main file
"""

hash_password = __import__('encrypt_password').hash_password
is_valid = __import__('encrypt_password').is_valid

password = "MyAmazingPassw0rd"
encrypted_password = hash_password(password)
print(encrypted_password)
print(is_valid(encrypted_password, password))

password_2 = "MyAmazingPassw0rd2"
encrypted_password_2 = hash_password(password_2)
print(encrypted_password_2)
print(is_valid(encrypted_password_2, password_2))

print(is_valid(encrypted_password_2, password))
print(is_valid(encrypted_password, password_2))
