"""In-memory data store for the OCAS reference server.

Deliberately uses plain Python dicts and lists instead of a database. The point
of this reference implementation is to show how the OCAS shapes fit together,
not how to run a production service. Everything here resets when the process
restarts.

The seed data mirrors the examples in the OpenAPI spec: Hope Mosque Foundation
in Birmingham, with a Ramadan campaign and a food-bank fund.
"""

from __future__ import annotations

import time
from datetime import datetime, timezone


def now_iso() -> str:
    """Current time as an ISO 8601 string in UTC."""
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


# Counter-based ID generation. Real implementations should use UUIDs or ULIDs;
# this keeps the demo readable.
_counter = 1000


def next_id(prefix: str) -> str:
    global _counter
    _counter += 1
    return f"{prefix}_{_counter:x}{int(time.time() * 1000):x}"


db: dict = {
    "charity": {
        "name": "Hope Mosque Foundation",
        "legal_name": "Hope Mosque Foundation Ltd",
        "description": "A community mosque and food bank serving Birmingham since 1998.",
        "website_url": "https://hopemosque.example.org",
        "logo_url": "https://hopemosque.example.org/logo.png",
        "registration_numbers": [
            {"jurisdiction": "GB", "type": "charity_commission", "value": "1234567"},
        ],
        "auth": {
            # This reference server runs in 'public' mode so you can try it with
            # no credentials. A real charity would more likely use 'api_key'.
            "mode": "public",
            "discovery_url": None,
            "key_request_url": None,
            "supported_scopes": [],
        },
        "supported_currencies": ["GBP", "USD", "EUR"],
        "supported_donation_types": [
            "general",
            "zakat",
            "sadaqah",
            "sadaqah_jariyah",
            "qurbani",
            "aqiqah",
        ],
        "supported_tax_relief_schemes": ["uk_gift_aid"],
        "supported_frequencies": ["monthly", "weekly", "daily"],
        "payment_methods": ["card", "bacs_direct_debit", "apple_pay", "google_pay"],
        "time_locked_types": [],
        "shariah_compliance": {
            "scholars_or_board": "Birmingham Council of Mosques",
            "fatwa_references": [
                {
                    "issuer": "National Zakat Foundation",
                    "year": 2024,
                    "url": "https://nzf.example.org/fatwa/zakat-administration",
                },
            ],
            "hundred_percent_zakat_policy": True,
            "annual_zakat_audit_url": "https://hopemosque.example.org/zakat-audit-2026.pdf",
        },
        "contact": {
            "email": "hello@hopemosque.example.org",
            "phone": "+441234567890",
            "address": {
                "line1": "45 Mosque Road",
                "line2": None,
                "city": "Birmingham",
                "region": "West Midlands",
                "postcode": "B14 7QA",
                "country": "GB",
            },
        },
        "spec_version": "0.1.0",
    },
    "campaigns": [
        {
            "id": "cmp_ramadan2026",
            "slug": "ramadan-2026",
            "name": "Ramadan 2026 \u2014 Iftar for 1,000 Families",
            "description": "Provide iftar meals to 1,000 families in need during Ramadan.",
            "image_url": "https://hopemosque.example.org/campaigns/ramadan-2026.jpg",
            "start_at": "2026-02-17T00:00:00Z",
            "end_at": "2026-03-19T23:59:59Z",
            "target_amount": {"value": 5000000, "currency": "GBP"},
            "current_amount": {"value": 1837500, "currency": "GBP"},
            "donor_count": 412,
            "allowed_donation_types": ["general", "zakat", "sadaqah"],
            "beneficiary_countries": ["GB", "YE", "SY", "BD"],
        },
    ],
    "funds": [
        {
            "id": "fund_food_bank",
            "name": "Community Food Bank",
            "description": "Long-running fund supporting our weekly food bank service.",
            "restricted": True,
            "allowed_donation_types": ["general", "sadaqah", "zakat"],
        },
    ],
    # These start empty and fill as requests come in.
    "donations": [],
    "subscriptions": [],
    "receipts": [],
    "webhooks": [],
}
