# API Security Test Suite

![API security tests](https://github.com/leylamammadva/api-security-test-suite/actions/workflows/tests.yml/badge.svg)

A hands-on API security testing project. I test an intentionally vulnerable
API ([VAmPI](https://github.com/erev0s/VAmPI)) for issues from the OWASP API
Security Top 10, automate the checks with Python and pytest, and document each
finding with severity, impact and remediation advice.

## Findings

| ID | Vulnerability | OWASP API Top 10 | Severity | Automated test |
|---|---|---|---|---|
| F-01 | Broken Object Level Authorization on `GET /books/v1/{book_title}` | API1:2023 | High | `tests/test_bola.py` |
| F-02 | Unauthenticated debug endpoint exposes user credentials | API3:2023 | Critical | `tests/test_data_exposure.py` |
| F-03 | Mass assignment allows self-registration as administrator | API3:2023 | Critical | `tests/test_mass_assignment.py` |

Full details, reproduction steps and recommendations: [reports/FINDINGS.md](reports/FINDINGS.md)

## How to run

Requirements: Python 3.10+, Docker Desktop, Git.

1. Start the target API (bound to localhost only):

   ```
   docker run -d -p 127.0.0.1:5000:5000 erev0s/vampi
   ```

2. Install dependencies:

   ```
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Run the tests:

   ```
   pytest -v
   ```

The test suite populates the target's test database automatically and stops
with a clear message if the API is not reachable.

**Expected result:** all tests report `XFAIL` (expected failure). Each test
asserts the *secure* behaviour, so a failing assertion proves that the
vulnerability exists in the target API. The tests are marked `xfail` with
`strict=True`: once a vulnerability is fixed, the test passes and pytest
reports `XPASS(strict)` as a failure, a signal to remove the marker.

## Continuous integration

A GitHub Actions workflow starts VAmPI in Docker and runs the full test suite
on every push and pull request.

## Project structure

```
api-security-test-suite/
├── .github/workflows/tests.yml    # CI: runs the tests on every push
├── first_request.py               # first API request (learning script)
├── bola_manual.py                 # manual BOLA proof of concept
├── mass_assignment_manual.py      # manual mass assignment proof of concept
├── pytest.ini                     # pytest settings
├── requirements.txt
├── tests/
│   ├── conftest.py                # shared fixtures (login, base URL, API check)
│   ├── test_bola.py               # automated BOLA test
│   ├── test_data_exposure.py      # automated data exposure tests
│   └── test_mass_assignment.py    # automated mass assignment test
└── reports/
    └── FINDINGS.md                # vulnerability reports
```

## Roadmap

- [x] Development environment setup
- [x] Target API setup (VAmPI in Docker)
- [x] BOLA: manual check, automated test, report
- [x] Excessive data exposure: automated tests, report
- [x] Mass assignment: manual check, automated test, report
- [ ] GitHub Actions workflow
- [ ] Authentication weaknesses
- [ ] Rate limiting checks
- [ ] Risk summary and remediation plan

## Disclaimer

All testing is done only against an intentionally vulnerable application that
I run locally for learning purposes.