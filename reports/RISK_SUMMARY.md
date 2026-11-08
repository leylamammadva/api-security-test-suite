# Risk Summary

This document summarizes the findings in [FINDINGS.md](FINDINGS.md) in terms
of business risk, to support prioritization and remediation planning.

## Risk matrix

Likelihood is rated against an attacker with no prior access (unauthenticated
or a regular registered user). Impact considers confidentiality, integrity
and availability of user data.

| ID | Finding | Likelihood | Impact | Risk | Priority |
|---|---|---|---|---|---|
| F-05 | Unauthorized password change (account takeover) | High | High | **Critical** | 1 |
| F-04 | SQL Injection | High | High | **Critical** | 2 |
| F-03 | Mass assignment (self-registration as admin) | High | High | **Critical** | 3 |
| F-02 | Unauthenticated debug endpoint exposes credentials | High | High | **Critical** | 4 |
| F-01 | Broken Object Level Authorization | Medium | Medium | **High** | 5 |

**Likelihood** is High when exploitation requires no special access or
tooling (a single crafted HTTP request); Medium when it requires a valid
account but no special privileges.

**Impact** is High when the finding exposes or allows modification of other
users' data, or grants elevated privileges; Medium when it exposes data
scoped to individual records without a path to broader compromise.

## Remediation plan

| Priority | ID | Recommended fix | Effort |
|---|---|---|---|
| 1 | F-05 | Add an ownership check on the password change endpoint; require re-authentication | Low |
| 2 | F-04 | Replace string-built SQL with parameterized queries / ORM | Low |
| 3 | F-03 | Restrict registration to an explicit field allow-list | Low |
| 4 | F-02 | Remove or restrict the debug endpoint; never return passwords | Low |
| 5 | F-01 | Add an ownership check on every object-level endpoint | Medium |

All five fixes are low-to-medium effort and do not require architectural
changes, so remediation is recommended before any production deployment of
this codebase.

## Control mapping (ISO/IEC 27001:2022 Annex A)

| ID | Related Annex A controls |
|---|---|
| F-01 | A.8.3 Information access restriction, A.8.2 Privileged access rights |
| F-02 | A.8.9 Configuration management, A.8.24 Use of cryptography (credential storage) |
| F-03 | A.8.2 Privileged access rights, A.8.26 Application security requirements |
| F-04 | A.8.26 Application security requirements, A.8.29 Security testing in development |
| F-05 | A.8.2 Privileged access rights, A.8.5 Secure authentication |

## Summary

| Severity | Count |
|---|---|
| Critical | 4 |
| High | 1 |
| **Total** | **5** |

All five findings stem from insufficient server-side validation: the API
trusts client-supplied input (object identifiers, extra JSON fields, raw
strings used in queries, and the identity in the URL path) without checking
authorization or sanitizing input. A consistent pattern across fixes is to
validate and authorize every request on the server, never relying on the
client to behave correctly.