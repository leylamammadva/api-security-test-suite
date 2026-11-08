"""Automated test for unauthorized password change on VAmPI (OWASP API1:2023)."""

import pytest
import requests


@pytest.mark.xfail(
    raises=AssertionError, strict=True,
    reason="F-05: any user can change another user's password",
)
def test_user_cannot_change_another_users_password(base_url, login):
    """name2 must NOT be able to change name1's password."""
    headers = login("name2", "pass2")

    response = requests.put(
        f"{base_url}/users/v1/name1/password",
        json={"password": "shouldnotwork123"},
        headers=headers,
    )

    assert response.status_code in (401, 403), (
        f"Password change: name2 changed name1's password "
        f"(status {response.status_code})"
    )