#!/usr/bin/env python3
"""Module of session authenticating views.
"""
import os
from typing import Tuple, Union
from flask import Response, abort, jsonify, request

from models.user import User
from api.v1.views import app_views
from models.user import User


@app_views.route("/auth_session/login", methods=["POST"], strict_slashes=False)
def login() -> Union[Tuple[Response, int], Response]:
    """ POST /api/v1/auth_session/login
    Return:
      - User object JSON represented
    """
    email = request.form.get("email")
    if not email or email == "":
        return jsonify({"error": "email missing"}), 400

    password = request.form.get("password")
    if not password or password == "":
        return jsonify({"error": "password missing"}), 400

    try:
        user = User.search({"email": email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404

    if not user:
        return jsonify({"error": "no user found for this email"}), 404

    if user[0].is_valid_password(password):
        from api.v1.app import auth

        session_id = auth.create_session(user[0].id)
        cookie_name = os.getenv("SESSION_NAME")
        response = jsonify(user[0].to_json())
        response.set_cookie(cookie_name, session_id)

        return response
    else:
        return jsonify({"error": "wrong password"}), 401
