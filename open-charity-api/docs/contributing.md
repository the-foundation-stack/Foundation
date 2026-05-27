# Contributing to OCAS

Thank you for considering a contribution. The whole project depends on people who actually run charities, integrate with charities, or study the sector showing up and pushing back when something is wrong.

## Ways to contribute

### 1. Spotted a problem? Open an issue.

Use the issue templates if they exist. If they don't yet, just include:
- **What's wrong** (current behaviour, or current wording in the spec)
- **What should be right** (proposed behaviour or wording)
- **Why it matters** (a real-world scenario where the current spec breaks)

### 2. Want to add a small thing? Open a PR.

Suitable for PRs without prior discussion:
- Typo fixes, broken links, clarifications.
- New examples in the Postman collection.
- New language translations of the README.
- Documentation for a country-specific tax-relief scheme already listed in the enum but not documented.
- Code examples in a new language (curl, Python, JS/TS, Go, Java, PHP, Ruby, Swift, Kotlin, etc.).

PR checklist:
- [ ] If you changed `spec/openapi.yaml`, the spec still validates (`make validate` or run any OpenAPI validator).
- [ ] If you added a field, it's documented in the appropriate `docs/` file.
- [ ] If you added a new enum value (e.g. a new donation type or tax-relief scheme), the rationale is in the PR description.
- [ ] If you added a translation, the file is named `README.{lang}.md` in `docs/i18n/` using a [BCP 47](https://www.rfc-editor.org/rfc/rfc5646) tag.

### 3. Want to change something significant? Open an RFC.

"Significant" includes:
- Breaking changes to existing endpoints or schemas.
- New endpoints.
- New auth modes.
- Anything that requires charities already implementing the spec to update their code.

The RFC process:

1. Open an issue titled `RFC: short title` describing the problem, proposed solution, alternatives considered, and migration path.
2. Discussion happens in the issue for at least 14 days.
3. If consensus emerges, a maintainer marks the issue `rfc-accepted` and the proposer opens the PR.
4. PR is merged once at least two maintainers approve and CI passes.

We deliberately keep this lightweight. We're not the IETF. But we don't want to ship a v1 we have to walk back.

## What we especially want

| Contribution type | Why we want it |
|---|---|
| **Adoption** | A charity actually implementing OCAS. Even partial implementation. Tell us, we'll list you in `ADOPTERS.md`. |
| **Country-specific tax-relief profiles** | We started with the schemes we know; others should be modelled by people who know them. |
| **Translations** | The README in your language reaches developers in your part of the world. |
| **Reference implementations** | A working OCAS server (or client) in a popular stack, ideally MIT/Apache-2.0 licensed and dropped in `examples/`. |
| **Academic input** | Theory papers, distribution models, fraud-detection methods that map to OCAS data. Add to `docs/research/` with a citation and an explainer for developers. |
| **Critique** | "This field is wrong because in our jurisdiction..." — that's the most valuable kind of feedback. |

## Style guide

### For prose
- British English in core docs; American English in `docs/i18n/README.en.md` if it ever exists. Either is fine in PR descriptions.
- Concrete examples over abstract claims.
- Don't editorialise; explain.

### For the OpenAPI spec
- Snake_case for field names. Enum values are also snake_case.
- All times in ISO 8601 UTC (`format: date-time`).
- All amounts as `Money` objects with integer minor units. **Never** decimal floats for money.
- Country codes ISO 3166-1 alpha-2. Language codes BCP 47. Currency codes ISO 4217.
- Optional fields explicitly nullable: `type: [string, "null"]`.
- New enum values added at the end (don't reorder existing ones — clients may have parsing assumptions).

### For commit messages
- First line ≤72 chars, imperative mood ("Add Qurbani metadata schema", not "Added").
- Body, if any, separated by a blank line, explaining *why* not *what*.

## Versioning

We follow [SemVer](https://semver.org) on the **spec** as a whole:

- **PATCH** (`0.1.x`): clarifications in docs, non-substantive changes, new examples.
- **MINOR** (`0.x.0`): new optional fields, new enum values added at the end, new endpoints.
- **MAJOR** (`x.0.0`): breaking changes. Bump the URL major version (`/api/ocas/v2`).

While in `0.x.y`, *any* release may technically break things, but we'll only do so where the cost of preserving back-compat is too high. Once we ship `1.0.0`, breakage requires an RFC and a 12-month parallel-support recommendation.

## Code of conduct

We follow the [Contributor Covenant](https://www.contributor-covenant.org/). Be kind, be specific, assume good faith, push back on ideas not people.

There is one extra norm specific to this project: **no proselytising, in any direction**. Religious motivations for this work are welcome to be discussed openly; religious arguments are not a basis for technical decisions. A field is in or out of the spec because of operational need, not theology. Conversely, no one's contribution is unwelcome because of their beliefs (or lack of them).

## Governance, current state

OCAS is currently maintained by the original author(s). Once two non-author maintainers from different organisations have been onboarded, governance moves to a steering group with:

- 1 charity-side practitioner (someone whose day job is fundraising operations)
- 1 developer (someone shipping integrations against it)
- 1 academic or researcher
- 1 maintainer at large

Decisions by simple majority. Tiebreaker rotates monthly. This is the rough plan; it will be written up properly in `GOVERNANCE.md` when it actually exists.

## Releasing

Maintainers tag releases with annotated git tags `v0.x.y`. CI publishes the spec to the docs site and the Postman collection to the Postman public workspace. Detailed steps are in `RELEASING.md` (TODO).

## Questions

Open a "discussion" rather than an issue for open-ended questions. Email the maintainers (address in `MAINTAINERS.md`) only for security disclosures or private legal/conflict-of-interest matters.
