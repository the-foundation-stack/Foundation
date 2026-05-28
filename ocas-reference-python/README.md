# OCAS Reference Server (Python)

A barebones, runnable implementation of the [Open Charity API Standard (OCAS)](../open-charity-api/), built with FastAPI. It's a sibling to the [Node.js reference server](../ocas-reference-node/): same behaviour, same seed data, different language, so you can see the spec is genuinely portable.

It's built for learning and conformance testing. It is **not** production software: there's no persistence (data lives in memory and resets on restart), no real payment processing, no authentication, and no rate limiting. Think of it as an executable copy of the spec.

## What it does

Implements the core OCAS endpoints in [`ocas/server.py`](./ocas/server.py):

- `GET /charity` — capability discovery
- `GET /campaigns`, `GET /campaigns/{id}`
- `GET /funds`, `GET /funds/{id}`
- `POST /donations`, `GET /donations`, `GET /donations/{id}`, `POST /donations/{id}/refund`
- `POST /subscriptions`, `GET /subscriptions`, `GET /subscriptions/{id}`, `PATCH`, `DELETE`
- `GET /receipts/{id}`
- `GET /zakat/calculator`
- `POST /webhooks`, `GET /webhooks`, `DELETE /webhooks/{id}`

It enforces the same rules as the Node server, the parts of OCAS that are easy to get wrong:

- **Money is integer minor units.** `2500` means £25.00. Decimals are rejected.
- **Asnaf allocations must sum to 100.** A Zakat donation split across the 8 canonical categories has to add up.
- **`interest_purification` can never be Zakat.** Sending `zakat_metadata` with that type is a `422`.
- **Idempotency.** Repeating a `POST /donations` with the same `Idempotency-Key` returns the original donation rather than creating a duplicate.
- **Referential integrity.** Referencing a campaign or fund that doesn't exist is a `422`.

It runs in **public auth mode**, so no credentials are needed.

## Run it

You need Python 3.10 or newer.

```bash
cd ocas-reference-python
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn ocas.server:app --reload
```

The server starts on `http://localhost:8000`. Then, in another terminal:

```bash
# Discover what the charity supports
curl http://localhost:8000/api/ocas/v1/charity

# Make a Zakat donation split 60/40 across two Asnaf categories
curl -X POST http://localhost:8000/api/ocas/v1/donations \
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
```

Because this is built with FastAPI, you also get **interactive API docs for free** at `http://localhost:8000/docs` once the server is running. Note these are FastAPI's auto-generated docs describing *this server*; the canonical OCAS spec lives in [`../open-charity-api/`](../open-charity-api/).

## Test it

```bash
pip install -r requirements.txt    # includes pytest + httpx
pytest
```

The tests in [`tests/test_server.py`](./tests/test_server.py) double as a small conformance suite: happy path, validation rules, idempotency, and refunds. They use FastAPI's `TestClient`, so no running server is needed.

## How it's organised

```
ocas-reference-python/
├── requirements.txt      FastAPI, uvicorn, plus pytest + httpx for tests.
├── ocas/
│   ├── server.py         All the routes.
│   ├── store.py          In-memory data + seed data (Hope Mosque Foundation).
│   └── validation.py     The OCAS-specific rules (money, Asnaf, Zakat).
└── tests/
    └── test_server.py    Conformance-style tests.
```

## Where this fits

This is one implementation of OCAS, alongside the [Node.js one](../ocas-reference-node/). The spec is the source of truth; if any implementation and the spec disagree, the spec wins (and please [open an issue](https://github.com/the-foundation-stack/Foundation/issues)). Implementations in other languages — Go, PHP, Ruby, Rust — are very welcome as contributions.

Licensed Apache 2.0, same as the rest of The Foundation.
