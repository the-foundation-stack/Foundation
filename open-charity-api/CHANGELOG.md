# Changelog

All notable changes to OCAS will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] — 2026-05-27

Initial draft release. Published under [The Foundation](https://github.com/the-foundation).

### Added
- OpenAPI 3.1 specification covering 16 endpoints and 40 schemas: donations, subscriptions, campaigns, funds, donors, receipts, webhooks, and optional Zakat calculator
- Three discoverable authentication modes: `public`, `api_key`, `oauth2` (with PKCE)
- Polymorphic `tax_relief_declarations[]` with discriminator-based schemes for UK Gift Aid, US 501(c)(3), Canadian CRA, Australian DGR, Irish CHY, German Spendenbescheinigung, French réduction d'impôt, Dutch ANBI, Singaporean IPC, Malaysian §44(6)
- First-class Islamic donation types: `zakat`, `sadaqah`, `sadaqah_jariyah`, `waqf`, `lillah`, `fidya`, `kaffarah`, `qurbani`, `aqiqah`, `interest_purification`
- `ZakatMetadata` schema with the 8 canonical Asnaf categories from Qur'an 9:60
- `QurbaniMetadata` and `AqiqahMetadata` schemas
- Idempotency-Key header support on `POST /donations` and `POST /subscriptions`
- HMAC-SHA256 webhook signing with `OCAS-Signature` header and 5-minute replay window
- Money represented as integer minor units throughout
- Ready-to-import Postman collection with worked examples (Gift Aid, Zakat with Asnaf, Qurbani, refunds, daily Ramadan subscription)
- READMEs translated into Arabic, Urdu, French, Spanish, Turkish, Bahasa Indonesia, Bahasa Melayu
- Six example JSON payloads under `examples/`
- Industry analysis, authentication guide, tax-relief guide, Islamic-giving guide, contributing guide

### Known limitations
- Draft status — breaking changes are possible until `v1.0.0`
- No reference implementation yet (planned)
- Donor-advised funds, donations in stocks/crypto specifics, legacies, in-kind donations, and grant disbursement are intentionally out of scope for v0.1
- Country profiles beyond the 10 listed tax-relief schemes will be added by PR as adopters need them

[Unreleased]: https://github.com/YOUR_USERNAME/Foundation/compare/ocas-v0.1.0...HEAD
[0.1.0]: https://github.com/YOUR_USERNAME/Foundation/releases/tag/ocas-v0.1.0
