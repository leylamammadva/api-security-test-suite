# API Security Test Suite

A hands-on API security testing project. I test an intentionally vulnerable API
for issues from the OWASP API Security Top 10, automate the checks with Python
and pytest, and document each finding with risk level and remediation advice.

## Goals

- Learn how APIs work (HTTP, authentication, tokens)
- Find and reproduce common API vulnerabilities (e.g. BOLA)
- Automate security checks with pytest
- Write professional vulnerability reports

## Tech stack

- Python, requests, pytest
- Docker (for the target API)
- Postman / Burp Suite (manual testing)
- Git & GitHub

## Status

Work in progress.

- [x] Development environment setup
- [x] First API request
- [ ] Set up the target API (VAmPI)
- [ ] Manual testing of BOLA and authentication issues
- [ ] Automated tests with pytest
- [ ] Findings report

## Disclaimer

All testing is done only against intentionally vulnerable applications that
I run locally for learning purposes.