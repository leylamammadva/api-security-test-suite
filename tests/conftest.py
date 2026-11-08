"""Shared fixtures for the API security tests."""

import pytest
import requests

BASE_URL = "http://localhost:5000"


@pytest.fixture(scope="function", autouse=True)
def target_api_ready():
    """Stop early with a clear message if VAmPI is not running.

    Also (re)populates the test database before every test, so tests that
    modify data (e.g. changing a password) cannot affect later tests.
    """
    try:
        requests.get(f"{BASE_URL}/createdb", timeout=5)
    except requests.exceptions.ConnectionError:
        pytest.exit(
            "VAmPI is not reachable on localhost:5000. Start it with Docker first.",
            returncode=2,
        )


@pytest.fixture
def base_url():
    return BASE_URL


@pytest.fixture
def login(base_url):
    """Return a function that logs in and gives back the Authorization header."""

    def _login(username, password):
        response = requests.post(
            f"{base_url}/users/v1/login",
            json={"username": username, "password": password},
        )
        token = response.json()["auth_token"]
        return {"Authorization": f"Bearer {token}"}

    return _login