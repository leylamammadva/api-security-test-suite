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


## F-02: Unauthenticated debug endpoint exposes user credentials

| Field | Value |
|---|---|
| Severity | Critical |
| OWASP API Top 10 (2023) | API3: Broken Object Property Level Authorization (excessive data exposure) |
| CWE | CWE-306: Missing Authentication for Critical Function; CWE-200: Exposure of Sensitive Information |
| Endpoint | `GET /users/v1/_debug` |
| Status | Reproduced |

### Description

The endpoint returns the full list of users, including their passwords,
to anyone. It requires no authentication and no token.

### Impact

An anonymous attacker can obtain valid credentials for every user (including
the admin) with a single request and take over all accounts. Because the
passwords are returned in readable form, users who reuse them on other
services are also at risk.

### Steps to reproduce

1. Send `GET http://localhost:5000/users/v1/_debug` without any
   `Authorization` header.
2. Read the `password` field of each user in the response.

### Evidence

- Expected: `401`, `403` or `404`, and no passwords in any response
- Actual: `200 OK` with usernames and passwords of all users

Tests: `tests/test_data_exposure.py`

### Recommendation

- Remove the debug endpoint from production builds, or restrict it to
  authenticated administrators.
- Never return password fields in API responses.
- Store passwords only as salted hashes (e.g. bcrypt or Argon2).
- Review all endpoints for unintended data in responses.