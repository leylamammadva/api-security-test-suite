"""Automated mass assignment test for VAmPI (OWASP API3:2023)."""

import uuid

import requests

BASE_URL = "http://localhost:5000"


def test_user_cannot_set_admin_flag_during_registration():
    """A client-supplied "admin": true must be ignored during registration."""
    username = f"attacker{uuid.uuid4().hex[:8]}"
    password = "pass123"

    # Register with an extra field the client should never control
    requests.post(
        f"{BASE_URL}/users/v1/register",
        json={
            "username": username,
            "password": password,
            "email": f"{username}@mail.com",
            "admin": True,
        },
    )

    # Log in and read the account's own details
    login = requests.post(
        f"{BASE_URL}/users/v1/login",
        json={"username": username, "password": password},
    )
    headers = {"Authorization": f"Bearer {login.json()['auth_token']}"}
    me = requests.get(f"{BASE_URL}/me", headers=headers).json()

    assert me["data"]["admin"] is False, (
        f"Mass assignment: {username} registered itself as admin"
    )