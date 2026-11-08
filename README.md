# API Security Test Suite

A hands-on API security testing project. I test an intentionally vulnerable
API ([VAmPI](https://github.com/erev0s/VAmPI)) for issues from the OWASP API
Security Top 10, automate the checks with Python and pytest, and document each
finding with severity, impact and remediation advice.

## Findings

| ID | Vulnerability | OWASP API Top 10 | Severity | Automated test |
|---|---|---|---|---|
| F-01 | Broken Object Level Authorization on `GET /books/v1/{book_title}` | API1:2023 | High | `tests/test_bola.py` |

Full details, reproduction steps and recommendations: [reports/FINDINGS.md](reports/FINDINGS.md)

## How to run

Requirements: Python 3.10+, Docker Desktop, Git.

1. Start the target API (bound to localhost only):

   ```
   docker run -d -p 127.0.0.1:5000:5000 erev0s/vampi
   ```

2. Populate the test database by opening `http://localhost:5000/createdb`
   in a browser.

3. Install dependencies:

   ```
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. Run the tests:

   ```
   pytest -v
   ```

**Expected result:** the tests currently **fail**. This is intentional: each
failing test proves that a vulnerability exists in the target API. After a
vulnerability is fixed, the same test passes.

## Project structure

```
api-security-test-suite/
├── bola_manual.py      # manual BOLA proof of concept
├── tests/
│   └── test_bola.py    # automated BOLA test
├── reports/
│   └── FINDINGS.md     # vulnerability reports
└── requirements.txt
```

## Roadmap

- [x] Development environment setup
- [x] Target API setup (VAmPI in Docker)
- [x] BOLA: manual check, automated test, report
- [ ] Authentication weaknesses
- [ ] Mass assignment
- [ ] Excessive data exposure
- [ ] GitHub Actions workflow

## Disclaimer

All testing is done only against an intentionally vulnerable application that
I run locally for learning purposes.