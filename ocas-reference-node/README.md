# OCAS Reference Server (Node.js)

A barebones, runnable implementation of the [Open Charity API Standard (OCAS)](../open-charity-api/). It exists to make the spec real: instead of reading YAML and imagining how the pieces fit, you can start a server, send real requests, and watch real responses come back.

It is built for learning and conformance testing. It is **not** production software: there is no persistence (data lives in memory and resets on restart), no real payment processing, no authentication, and no rate limiting. Think of it as an executable copy of the spec.

## What it does

Implements the core OCAS endpoints in [`src/server.js`](./src/server.js):

- `GET /charity` — capability discovery
- `GET /campaigns`, `GET /campaigns/{id}`
- `GET /funds`, `GET /funds/{id}`
- `POST /donations`, `GET /donations`, `GET /donations/{id}`, `POST /donations/{id}/refund`
- `POST /subscriptions`, `GET /subscriptions`, `GET /subscriptions/{id}`, `PATCH`, `DELETE`
- `GET /receipts/{id}`
- `GET /zakat/calculator`
- `POST /webhooks`, `GET /webhooks`, `DELETE /webhooks/{id}`

It also enforces the parts of OCAS that are easy to get wrong, so you can see the rules in action:

- **Money is integer minor units.** `2500` means £25.00. Decimals are rejected.
- **Asnaf allocations must sum to 100.** A Zakat donation split across the 8 canonical categories has to add up.
- **`interest_purification` can never be Zakat.** Sending `zakat_metadata` with that type is a `422`.
- **Idempotency.** Repeating a `POST /donations` with the same `Idempotency-Key` returns the original donation rather than creating a duplicate.
- **Referential integrity.** Referencing a campaign or fund that doesn't exist is a `422`.

It runs in **public auth mode**, so no credentials are needed to try it.

## Run it

You need Node.js 20 or newer.

```bash
cd ocas-reference-node
npm install
npm start
```

The server starts on `http://localhost:3000`. Then, in another terminal:

```bash
# Discover what the charity supports
curl http://localhost:3000/api/ocas/v1/charity

# Make a Zakat donation split 60/40 across two Asnaf categories
curl -X POST http://localhost:3000/api/ocas/v1/donations \
  -H "Content-Type: application/json" \
  -d '{
    "amount": { "value": 2500, "currency": "GBP" },
    "donation_type": "zakat",
    "donor": { "first_name": "Aisha", "last_name": "Khan", "email": "aisha@example.com" },
    "zakat_metadata": {
      "asnaf_allocation": [
        { "asnaf": "fuqara", "percentage": 60 },
        { "asnaf": "masakin", "percentage": 40 }
      ]
    }
  }'

# Watch a validation rule fire: this one sums to 90, not 100
curl -X POST http://localhost:3000/api/ocas/v1/donations \
  -H "Content-Type: application/json" \
  -d '{
    "amount": { "value": 2500, "currency": "GBP" },
    "donation_type": "zakat",
    "zakat_metadata": {
      "asnaf_allocation": [
        { "asnaf": "fuqara", "percentage": 50 },
        { "asnaf": "masakin", "percentage": 40 }
      ]
    }
  }'
```

## Test it

```bash
npm test
```

The tests in [`test/server.test.js`](./test/server.test.js) double as a small conformance suite: they check the happy path, the validation rules, idempotency, and refunds. They use Node's built-in test runner and `fetch`, so there are no extra dependencies to install.

## How it's organised

```
ocas-reference-node/
├── package.json          One dependency: express.
├── src/
│   ├── server.js         All the routes.
│   ├── store.js          In-memory data + seed data (Hope Mosque Foundation).
│   └── validation.js     The OCAS-specific rules (money, Asnaf, Zakat).
└── test/
    └── server.test.js    Conformance-style tests.
```

It's deliberately small and readable. If you want to build a real OCAS server, this shows you the shapes and the rules; swap the in-memory store for a database, add your auth mode, wire in a real payment processor, and sign your webhooks.

## Where this fits

This is one implementation of OCAS. The spec is the source of truth; if this server and the spec ever disagree, the spec wins (and please [open an issue](https://github.com/the-foundation-stack/Foundation/issues)). There's also a [Python reference server](../ocas-reference-python/) with identical behaviour. Implementations in further languages (Go, PHP, Ruby, Rust) are very welcome as contributions.

Licensed Apache 2.0, same as the rest of The Foundation.
