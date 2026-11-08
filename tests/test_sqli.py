"""Automated SQL injection test for VAmPI (OWASP API8:2023 - Injection)."""

import pytest
import requests


@pytest.mark.xfail(
    raises=AssertionError, strict=True,
    reason="F-04: SQL injection on GET /users/v1/{username}",
)
def test_username_lookup_is_not_vulnerable_to_sql_injection(base_url, login):
    """A classic ' OR '1'='1 payload must not return another user's data."""
    headers = login("name1", "pass1")

    payload = "doesnotexist123' OR '1'='1"
    response = requests.get(f"{base_url}/users/v1/{payload}", headers=headers)

    assert response.status_code == 404, (
        f"SQL injection: payload returned status {response.status_code} "
        f"instead of 404 (body: {response.text})"
    )