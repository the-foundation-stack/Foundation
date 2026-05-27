# Open Charity API Standard (OCAS)

> An open, vendor-neutral specification for charity donation APIs.
> Built so any charity, small mosque, global NGO, food bank, hospice, can be integrated with by any developer, in any app, anywhere in the world.

[![License: Apache-2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Spec: OpenAPI 3.1](https://img.shields.io/badge/Spec-OpenAPI_3.1-green.svg)](spec/openapi.yaml)
[![Status: Draft](https://img.shields.io/badge/Status-Draft_v0.1-orange.svg)](#)

**Read this in another language:** [العربية](docs/i18n/README.ar.md) · [اردو](docs/i18n/README.ur.md) · [Français](docs/i18n/README.fr.md) · [Español](docs/i18n/README.es.md) · [Türkçe](docs/i18n/README.tr.md) · [Bahasa Indonesia](docs/i18n/README.id.md) · [Bahasa Melayu](docs/i18n/README.ms.md)

---

## Why this exists

If you've ever tried to build software that talks to charities, you've probably hit the same wall most developers hit: there is no standard. Every charity that does expose a way to accept donations programmatically does so differently. Most don't expose anything at all. They rely on third-party platforms (JustGiving, Donorbox, Enthuse, Fundraise Up, GoFundMe) which each have their own APIs, their own data models, their own auth, and their own fees.

That fragmentation has a cost. It means:

- A developer who wants to add "donate to charity X" inside their app has to integrate with N different systems.
- Charities that can't afford a paid platform have no way to be programmatically reachable at all.
- Smaller faith-based, community, and grassroots charities are effectively invisible to the wider tech ecosystem.
- Standard concepts like Gift Aid, recurring giving, Zakat categorisation, and tax receipts are reimplemented (badly) over and over.

**Open Charity API Standard (OCAS)** is an attempt to fix this. It is a free, open specification any charity can adopt to expose donations, subscriptions, campaigns, receipts, and tax-relief metadata in a consistent shape. Any app can then integrate with any compliant charity with the same code path.

This project is intentionally:

- **Vendor-neutral.** Not tied to Stripe, PayPal, or any single payment processor.
- **Faith- and ideology-neutral on the surface.** Works equally well for a secular food bank and a mosque.
- **Religiously-aware where it matters.** First-class support for Zakat, Sadaqah, Waqf, Lillah, Fidya, Kaffarah, Qurbani, Aqiqah, alongside Gift Aid, 501(c)(3), DGR, ANBI and other tax-relief schemes.
- **Self-hostable.** A charity can implement OCAS on its own server. No central authority. No mandatory hub.

## Who this is for

| If you are... | OCAS gives you... |
|---|---|
| A **charity** | A spec you can implement (or ask your CRM vendor to implement) so any app can take donations on your behalf. |
| An **app developer** | A single integration target. Implement OCAS once and you can donate to any OCAS-compliant charity. |
| A **CRM / fundraising platform** | A standard adapter you can expose, freeing your customers from lock-in and making your platform more attractive. |
| A **researcher or academic** | A clean data shape you can build theory and tooling on top of (Zakat distribution models, fairness in giving, fraud detection, impact tracking). |
| A **regulator** | A reference for what good interop looks like, including standardised audit fields. |

## The bigger picture, The Foundation

OCAS is the first project published under **[The Foundation](../README.md)**, a home for **open standards, protocols and shared infrastructure for socially-beneficial software**, with a particular focus on enabling Muslim developers, academics, and communities to collaborate openly. The work itself is for everyone; the lens is one of public benefit, ethical computing, and refusing to let critical community infrastructure stay locked behind proprietary gateways.

The name is deliberate. *Foundation* in the sense of `waqf`, a permanent, public endowment of work that nobody owns and everybody can build on. *Foundation* in the sense of the base layer of a stack: standards, protocols, primitives that other people's products sit on top of.

The ambition is that universities, researchers and professors with theories about social finance, ethical computing, halal payment rails, equitable distribution, and similar topics can publish reference implementations under The Foundation that any developer can build on, with proper attribution. Pull requests, RFCs, and research papers are all welcome.

If you're building something Islamic-finance-aware, community-benefit-aware, or values-aligned in some other way and you find yourself reinventing wheels, this is the place to bring the wheel and let others use it.

## What's in this directory

```
Foundation/                         <- repo root
├── README.md                       <- about The Foundation umbrella
├── LICENSE                         <- Apache 2.0 (covers the whole repo)
├── NOTICE
├── CODE_OF_CONDUCT.md
├── .gitignore
│
└── open-charity-api/               <- you are here
    ├── README.md
    ├── CHANGELOG.md
    ├── SECURITY.md
    ├── spec/
    │   └── openapi.yaml             <- The OpenAPI 3.1 specification
    ├── postman/
    │   └── OCAS.postman_collection.json
    ├── docs/
    │   ├── industry-analysis.md     <- Why these endpoints, why these fields
    │   ├── authentication.md        <- API keys, OAuth, public mode
    │   ├── gift-aid-and-tax.md      <- UK Gift Aid + international equivalents
    │   ├── islamic-considerations.md <- Zakat, Sadaqah, Waqf, Qurbani, etc.
    │   ├── contributing.md          <- How to propose changes
    │   └── i18n/                    <- README translated into 7+ languages
    └── examples/
        └── (worked JSON payloads + reference implementations welcome via PR)
```

## Quick start (for a developer integrating)

Every OCAS-compliant charity exposes (at minimum) the following base URL pattern:

```
https://{charity-domain}/api/ocas/v1
```

The minimum viable donation flow is two HTTP calls:

**1. Get charity info** (public, no auth required):

```http
GET /charity
```

This tells you the charity's legal name, registration numbers (e.g. UK Charity Commission number, EIN, ABN), supported currencies, supported donation types, supported tax-relief schemes, and which auth mode it uses.

**2. Create a donation:**

```http
POST /donations
Content-Type: application/json
Authorization: Bearer {token}      # if the charity requires auth; otherwise omit

{
  "amount": { "value": 5000, "currency": "GBP" },   // 5000 = £50.00 (minor units)
  "donation_type": "sadaqah",
  "donor": {
    "email": "donor@example.com",
    "first_name": "Aisha",
    "last_name": "Khan",
    "address": { "line1": "...", "postcode": "...", "country": "GB" }
  },
  "gift_aid": { "declared": true, "declaration_text_version": "v1" },
  "campaign_id": "ramadan-2026",
  "anonymous": false,
  "message": "For my late father, may Allah have mercy on him."
}
```

The charity returns a `donation_id` and a `payment_intent` you can complete with the charity's chosen payment processor, or, if the charity issues a `redirect_url`, you simply send the donor there.

That's it. Full reference in [`spec/openapi.yaml`](spec/openapi.yaml).

## Authentication, in one paragraph

Charities can run OCAS in one of three modes, declared in `GET /charity`:

- `public`, no auth required for `POST /donations`. Anyone can donate. (Read-only listing endpoints are still public.) Best for small charities who want to be maximally embeddable.
- `api_key`, a static API key in the `Authorization: Bearer` header. Best for trusted partner apps.
- `oauth2`, full OAuth 2.0 with PKCE. Used when individual donors need accounts and donation history. Charities can expose their own authorisation server, or delegate to a third party.

Apps integrating with multiple charities just read the mode from `GET /charity` and adapt. Details in [`docs/authentication.md`](docs/authentication.md).

## Tax relief (Gift Aid and friends)

The spec models tax-relief declarations generically. A UK Gift Aid declaration is just one instance of a `tax_relief_declaration` object; a US 501(c)(3) tax receipt is another; Australia's DGR, Canada's CRA receipts, Germany's Spendenbescheinigung, Ireland's CHY3/CHY4, Netherlands' ANBI, all supported through the same shape with country-specific fields. See [`docs/gift-aid-and-tax.md`](docs/gift-aid-and-tax.md).

## Islamic giving categories

Zakat, Sadaqah, Sadaqah Jariyah, Lillah, Waqf, Fidya, Kaffarah, Qurbani/Udhiya, and Aqiqah are first-class `donation_type` values. A `zakat_metadata` object lets charities expose which of the eight Quranic categories of recipients (Asnaf) a Zakat donation will flow to. A separate (optional) `/zakat/calculator` endpoint lets apps offer Nisab-aware Zakat calculation. See [`docs/islamic-considerations.md`](docs/islamic-considerations.md).

None of this is required. A charity that only takes generic donations can ignore those fields entirely.

## How to contribute

Three ways:

1. **Open an issue.** Spotted a missing field, an unsupported jurisdiction, an ambiguity? Tell us.
2. **Open a pull request.** Especially welcome: new language translations, country-specific tax-relief profiles, reference server implementations in your stack of choice.
3. **Adopt the spec.** The single most valuable thing a charity can do is implement it. Tell us when you do, we'll list you in `ADOPTERS.md`.

See [`docs/contributing.md`](docs/contributing.md) for the full process, including the RFC procedure for breaking changes.

## Governance and license

OCAS is licensed under the **Apache License 2.0**. The spec, schemas, and reference materials are free to use commercially, fork, modify, and embed. No royalties, no attribution gymnastics, just keep the licence header and don't sue us.

Long-term governance is intended to be a lightweight steering group of charity practitioners, developers, and at least one academic; until that exists, decisions are made by maintainers via the RFC process in `docs/contributing.md`.

## A note on intent

This project is being built in the belief that good infrastructure is itself an act of charity, sadaqah jariyah, if you like, and that the technical community has a duty to make it easier, not harder, for money to reach people who need it. If even one extra pound, dollar, ringgit or rupee reaches a hungry person because two systems could talk to each other, the work was worth it.

Contributions, critique, and corrections all welcome.

---

**Maintainers:** see [`MAINTAINERS.md`](MAINTAINERS.md) *(to be created when first non-author maintainer joins)*
**Security disclosure:** see [`SECURITY.md`](SECURITY.md) *(coming soon)*
**Code of conduct:** see [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md) *(coming soon, Contributor Covenant)*
