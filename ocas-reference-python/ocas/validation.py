"""Minimal request validation for the OCAS reference server.

This is intentionally light. A production implementation would validate against
the OpenAPI schema directly. Here we hand-roll a few checks so the logic stays
visible and the rules OCAS cares about are easy to read.

Each validator returns None on success, or a Problem (status + body) on failure.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class Problem:
    status: int
    body: dict


def problem(status: int, code: str, message: str, field: Optional[str] = None) -> Problem:
    """Build a Problem mirroring the OCAS Error schema."""
    err: dict = {"code": code, "message": message}
    if field:
        err["field"] = field
    return Problem(status=status, body={"error": err})


def validate_money(money: Any, field_path: str) -> Optional[Problem]:
    """Money must be {value: int >= 1 (minor units), currency: 3-letter code}."""
    if not isinstance(money, dict):
        return problem(400, "invalid_amount", "Amount is required.", field_path)
    value = money.get("value")
    # bool is a subclass of int in Python; exclude it explicitly.
    if not isinstance(value, int) or isinstance(value, bool):
        return problem(
            400,
            "invalid_amount",
            "Amount value must be an integer in minor units (e.g. 2500 for \u00a325.00).",
            f"{field_path}.value",
        )
    if value <= 0:
        return problem(400, "invalid_amount", "Amount must be greater than zero.", f"{field_path}.value")
    currency = money.get("currency")
    if not isinstance(currency, str) or len(currency) != 3 or not currency.isalpha() or not currency.isupper():
        return problem(
            400,
            "invalid_currency",
            "Currency must be a 3-letter ISO 4217 code, e.g. GBP.",
            f"{field_path}.currency",
        )
    return None


DONATION_TYPES = {
    "general",
    "zakat",
    "sadaqah",
    "sadaqah_jariyah",
    "waqf",
    "lillah",
    "fidya",
    "kaffarah",
    "qurbani",
    "udhiyyah",
    "aqiqah",
    "interest_purification",
}

# The 8 canonical Asnaf (Qur'an 9:60).
ASNAF = {
    "fuqara",
    "masakin",
    "amilin_alayha",
    "muallafat_al_qulub",
    "fir_riqab",
    "gharimin",
    "fi_sabilillah",
    "ibn_al_sabil",
}


def validate_donation_type(donation_type: Any) -> Optional[Problem]:
    if not isinstance(donation_type, str) or donation_type not in DONATION_TYPES:
        allowed = ", ".join(sorted(DONATION_TYPES))
        return problem(
            400,
            "invalid_donation_type",
            f"donation_type must be one of: {allowed}.",
            "donation_type",
        )
    return None


def validate_zakat_metadata(donation_type: Any, zakat_metadata: Any) -> Optional[Problem]:
    """interest_purification can never be Zakat. If asnaf_allocation is present,
    every category must be a valid Asnaf and the percentages must sum to 100.
    """
    if donation_type == "interest_purification" and zakat_metadata:
        return problem(
            422,
            "invalid_zakat",
            "interest_purification cannot carry zakat_metadata; purification of interest is not Zakat.",
            "zakat_metadata",
        )

    if not zakat_metadata or "asnaf_allocation" not in zakat_metadata:
        return None

    allocation = zakat_metadata.get("asnaf_allocation")
    if not isinstance(allocation, list) or len(allocation) == 0:
        return problem(
            400,
            "invalid_zakat",
            "asnaf_allocation must be a non-empty array.",
            "zakat_metadata.asnaf_allocation",
        )

    total = 0.0
    for entry in allocation:
        if not isinstance(entry, dict) or entry.get("asnaf") not in ASNAF:
            allowed = ", ".join(sorted(ASNAF))
            got = entry.get("asnaf") if isinstance(entry, dict) else entry
            return problem(
                400,
                "invalid_asnaf",
                f'Unknown Asnaf category "{got}". Must be one of: {allowed}.',
                "zakat_metadata.asnaf_allocation",
            )
        pct = entry.get("percentage")
        if not isinstance(pct, (int, float)) or isinstance(pct, bool) or pct <= 0:
            return problem(
                400,
                "invalid_asnaf",
                "Each Asnaf allocation needs a positive percentage.",
                "zakat_metadata.asnaf_allocation",
            )
        total += pct

    if round(total) != 100:
        return problem(
            422,
            "invalid_zakat",
            f"Asnaf allocation percentages must sum to 100 (got {int(total) if total == int(total) else total}).",
            "zakat_metadata.asnaf_allocation",
        )

    return None
