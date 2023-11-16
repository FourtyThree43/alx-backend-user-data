#!/usr/bin/env python3
""" End-to-end (E2E) integration test for Flask 'app'
"""
import requests

EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"
BASE_URL = "http://localhost:5000"


def register_user(email: str, password: str) -> None:
    """Test register_user() function"""
    url = f"{BASE_URL}/users"
    data = {"email": email, "password": password}

    response = requests.post(url, data=data)
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "user created"}

    response = requests.post(url, data=data)
    assert response.status_code == 400
    assert response.json() == {
        "email": email,
        "message": "user already exists"
    }


def log_in_wrong_password(email: str, password: str) -> None:
    """Test log_in() function"""
    url = f"{BASE_URL}/sessions"
    data = {"email": email, "password": password}

    response = requests.post(url, data=data)
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """Test log_in() function"""
    url = f"{BASE_URL}/sessions"
    data = {"email": email, "password": password}

    response = requests.post(url, data=data)
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "logged in"}

    session_id = response.cookies.get("session_id")

    response = requests.post(url, data=data)
    assert response.status_code == 400
    assert response.json() == {"email": email, "message": "already logged in"}

    return session_id


def profile_unlogged() -> None:
    """Test profile() function"""
    url = f"{BASE_URL}/profile"

    response = requests.get(url)
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """Test profile() function"""
    url = f"{BASE_URL}/profile"
    cookies = {"session_id": session_id}

    response = requests.get(url, cookies=cookies)
    assert response.status_code == 200
    assert response.json() == {"email": EMAIL}


def log_out(session_id: str) -> None:
    """Test log_out() function"""
    url = f"{BASE_URL}/sessions"
    cookies = {"session_id": session_id}

    response = requests.delete(url, cookies=cookies)
    assert response.status_code == 200
    assert response.json() == {"message": "Bienvenue"}


def reset_password_token(email: str) -> str:
    """Test reset_password_token() function"""
    url = f"{BASE_URL}/reset_password"
    data = {"email": email}

    response = requests.post(url, data=data)
    assert response.status_code == 200

    reset_token = response.json().get("reset_token")

    response = requests.post(url, data=data)
    assert response.status_code == 400
    assert response.json() == {"email": email, "message": "already reseted"}

    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Test update_password() function"""
    url = f"{BASE_URL}/reset_password"
    data = {
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password
    }

    response = requests.put(url, data=data)
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "Password updated"}

    response = requests.put(url, data=data)
    assert response.status_code == 400
    assert response.json() == {"email": email, "message": "already reseted"}

    response = requests.put(url,
                            data={
                                "email": email,
                                "reset_token": "wrong",
                                "new_password": new_password
                            })
    assert response.status_code == 403
    assert response.json() == {"email": email, "message": "Unauthorized"}


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
