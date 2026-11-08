"""Automated tests for excessive data exposure on VAmPI (OWASP API3:2023)."""

import requests

BASE_URL = "http://localhost:5000"


def test_debug_endpoint_requires_authentication():
    """The debug endpoint must not answer requests that carry no token."""
    response = requests.get(f"{BASE_URL}/users/v1/_debug")  # no Authorization header
    assert response.status_code in (401, 403, 404), (
        f"Debug endpoint is open to anonymous users (status {response.status_code})"
    )


def test_debug_endpoint_does_not_leak_passwords():
    """No endpoint may return user passwords in its response."""
    response = requests.get(f"{BASE_URL}/users/v1/_debug")
    assert "password" not in response.text, "Passwords are exposed in the response"