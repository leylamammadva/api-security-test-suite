"""Automated mass assignment test for VAmPI (OWASP API3:2023)."""

import uuid

import pytest
import requests


@pytest.mark.xfail(
    raises=AssertionError, strict=True,
    reason="F-03: mass assignment allows self-registration as admin",
)
def test_user_cannot_set_admin_flag_during_registration(base_url, login):
    """A client-supplied "admin": true must be ignored during registration."""
    username = f"attacker{uuid.uuid4().hex[:8]}"
    password = "pass123"

    # Register with an extra field the client should never control
    requests.post(
        f"{base_url}/users/v1/register",
        json={
            "username": username,
            "password": password,
            "email": f"{username}@mail.com",
            "admin": True,
        },
    )

    # Log in and read the account's own details
    headers = login(username, password)
    me = requests.get(f"{base_url}/me", headers=headers).json()

    assert me["data"]["admin"] is False, (
        f"Mass assignment: {username} registered itself as admin"
    )