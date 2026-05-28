# The Foundation

> Open standards, protocols and shared infrastructure for socially-beneficial software.

We publish specifications, protocols, reference implementations, and research that the world's charities, community organisations, and builders can adopt freely. The work has a particular focus on enabling Muslim developers, academics, and communities to collaborate openly, but the output itself is for everyone, and intentionally vendor-neutral.

The name has two readings, both intended:

- **Foundation** as in `waqf`, a permanent, public endowment of work. Nobody owns it; everybody can build on it.
- **Foundation** as in the base layer of a stack. The primitives that other people's products sit on top of.

## What we publish

- **Open API standards**, vendor-neutral specifications that anyone can adopt
- **Protocols**, interoperability layers for community infrastructure
- **Reference implementations**, working code so adoption isn't theoretical
- **RFCs and research**, published thinking from academics, practitioners, and operators, with proper attribution

Everything is permissively licensed (Apache 2.0 by default), self-hostable, and free of central authorities or mandatory hubs.

## Projects

### [open-charity-api](./open-charity-api/), OCAS

The **Open Charity API Standard**. A vendor-neutral OpenAPI 3.1 specification any charity can adopt to expose donations, subscriptions, campaigns, receipts and tax-relief declarations in a standard shape. First-class support for Gift Aid, US 501(c)(3), Canadian CRA, Australian DGR and seven more international schemes, alongside Zakat (with 8 Asnaf categories), Sadaqah, Waqf, Qurbani, Aqiqah, Fidya, Kaffarah, and interest purification.

📁 [`./open-charity-api/`](./open-charity-api/) · 🌐 7 translated READMEs · *Status: draft v0.1*

> 💡 Want to see it run? The [OCAS reference server](./ocas-reference-node/) is a working implementation you can start in under a minute.

---

### [ocas-reference-node](./ocas-reference-node/), OCAS reference server

A runnable, in-memory implementation of OCAS in Node.js. Start it with `npm install && npm start` and you have a live charity API answering real requests on `localhost`. It enforces the rules that are easy to get wrong: integer-minor-unit money, Asnaf allocations summing to 100, interest purification never counting as Zakat, and idempotency keys. Ships with a conformance-style test suite. Built for learning and conformance testing, not production.

📁 [`./ocas-reference-node/`](./ocas-reference-node/) · 🟢 `npm start` · ✅ tested · *Implements OCAS draft v0.1*

---

### [ocas-reference-python](./ocas-reference-python/), OCAS reference server (Python)

The same reference server, in Python with FastAPI. Identical behaviour and rules to the Node version, so you can see the spec is genuinely portable across stacks. Start it with `uvicorn ocas.server:app --reload` and FastAPI even serves its own interactive docs at `/docs`. Ships with a pytest conformance suite. Built for learning and conformance testing, not production.

📁 [`./ocas-reference-python/`](./ocas-reference-python/) · 🟢 `uvicorn` · ✅ tested · *Implements OCAS draft v0.1*

---

## How to get involved

- **Adopt a spec.** The fastest way to help is to implement one of our standards in a real product and tell us what broke. Adoption stories beat theoretical critique.
- **Open a PR.** Country profiles for tax relief, translations, schema clarifications, additional faith traditions (tithing, ma'aser, daana, dasvandh, etc.), all welcome.
- **Submit an RFC.** Got a theory, a paper, or a protocol idea? Open a discussion. We're especially interested in contributions from universities and researchers in social finance, ethical computing, and equitable distribution.
- **Critique.** If a design choice is wrong, say so. Open an issue with the reasoning and we'll engage with it seriously.

## Principles

1. **Open by default.** Apache 2.0 or equivalent. No "open core" with paid extensions.
2. **Vendor-neutral.** Specs don't presume Stripe, PayPal, AWS, or any single provider.
3. **Self-hostable.** No mandatory central registry, hub, or gateway.
4. **Religiously informed where it matters, religiously neutral on the surface.** We model Zakat properly because it has technical requirements (the 8 Asnaf, hawl, nisab, purification rules); we don't proselytise.
5. **Practical over performative.** Working code, real adopters, concrete examples. Less manifesto, more YAML.

## Code of conduct

All projects under The Foundation adhere to the [Contributor Covenant v2.1](https://www.contributor-covenant.org/version/2/1/code_of_conduct/), with one explicit additional norm: **no proselytising, in any direction**. Keep the work technical; keep the spirit welcoming.

---

*The Foundation is currently a brand and a publishing umbrella, not yet a formally incorporated entity. If you're interested in helping it become one, particularly as a non-profit or charitable trust, please open a discussion.*
