"""Automated BOLA test for VAmPI (OWASP API1:2023)."""

import pytest
import requests


@pytest.mark.xfail(
    raises=AssertionError, strict=True,
    reason="F-01: BOLA on GET /books/v1/{book_title}",
)
def test_user_cannot_read_another_users_book(base_url, login):
    """name1 must NOT be able to read a book owned by another user."""
    headers = login("name1", "pass1")

    # Find a book that belongs to someone else
    books = requests.get(f"{base_url}/books/v1", headers=headers).json()["Books"]
    other_books = [book for book in books if book["user"] != "name1"]
    assert other_books, "No books owned by other users found."

    # Try to read it as name1
    title = other_books[0]["book_title"]
    response = requests.get(f"{base_url}/books/v1/{title}", headers=headers)

    # A secure API denies access and never leaks the secret
    assert response.status_code in (403, 404), (
        f"BOLA: name1 read {title} (status {response.status_code})"
    )
    assert "secret" not in response.text, "BOLA: secret leaked to another user"