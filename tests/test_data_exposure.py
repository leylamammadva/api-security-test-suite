"""Automated tests for excessive data exposure on VAmPI (OWASP API3:2023)."""

import pytest
import requests


@pytest.mark.xfail(
    raises=AssertionError, strict=True,
    reason="F-02: debug endpoint is open to anonymous users",
)
def test_debug_endpoint_requires_authentication(base_url):
    """The debug endpoint must not answer requests that carry no token."""
    response = requests.get(f"{base_url}/users/v1/_debug")  # no Authorization header
    assert response.status_code in (401, 403, 404), (
        f"Debug endpoint is open to anonymous users (status {response.status_code})"
    )


@pytest.mark.xfail(
    raises=AssertionError, strict=True,
    reason="F-02: debug endpoint returns user passwords",
)
def test_debug_endpoint_does_not_leak_passwords(base_url):
    """No endpoint may return user passwords in its response."""
    response = requests.get(f"{base_url}/users/v1/_debug")
    assert "password" not in response.text, "Passwords are exposed in the response"