# Findings

Target: VAmPI (intentionally vulnerable API), running locally via Docker.

## F-01: Broken Object Level Authorization on GET /books/v1/{book_title}

| Field | Value |
|---|---|
| Severity | High |
| OWASP API Top 10 (2023) | API1: Broken Object Level Authorization |
| CWE | CWE-639: Authorization Bypass Through User-Controlled Key |
| Endpoint | `GET /books/v1/{book_title}` |
| Status | Reproduced |

### Description

The endpoint returns any book, including its `secret` field, to any
authenticated user. It does not check whether the requesting user owns the
book.

### Impact

A user can read confidential data that belongs to other users (including
the admin) by changing the `book_title` value in the request.

### Steps to reproduce

1. Log in as `name1` via `POST /users/v1/login` and obtain the token.
2. Call `GET /books/v1` and pick a book owned by another user
   (e.g. `bookTitle5`, owner `name2`).
3. Call `GET /books/v1/bookTitle5` with the `name1` token.

### Evidence

- Expected: `403 Forbidden` (or `404 Not Found`)
- Actual: `200 OK` with the response body
  `{"book_title": "bookTitle5", "owner": "name2", "secret": "secret for bookTitle5"}`

Script: `bola_manual.py`

### Recommendation

- Compare the authenticated user (from the token) with the book owner on the
  server for every request.
- Return `403` or `404` if they do not match.
- Add an automated authorization test for this endpoint.