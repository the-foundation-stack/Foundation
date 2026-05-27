# Tax Relief: Gift Aid and International Equivalents

Most countries with a meaningful charitable sector have some form of tax incentive that increases the effective value of a donation. The schemes differ in mechanics (donor deduction vs charity reclaim), thresholds, paperwork, and which charities qualify. The OCAS data model is designed so a single donation can carry zero, one, or many `tax_relief_declarations` — one per scheme that applies to that donor and that gift.

This document explains how each major scheme maps to the spec.

## The shape

```jsonc
{
  "tax_relief_declarations": [
    {
      "scheme": "uk_gift_aid",
      "declared_at": "2026-05-27T10:23:00Z",
      "declaration_text_version": "hmrc-model-2024-v1",
      "covers": "this_gift_and_all_future",
      "uk_gift_aid": {
        "donor_full_name": "Aisha Khan",
        "donor_home_address": {
          "line1": "12 Example Road",
          "line2": null,
          "city": "London",
          "postcode": "E1 6AN",
          "country": "GB"
        },
        "donor_confirms_taxpayer": true,
        "donor_confirms_pays_enough_tax": true
      }
    }
  ]
}
```

`scheme` is a discriminator. The corresponding scheme-specific object (`uk_gift_aid`, `us_501c3`, `au_dgr`, etc.) carries the fields that scheme actually needs. Charities only implement the schemes they support; apps only render UI for the schemes the charity declares in `GET /charity → supported_tax_relief_schemes`.

## UK — Gift Aid (`uk_gift_aid`)

**What it is.** When a UK income-tax or capital-gains-tax payer makes a "qualifying donation" to an HMRC-recognised charity and provides a valid declaration, the charity can reclaim 25p for every £1 donated (i.e. 25% of the basic-rate tax the donor has already paid). Higher-rate taxpayers can claim back the difference between basic and higher rate on their self-assessment.

**Declaration requirements (HMRC, as of 2026).** A valid declaration must contain:

1. The **donor's full forename(s)** — not initials.
2. The **donor's home address** — work / care-of / PO Box addresses are not acceptable. Postcode at minimum.
3. The **name of the charity**.
4. The **identity of the gift(s)** — this one gift, or all future gifts, or "all gifts I have made in the past 4 years and all future gifts".
5. The donor's **confirmation** that they want Gift Aid claimed.
6. The donor must be **made aware** that if they have not paid enough income or CGT to cover the amount the charity will reclaim, they will need to make up the difference themselves. (This notice doesn't need to be inside the declaration, but charities almost always include it.)

**Spec fields:** the `uk_gift_aid` object above carries all six. The `declaration_text_version` is the charity's identifier for the exact wording shown to the donor at the time — useful for audit if HMRC questions a claim.

**GASDS (Gift Aid Small Donations Scheme).** Cash and contactless donations up to £30 each can be reclaimed under GASDS without a declaration, up to £8,000 per tax year (capped at 10× the charity's Gift Aid claims). This is a charity-side reclaim, not a donor-side declaration; it has no field in the donation object. Charities track it internally from their bookkeeping.

**Tainted Donations (April 2026 changes).** From April 2026, HMRC applies a stricter test where a donor receives a financial benefit from the charity in return. Charities are responsible for their own compliance; OCAS exposes the `benefits_received` optional field on a donation so charities can record what (if anything) the donor got back, but the rules themselves are not codified into the spec.

**Reclaim mechanics.** Charities file claims with HMRC via Charities Online or a software submission to the HMRC API quarterly (or more frequently). OCAS does not yet expose an endpoint that bundles a claim file, but a future version may; the underlying donation data already contains everything HMRC requires.

## US — 501(c)(3) (`us_501c3`)

**What it is.** Donations to organisations recognised under IRS section 501(c)(3) are deductible by the donor against US federal income tax (and most state taxes), subject to AGI percentage limits.

**Declaration requirements.** Unlike Gift Aid, the donor doesn't "declare" up-front — they keep the receipt. But the charity MUST provide a "contemporaneous written acknowledgment" for any single gift of $250 or more, containing:

1. The amount of cash and a description (not value) of any non-cash contribution.
2. A statement of whether the charity provided any goods or services in consideration, in whole or in part, for the gift.
3. If goods or services were provided, a description and good-faith estimate of their value.

**Spec fields:**

```jsonc
{
  "scheme": "us_501c3",
  "us_501c3": {
    "ein": "12-3456789",
    "goods_or_services_provided": false,
    "goods_or_services_description": null,
    "goods_or_services_value": null,
    "donor_intends_to_deduct": true
  }
}
```

The `ein` is the charity's IRS Employer Identification Number. Apps should display "Tax ID: 12-3456789" on the receipt.

## Canada — CRA Donation Receipt (`ca_cra`)

**What it is.** Registered Canadian charities issue "official donation receipts" that donors use for a federal credit (15% on first $200, 29% above) plus provincial credits.

**Required receipt fields** (Income Tax Regulations s.3501): charity name and registration number, CRA's website, receipt serial number, place of issue, donor full name and address, date of donation, amount, eligible-amount (if any advantage was received), advantage amount, name of authorised signatory.

```jsonc
{
  "scheme": "ca_cra",
  "ca_cra": {
    "registration_number": "12345 6789 RR0001",
    "advantage_amount": { "value": 0, "currency": "CAD" },
    "eligible_amount": { "value": 5000, "currency": "CAD" },
    "receipt_serial_number": "2026-001234",
    "place_of_issue": "Toronto, ON"
  }
}
```

## Australia — DGR (`au_dgr`)

**What it is.** Donations of $2 or more to charities with Deductible Gift Recipient endorsement are deductible against Australian income tax at the donor's marginal rate.

```jsonc
{
  "scheme": "au_dgr",
  "au_dgr": {
    "abn": "12 345 678 901",
    "dgr_endorsement_category": "Public Benevolent Institution",
    "donation_is_gift_under_div30": true
  }
}
```

A receipt is required for amounts above $2; charities typically issue one for every donation.

## Ireland — CHY Charitable Donations Scheme (`ie_chy`)

**What it is.** For donations ≥ €250 in a tax year from a PAYE or self-assessed donor, the charity can reclaim tax at a blended rate of 31%. The donor signs CHY3 (5-year enduring) or CHY4 (single year) certificate.

```jsonc
{
  "scheme": "ie_chy",
  "ie_chy": {
    "donor_ppsn": "1234567A",      // optional but strongly recommended for charity
    "certificate_type": "CHY3",
    "valid_until": "2030-12-31"
  }
}
```

## Germany — Spendenbescheinigung (`de_spendenbescheinigung`)

**What it is.** Recognised gemeinnützige (charitable) organisations issue a Zuwendungsbestätigung (donation confirmation) which the donor uses to reduce taxable income by up to 20% of total income.

For donations under €300, a simplified receipt (bank statement + the charity's prescribed short form) is sufficient; above €300 a full Zuwendungsbestätigung in the form prescribed by the Bundesministerium der Finanzen is required.

```jsonc
{
  "scheme": "de_spendenbescheinigung",
  "de_spendenbescheinigung": {
    "vereinsregister_number": "VR 12345",
    "freistellungsbescheid_date": "2025-03-15",
    "issuing_finanzamt": "Finanzamt München",
    "form_variant": "long"          // "short" | "long"
  }
}
```

## France — Réduction d'impôt (`fr_reduction`)

**What it is.** Donations to organisations of "intérêt général" qualify for a 66% income-tax reduction (75% for some categories like food/lodging for the destitute), capped at 20% of taxable income. The donor receives a *reçu fiscal* (Cerfa form 11580).

```jsonc
{
  "scheme": "fr_reduction",
  "fr_reduction": {
    "organisation_status": "interet_general",  // or "utilite_publique", "culte"
    "siret": "12345678901234",
    "reduction_rate": 66,
    "cerfa_form_number": "11580*05"
  }
}
```

## Netherlands — ANBI (`nl_anbi`)

**What it is.** Donations to "Algemeen Nut Beogende Instellingen" are deductible. Periodic gifts (5+ year commitments) via notarial deed historically gave 100%+ deduction; one-off gifts have a threshold-and-cap structure.

```jsonc
{
  "scheme": "nl_anbi",
  "nl_anbi": {
    "rsin": "123456789",
    "anbi_status_verified_at": "2026-01-01",
    "is_periodic_gift": false,
    "notarial_deed_reference": null
  }
}
```

## Singapore — IPC (`sg_ipc`)

**What it is.** Donations to Institutions of a Public Character are deductible at 250% — among the most generous schemes globally.

```jsonc
{
  "scheme": "sg_ipc",
  "sg_ipc": {
    "ipc_number": "IPC000123",
    "donor_nric_or_fin": "S1234567A",   // required for IRAS auto-inclusion
    "deduction_multiplier": 2.5
  }
}
```

## Malaysia — Section 44(6) (`my_section44_6`)

```jsonc
{
  "scheme": "my_section44_6",
  "my_section44_6": {
    "irb_approval_number": "LHDN.01/35/42/51/179-...",
    "donor_tax_file_number": "OG12345678"
  }
}
```

## A note on cross-border giving

In most jurisdictions, **a donor cannot deduct a donation made directly to a foreign charity**. The standard workaround is to give via a domestic intermediary that holds local charitable status and grants onwards (CAF in the UK, NPT in the US, Foundation Source in Europe). The donation API itself doesn't need to model this — from the donor's perspective they're donating to the intermediary, and the intermediary's OCAS endpoint would issue the local declaration.

A future RFC may add an `intended_beneficiary_charity` field for transparency.

## What apps should do

1. Read `supported_tax_relief_schemes` from `GET /charity`.
2. Intersect with the donor's tax residency (which the donor can set in their profile, or the app can infer from billing address).
3. Render the appropriate UI: a Gift Aid checkbox with the legally required text for UK donors, a "this is tax-deductible" notice for US donors, etc.
4. Send the declaration on `POST /donations` in the `tax_relief_declarations` array.
5. Use the receipt URL returned in the response to give the donor proof.

That's it. Apps don't need to know the legal mechanics of each scheme — only that they need to collect certain fields when the donor is in jurisdiction X and the charity supports scheme Y.

## What charities must do

For each scheme they support, charities need to:

1. Be properly registered with the relevant authority (HMRC, IRS, CRA, ATO, Finanzamt, etc.).
2. Use a `declaration_text_version` they can show to auditors — the exact wording shown to the donor when they ticked the box.
3. Retain declarations for the period required by the relevant authority (usually 6 years from end of accounting period for UK Gift Aid; 7 years for US 501(c)(3); varies elsewhere).
4. File the claims with the authority on the relevant schedule. OCAS does not file claims for you; it gives you clean structured data to file them with.

## Disclaimer

This document is a developer-oriented summary for the purpose of explaining API fields. It is **not** tax or legal advice. Rules change. Confirm details with HMRC, the IRS, CRA, ATO, BMF, or your local equivalent before implementing in production. Anywhere you see a number or a threshold, double-check it against the official guidance for the current tax year.
