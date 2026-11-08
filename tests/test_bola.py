"""Automated BOLA test for VAmPI (OWASP API1: Broken Object Level Authorization)."""

import requests

BASE_URL = "http://localhost:5000"


def get_auth_headers(username, password):
    """Log in and return the Authorization header for later requests."""
    response = requests.post(
        f"{BASE_URL}/users/v1/login",
        json={"username": username, "password": password},
    )
    token = response.json()["auth_token"]
    return {"Authorization": f"Bearer {token}"}


def test_user_cannot_read_another_users_book():
    """name1 must NOT be able to read a book owned by another user."""
    headers = get_auth_headers("name1", "pass1")

    # Find a book that belongs to someone else
    books = requests.get(f"{BASE_URL}/books/v1", headers=headers).json()["Books"]
    other_books = [book for book in books if book["user"] != "name1"]
    assert other_books, "No books owned by other users found. Run /createdb first."

    # Try to read it as name1
    title = other_books[0]["book_title"]
    response = requests.get(f"{BASE_URL}/books/v1/{title}", headers=headers)

    # A secure API denies access and never leaks the secret
    assert response.status_code in (403, 404), (
        f"BOLA: name1 read {title} (status {response.status_code})"
    )
    assert "secret" not in response.text, "BOLA: secret leaked to another user"