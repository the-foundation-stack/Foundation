# Security policy

This file covers vulnerability reporting for **The Foundation** as a whole. Each project may also have its own `SECURITY.md` with project-specific scope (see e.g. [`open-charity-api/SECURITY.md`](./open-charity-api/SECURITY.md)).

## Reporting a vulnerability

The Foundation publishes specifications, not running services. So "vulnerabilities" here means **design flaws that would lead implementers to build insecure or privacy-violating systems** if they followed our specs as written.

**Please do not open a public GitHub issue for security concerns.** Instead, use one of:

1. **Private security advisories** in this repository: *Security → Advisories → New draft security advisory*
2. **Email** the maintainer address listed on the org profile (set this up once the org exists)

Expect an initial acknowledgement within **7 days** and a triage decision within **21 days**. Critical issues are addressed before any other work.

## What's in scope

- Any published specification under this repository
- Authentication, signing, idempotency, and tax-handling design across all projects
- Example payloads and reference implementations that could lead implementers astray

## What's out of scope

- Vulnerabilities in specific implementations of our specs — please report those to the implementer
- Third-party services referenced for comparison (Stripe, JustGiving, etc.)
- Issues in upstream tools (OpenAPI tooling, Postman, etc.) — report upstream

## Coordinated disclosure

If you'd like to publish a write-up, please coordinate timing with the maintainers so a fix or guidance can land alongside disclosure. We credit reporters in the relevant project's `CHANGELOG.md` unless they prefer to remain anonymous.
