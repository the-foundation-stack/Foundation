"""OCAS reference server (Python / FastAPI).

A barebones, in-memory implementation of the Open Charity API Standard.

Run with:
    pip install -r requirements.txt
    uvicorn ocas.server:app --reload

Base path matches the spec: /api/ocas/v1

This server runs in "public" auth mode, so no credentials are needed. It is for
learning and conformance testing, NOT production: there's no persistence, no
real payment processing, no authentication, and no rate limiting.

A nice side effect of FastAPI: it generates its own interactive docs at
http://localhost:8000/docs once running.
"""

from __future__ import annotations

import json
from typing import Optional

from fastapi import FastAPI, Header, Request, Response
from fastapi.responses import JSONResponse

from .store import db, next_id, now_iso
from .validation import (
    Problem,
    problem,
    validate_donation_type,
    validate_money,
    validate_zakat_metadata,
)

app = FastAPI(
    title="OCAS Reference Server",
    description="A reference implementation of the Open Charity API Standard.",
    version="0.1.0",
)

BASE = "/api/ocas/v1"


def send_problem(p: Problem) -> JSONResponse:
    return JSONResponse(status_code=p.status, content=p.body)


def emit_webhook(event_type: str, data: dict) -> None:
    """Fire any registered webhooks for an event. In this reference server we
    just log them rather than making real HTTP calls, so you can see what would
    be sent without needing a receiver.
    """
    for w in db["webhooks"]:
        if w["active"] and event_type in w["events"]:
            event = {
                "id": next_id("evt"),
                "type": event_type,
                "created_at": now_iso(),
                "api_version": "1.0",
                "data": data,
            }
            # A real implementation would POST this to w["url"] with an
            # OCAS-Signature header (HMAC-SHA256 over the body).
            print(f'[webhook] would POST {event_type} to {w["url"]}: {json.dumps(event)}')


def strip_internal(obj: dict) -> dict:
    clone = dict(obj)
    clone.pop("_idempotency_key", None)
    return clone


# ---------------------------------------------------------------------------
# Charity
# ---------------------------------------------------------------------------


@app.get(f"{BASE}/charity")
def get_charity():
    return db["charity"]


# ---------------------------------------------------------------------------
# Campaigns
# ---------------------------------------------------------------------------


@app.get(f"{BASE}/campaigns")
def list_campaigns():
    return {"data": db["campaigns"]}


@app.get(f"{BASE}/campaigns/{{campaign_id}}")
def get_campaign(campaign_id: str):
    campaign = next((c for c in db["campaigns"] if c["id"] == campaign_id), None)
    if not campaign:
        return send_problem(problem(404, "not_found", "Campaign not found."))
    return campaign


# ---------------------------------------------------------------------------
# Funds
# ---------------------------------------------------------------------------


@app.get(f"{BASE}/funds")
def list_funds():
    return {"data": db["funds"]}


@app.get(f"{BASE}/funds/{{fund_id}}")
def get_fund(fund_id: str):
    fund = next((f for f in db["funds"] if f["id"] == fund_id), None)
    if not fund:
        return send_problem(problem(404, "not_found", "Fund not found."))
    return fund


# ---------------------------------------------------------------------------
# Donations
# ---------------------------------------------------------------------------


@app.post(f"{BASE}/donations")
async def create_donation(request: Request, idempotency_key: Optional[str] = Header(default=None)):
    body = await request.json()

    money_err = validate_money(body.get("amount"), "amount")
    if money_err:
        return send_problem(money_err)

    type_err = validate_donation_type(body.get("donation_type"))
    if type_err:
        return send_problem(type_err)

    zakat_err = validate_zakat_metadata(body.get("donation_type"), body.get("zakat_metadata"))
    if zakat_err:
        return send_problem(zakat_err)

    if body.get("campaign_id") and not any(c["id"] == body["campaign_id"] for c in db["campaigns"]):
        return send_problem(problem(422, "invalid_reference", "Referenced campaign does not exist.", "campaign_id"))
    if body.get("fund_id") and not any(f["id"] == body["fund_id"] for f in db["funds"]):
        return send_problem(problem(422, "invalid_reference", "Referenced fund does not exist.", "fund_id"))

    # Idempotency: if we've seen this key, return the original donation.
    if idempotency_key:
        existing = next((d for d in db["donations"] if d.get("_idempotency_key") == idempotency_key), None)
        if existing:
            return JSONResponse(status_code=200, content=strip_internal(existing))

    now = now_iso()
    donor = None
    if body.get("donor"):
        donor = {"id": next_id("donor"), **body["donor"]}

    donation = {
        "id": next_id("don"),
        "amount": body["amount"],
        "donation_type": body["donation_type"],
        "donor": donor,
        "anonymous": body.get("anonymous", False),
        "campaign_id": body.get("campaign_id"),
        "fund_id": body.get("fund_id"),
        "beneficiary_country": body.get("beneficiary_country"),
        "message": body.get("message"),
        "tax_relief_declarations": body.get("tax_relief_declarations", []),
        "zakat_metadata": body.get("zakat_metadata"),
        "qurbani_metadata": body.get("qurbani_metadata"),
        "aqiqah_metadata": body.get("aqiqah_metadata"),
        "cover_fees": body.get("cover_fees", False),
        "status": "completed",  # No real payment step; completed instantly.
        "payment": {
            "processor": "reference-sandbox",
            "processor_ref": next_id("pay"),
            "method_used": body.get("payment_method_preference", "card"),
            "completed_at": now,
        },
        "receipt_id": None,
        "created_at": now,
        "_idempotency_key": idempotency_key,
    }

    donor_name = "Anonymous"
    if donor:
        donor_name = f'{donor.get("first_name", "")} {donor.get("last_name", "")}'.strip()

    receipt = {
        "id": next_id("rcpt"),
        "donation_id": donation["id"],
        "issued_at": now,
        "amount": donation["amount"],
        "donor_name": donor_name,
        "charity_name": db["charity"]["name"],
        "charity_registration_numbers": db["charity"]["registration_numbers"],
        "tax_relief_schemes_applied": [d["scheme"] for d in donation["tax_relief_declarations"]],
        "pdf_url": None,
        "locale": "en-GB",
    }
    donation["receipt_id"] = receipt["id"]

    db["donations"].append(donation)
    db["receipts"].append(receipt)

    emit_webhook("donation.completed", {"donation": strip_internal(donation)})

    return JSONResponse(status_code=201, content=strip_internal(donation))


@app.get(f"{BASE}/donations")
def list_donations():
    return {"data": [strip_internal(d) for d in db["donations"]]}


@app.get(f"{BASE}/donations/{{donation_id}}")
def get_donation(donation_id: str):
    donation = next((d for d in db["donations"] if d["id"] == donation_id), None)
    if not donation:
        return send_problem(problem(404, "not_found", "Donation not found."))
    return strip_internal(donation)


@app.post(f"{BASE}/donations/{{donation_id}}/refund")
def refund_donation(donation_id: str):
    donation = next((d for d in db["donations"] if d["id"] == donation_id), None)
    if not donation:
        return send_problem(problem(404, "not_found", "Donation not found."))
    if donation["status"] == "refunded":
        return send_problem(problem(409, "already_refunded", "Donation has already been refunded."))
    donation["status"] = "refunded"
    emit_webhook("donation.refunded", {"donation": strip_internal(donation)})
    return strip_internal(donation)


# ---------------------------------------------------------------------------
# Subscriptions
# ---------------------------------------------------------------------------


@app.post(f"{BASE}/subscriptions")
async def create_subscription(request: Request):
    body = await request.json()

    money_err = validate_money(body.get("amount"), "amount")
    if money_err:
        return send_problem(money_err)

    type_err = validate_donation_type(body.get("donation_type"))
    if type_err:
        return send_problem(type_err)

    valid_freq = ["daily", "weekly", "monthly", "quarterly", "annually"]
    if body.get("frequency") not in valid_freq:
        return send_problem(
            problem(400, "invalid_frequency", f'frequency must be one of: {", ".join(valid_freq)}.', "frequency")
        )

    now = now_iso()
    donor = None
    if body.get("donor"):
        donor = {"id": next_id("donor"), **body["donor"]}

    sub = {
        "id": next_id("sub"),
        "amount": body["amount"],
        "frequency": body["frequency"],
        "donation_type": body["donation_type"],
        "donor": donor,
        "fund_id": body.get("fund_id"),
        "start_at": body.get("start_at", now),
        "max_payments": body.get("max_payments"),
        "status": "active",
        "created_at": now,
        "next_payment_at": body.get("start_at", now),
        "payments_completed": 0,
        "total_donated": {"value": 0, "currency": body["amount"]["currency"]},
        "anonymous": body.get("anonymous", False),
    }
    db["subscriptions"].append(sub)
    return JSONResponse(status_code=201, content=sub)


@app.get(f"{BASE}/subscriptions")
def list_subscriptions():
    return {"data": db["subscriptions"]}


@app.get(f"{BASE}/subscriptions/{{subscription_id}}")
def get_subscription(subscription_id: str):
    sub = next((s for s in db["subscriptions"] if s["id"] == subscription_id), None)
    if not sub:
        return send_problem(problem(404, "not_found", "Subscription not found."))
    return sub


@app.patch(f"{BASE}/subscriptions/{{subscription_id}}")
async def update_subscription(subscription_id: str, request: Request):
    sub = next((s for s in db["subscriptions"] if s["id"] == subscription_id), None)
    if not sub:
        return send_problem(problem(404, "not_found", "Subscription not found."))
    body = await request.json()
    if body.get("amount"):
        money_err = validate_money(body["amount"], "amount")
        if money_err:
            return send_problem(money_err)
        sub["amount"] = body["amount"]
    if body.get("status") in ("active", "paused"):
        sub["status"] = body["status"]
    return sub


@app.delete(f"{BASE}/subscriptions/{{subscription_id}}")
def cancel_subscription(subscription_id: str):
    sub = next((s for s in db["subscriptions"] if s["id"] == subscription_id), None)
    if not sub:
        return send_problem(problem(404, "not_found", "Subscription not found."))
    sub["status"] = "cancelled"
    return sub


# ---------------------------------------------------------------------------
# Receipts
# ---------------------------------------------------------------------------


@app.get(f"{BASE}/receipts/{{receipt_id}}")
def get_receipt(receipt_id: str):
    receipt = next((r for r in db["receipts"] if r["id"] == receipt_id), None)
    if not receipt:
        return send_problem(problem(404, "not_found", "Receipt not found."))
    return receipt


# ---------------------------------------------------------------------------
# Zakat calculator
# ---------------------------------------------------------------------------


@app.get(f"{BASE}/zakat/calculator")
def zakat_calculator():
    # Static illustrative Nisab values. A real implementation would fetch live
    # gold/silver prices.
    return {
        "nisab": {
            "gold_based": {"value": 542500, "currency": "GBP"},
            "silver_based": {"value": 41200, "currency": "GBP"},
            "as_of": now_iso(),
        },
        "rate": 0.025,
        "notes": "Illustrative values from the reference server. Consult a scholar where uncertain.",
    }


# ---------------------------------------------------------------------------
# Webhooks
# ---------------------------------------------------------------------------


@app.post(f"{BASE}/webhooks")
async def create_webhook(request: Request):
    body = await request.json()
    url = body.get("url")
    if not isinstance(url, str) or not (url.startswith("http://") or url.startswith("https://")):
        return send_problem(problem(400, "invalid_url", "Webhook url must be an http(s) URL.", "url"))
    events = body.get("events")
    if not isinstance(events, list) or len(events) == 0:
        return send_problem(problem(400, "invalid_events", "At least one event must be subscribed.", "events"))
    webhook = {
        "id": next_id("wh"),
        "url": url,
        "events": events,
        "description": body.get("description"),
        "active": True,
        "created_at": now_iso(),
    }
    db["webhooks"].append(webhook)
    return JSONResponse(status_code=201, content=webhook)


@app.get(f"{BASE}/webhooks")
def list_webhooks():
    return {"data": db["webhooks"]}


@app.delete(f"{BASE}/webhooks/{{webhook_id}}")
def delete_webhook(webhook_id: str):
    idx = next((i for i, w in enumerate(db["webhooks"]) if w["id"] == webhook_id), -1)
    if idx == -1:
        return send_problem(problem(404, "not_found", "Webhook not found."))
    db["webhooks"].pop(idx)
    return Response(status_code=204)


# ---------------------------------------------------------------------------
# Root
# ---------------------------------------------------------------------------


@app.get("/")
def root():
    return {
        "message": "OCAS reference server. See the spec at https://the-foundation-stack.github.io/Foundation/open-charity-api/",
        "base_path": BASE,
        "try": f"{BASE}/charity",
        "interactive_docs": "/docs",
    }
