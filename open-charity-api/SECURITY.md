# Security policy

## Supported versions

OCAS is currently at draft `v0.1.x`. While in draft, only the latest minor version receives fixes. Once `v1.0.0` ships, this policy will be revised to follow SemVer with explicit support windows.

## Reporting a vulnerability

OCAS is a specification, not a running service, so "vulnerabilities" here means design flaws that would lead implementers to build insecure or privacy-violating systems if they followed the spec as written. Examples:

- Authentication flows that leak credentials
- Webhook signing schemes vulnerable to replay or forgery
- Tax-relief declaration shapes that fail to capture data required by HMRC / IRS / equivalent
- PII captured unnecessarily, or transmitted in URL parameters
- Idempotency or refund flows that could cause double-charging
- Anything that would put donors, charities, or implementers at legal or financial risk

**Please do not open a public GitHub issue for security concerns.** Instead:

1. Open a **private security advisory** in this repository: *Security → Advisories → New draft security advisory*
2. Or email the address listed in this file once the project has a maintainer email set up

Expect an initial acknowledgement within **7 days** and a triage decision within **21 days**. Critical issues will be addressed before any other work.

## Coordinated disclosure

If you would like to publish a write-up of the issue, please coordinate timing with the maintainers so a fix or guidance can land alongside disclosure. We will credit reporters in the changelog unless they prefer to remain anonymous.

## Scope

In scope:
- The OpenAPI specification in `spec/openapi.yaml`
- The authentication, webhook, idempotency, and tax-relief design as documented
- Example payloads and the Postman collection (insofar as they would lead implementers astray)

Out of scope:
- Vulnerabilities in any specific implementation of OCAS, please report those to the implementer
- Issues in third-party platforms referenced for comparison (Stripe, JustGiving, Donorbox, etc.)
