"""Conformance-style tests for the OCAS reference server (Python).

Run with:
    pip install -r requirements.txt
    pytest

These mirror the Node implementation's tests: happy path, validation rules,
idempotency, and refunds.
"""

from fastapi.testclient import TestClient

from ocas.server import app, BASE

client = TestClient(app)


def test_get_charity():
    res = client.get(f"{BASE}/charity")
    assert res.status_code == 200
    body = res.json()
    assert body["name"] == "Hope Mosque Foundation"
    assert "zakat" in body["supported_donation_types"]


def test_create_donation_and_receipt():
    res = client.post(
        f"{BASE}/donations",
        json={
            "amount": {"value": 2500, "currency": "GBP"},
            "donation_type": "sadaqah",
            "donor": {"first_name": "Aisha", "last_name": "Khan", "email": "aisha@example.com"},
        },
    )
    assert res.status_code == 201
    body = res.json()
    assert body["id"].startswith("don_")
    assert body["status"] == "completed"
    assert body["receipt_id"]

    receipt_res = client.get(f'{BASE}/receipts/{body["receipt_id"]}')
    assert receipt_res.status_code == 200
    assert receipt_res.json()["donation_id"] == body["id"]


def test_rejects_zero_amount():
    res = client.post(
        f"{BASE}/donations",
        json={"amount": {"value": 0, "currency": "GBP"}, "donation_type": "sadaqah"},
    )
    assert res.status_code == 400
    assert res.json()["error"]["code"] == "invalid_amount"


def test_rejects_asnaf_not_summing_to_100():
    res = client.post(
        f"{BASE}/donations",
        json={
            "amount": {"value": 2500, "currency": "GBP"},
            "donation_type": "zakat",
            "zakat_metadata": {
                "asnaf_allocation": [
                    {"asnaf": "fuqara", "percentage": 50},
                    {"asnaf": "masakin", "percentage": 40},
                ]
            },
        },
    )
    assert res.status_code == 422
    assert res.json()["error"]["code"] == "invalid_zakat"


def test_rejects_interest_purification_as_zakat():
    res = client.post(
        f"{BASE}/donations",
        json={
            "amount": {"value": 2500, "currency": "GBP"},
            "donation_type": "interest_purification",
            "zakat_metadata": {"asnaf_allocation": [{"asnaf": "fuqara", "percentage": 100}]},
        },
    )
    assert res.status_code == 422
    assert res.json()["error"]["code"] == "invalid_zakat"


def test_idempotency_prevents_duplicates():
    payload = {"amount": {"value": 1000, "currency": "GBP"}, "donation_type": "sadaqah"}
    headers = {"Idempotency-Key": "test-key-py-123"}

    first = client.post(f"{BASE}/donations", json=payload, headers=headers)
    assert first.status_code == 201
    first_id = first.json()["id"]

    second = client.post(f"{BASE}/donations", json=payload, headers=headers)
    assert second.status_code == 200
    assert second.json()["id"] == first_id


def test_refund():
    create = client.post(
        f"{BASE}/donations",
        json={"amount": {"value": 500, "currency": "GBP"}, "donation_type": "sadaqah"},
    )
    donation_id = create.json()["id"]
    refund = client.post(f"{BASE}/donations/{donation_id}/refund")
    assert refund.status_code == 200
    assert refund.json()["status"] == "refunded"
