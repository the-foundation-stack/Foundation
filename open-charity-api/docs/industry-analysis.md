# Charity Industry Analysis

> This document is the reasoning behind the OCAS specification. Every endpoint and every field exists because of something in here. If you're proposing a change, please read this first — and if you think it's wrong, please open an issue, because that means our reasoning is wrong too.

## 1. The landscape, briefly

Globally, the charitable sector receives somewhere in the region of $500bn–$1tn a year in private donations, depending on whose methodology you trust. The UK alone sees roughly £13–15bn in individual giving annually. Despite the scale, the **technical infrastructure of the sector is fragmented to a degree that would not be tolerated in any other industry of comparable size**.

A typical charity's donation stack looks something like this:

```
Donor
  │
  ├── Direct website     ──→ WordPress + a plugin (GiveWP, Donorbox embed)
  ├── Facebook fundraiser ──→ Meta's own pipeline (charity may never see donor data)
  ├── JustGiving page    ──→ JustGiving's API and fee structure
  ├── Enthuse / GoFundMe ──→ Another platform, another fee, another export
  ├── Bank standing order ──→ A CSV, manually reconciled
  ├── Direct Debit (GoCardless) ──→ Reconciled into a CRM if they have one
  └── Cash in a bucket    ──→ Counted manually, no donor record at all
                ↓
        Charity CRM (Salesforce NPSP, Beacon, Donorfy, Raiser's Edge, Excel)
                ↓
        HMRC Gift Aid claim (uploaded as a spreadsheet to HMRC's Charities Online)
```

The donor's identity, intent, and tax status are scattered across half a dozen systems that don't talk to each other. Reconciliation eats charity staff time. Tax relief is left unclaimed because the data didn't survive the journey. Donors get duplicate thank-you emails or none at all.

This is the problem space.

## 2. What every charity needs from a donation API

After looking at the public-facing donation pages, integration docs, and FAQ pages of a wide sample of UK, US, Australian, EU and Muslim-world charities, a strikingly consistent set of needs emerges. We list them below as a flat checklist; the OpenAPI spec maps each one to an endpoint or field.

### 2.1 Money movement (the obvious bit)

- Accept a one-off donation in a specified currency and amount.
- Accept a recurring donation (weekly / monthly / quarterly / annually / **daily** — daily is increasingly requested for Ramadan use cases).
- Allow the donor to pay in their currency while the charity is denominated in another.
- Support the dominant payment methods of the donor's region:
  - **UK / EU:** card, Direct Debit (BACS / SEPA), Open Banking pay-by-bank, Apple/Google Pay.
  - **US:** card, ACH, Apple/Google Pay, PayPal, Venmo.
  - **MENA / South Asia / SE Asia:** card, local wallets (Sadad, Fawry, GCash, JazzCash, ShopeePay), bank transfer with a reference.
  - **Cross-border:** card with currency conversion, PayPal, crypto where the charity opts in.
- Issue a refund (within a window the charity controls).
- Handle failed payments and retry logic for recurring donations.

### 2.2 Donor identity and consent

- Capture donor identity at varying levels of fidelity:
  - Anonymous (no personal data, no receipt).
  - Email only (minimal — enough to send a receipt).
  - Email + name + address (required for Gift Aid in the UK).
  - Full account (donor can log in, see history, manage subscriptions).
- Capture GDPR-style consent for marketing, contact channel preferences, and data retention. *In the UK and EU, charities have been fined for getting this wrong.*
- Capture a donor's preferred language for receipts and follow-ups.
- Capture whether the donor wants to be anonymous publicly (e.g. on a fundraiser leaderboard) while still being known to the charity.
- Handle "in memory of" and "in honour of" dedications, optionally with a notification email to a third party.

### 2.3 Tax relief and receipts

This is the field that is most often badly modelled. Tax-relief schemes vary hugely:

| Country | Scheme | Donor must... | Charity must... | Top-up rate |
|---|---|---|---|---|
| UK | Gift Aid | Be a UK taxpayer, give name + home address, sign declaration | Be HMRC-recognised, store declaration, claim quarterly | 25% (basic rate reclaim) |
| UK | GASDS (Small Donations) | Nothing (no declaration needed) | Cash/contactless ≤£30, ≤£8,000/yr, 10× Gift Aid rule | 25% |
| US | 501(c)(3) | Have receipt for >$250 single gift | Be IRS-recognised, issue contemporaneous written acknowledgment | Itemised deduction |
| Canada | CRA donation receipt | Receive official receipt | Be CRA-registered, issue receipt with prescribed fields | Federal + provincial credit |
| Australia | DGR | Donate >$2 to DGR-endorsed charity | Hold DGR endorsement, issue receipt | Marginal-rate deduction |
| Ireland | CHY scheme | Donate ≥€250/yr, sign CHY3 or CHY4 | Be authorised, file claim | ~31% (charity reclaims) |
| Germany | Spendenbescheinigung | Receive Zuwendungsbestätigung for >€300 | Be gemeinnützig, issue receipt in prescribed form | Deductible up to 20% of income |
| France | Don aux œuvres | Receive reçu fiscal | Be d'intérêt général, issue reçu | 66% reduction (up to 20% of income) |
| Netherlands | ANBI | Receive receipt; periodic giving via notarial deed for full benefit | Hold ANBI status, publish required info | Variable, up to 125% for periodic |
| Singapore | IPC | Donate to Institution of a Public Character | Hold IPC status | 250% deduction (one of the most generous) |
| Malaysia | s.44(6) | Receive receipt | Approved by IRB | Deductible up to 10% of income |

**What this means for the API:** there is no universal `gift_aid: true` field. The right abstraction is a `tax_relief_declarations` array where each entry carries a `scheme` discriminator (`uk_gift_aid`, `us_501c3`, `au_dgr`, ...) and scheme-specific fields. Charities only need to support the schemes they're registered for. Apps only need to render UI for the schemes that match the donor's jurisdiction.

A donation receipt is a separate object from the tax-relief declaration. A receipt can be needed even without tax relief (e.g. for accounting), and tax relief can apply without a receipt being requested (e.g. Gift Aid claims happen quarterly in bulk).

### 2.4 Designation and intent

Donors care, often deeply, where their money goes within the charity. Charities accommodate this through:

- **Campaigns / appeals** — time-bound (Ramadan 2026, Winter Appeal, Türkiye Earthquake Emergency).
- **Funds / projects** — long-running designated buckets (water wells, orphan sponsorship, masjid building fund).
- **Restricted vs unrestricted** — legally meaningful in the UK. Restricted funds can only be spent on the specified purpose.
- **Beneficiary geography** — "I want this to go to Gaza" / "I want this to stay in our local borough".
- **Donation type** — even within a Muslim charity, Zakat money can only fund Zakat-eligible projects, Sadaqah is more flexible, Lillah is for masjid upkeep, Qurbani is time-locked to Eid al-Adha, etc.

**API implication:** a donation can reference an optional `campaign_id`, an optional `fund_id`, an optional `beneficiary_country`, and a `donation_type`. The charity exposes `/campaigns` and `/funds` so apps can render pickers.

### 2.5 Recurring giving

- A subscription has a frequency, amount, start date, and (optionally) an end date or maximum count.
- It can be paused, resumed, amended (different amount, different frequency, different designation), cancelled.
- Failed payments need to be surfaced to the donor so they can update their card; "involuntary churn" is the single biggest cause of recurring donation loss.
- The donor needs to be able to see their subscription and cancel it without contacting the charity (legal requirement in many jurisdictions, including the UK under the FRSB regulator and the EU under the PSD2/SCA framework).
- Subscriptions tied to a finite goal (e.g. "£20/month sponsoring child X for 12 months") need a clear end and a way for the charity to notify the donor that the term has completed.

### 2.6 Anti-fraud and compliance

- AML (Anti-Money Laundering): large donations may need source-of-funds checking. The API should expose donation amounts and donor identity in a way that allows the charity to apply its own AML policy without forcing the API to bake one in.
- PCI DSS: the API itself should never see raw card data. Payment data is tokenised by the payment processor and only the token / payment intent ID flows through OCAS.
- Sanctions screening: charities operating in conflict zones often need to screen donors against OFAC / HMT / EU consolidated lists. The API exposes enough donor identity to make this possible; how it's done is the charity's choice.
- Audit trail: every donation, declaration, refund, and subscription change must be timestamped and immutable. Charities subject to the UK Charity Commission, US IRS Form 990, etc. need this for their annual reporting.

### 2.7 Reconciliation and accounting

- The charity needs a way to pull a list of donations within a date range, by status (completed / pending / failed / refunded), with their payment-processor IDs so they can reconcile to the bank.
- Webhooks for donation lifecycle events (`donation.completed`, `donation.refunded`, `subscription.payment_failed`) so the charity's CRM stays in sync.
- A bulk export for offline analysis (CSV / JSON Lines).

### 2.8 Communication

- Receipts (transactional, sent immediately).
- Thank-yous (may be transactional or part of a journey).
- Tax-year summaries (annual, e.g. for US donors at year-end).
- The API doesn't need to *send* these emails — but it does need to expose the data so the charity's marketing tool can.

## 3. What's currently available, and where it falls short

| Platform | Has API? | Open? | Vendor lock-in | Notes |
|---|---|---|---|---|
| JustGiving | Partial | No (deprecated public API) | High | Largest UK platform; modern API access is limited. |
| GoFundMe | No real API | No | Total | Aggressively closed ecosystem. |
| Donorbox | Yes (REST) | No | Medium | Per-charity setup, sane API, but proprietary. |
| Enthuse | Limited | No | Medium | UK-focused, white-label. |
| Stripe (Climate / Charity) | Yes | No (Stripe-owned) | Low–medium | Excellent for payments, not a charity model. |
| PayPal Giving Fund | Yes | No | High | Routes donations via PPGF; not the charity directly. |
| GlobalGiving | Yes | Documented | Medium | International, project-based. |
| GiveWP | WordPress plugin | Open source | Low | But it's a plugin, not a public API spec. |
| **OCAS** | Yes | **Yes, this spec** | **None** | What you're reading. |

The gap is obvious: there is no vendor-neutral, open, charity-side-implementable specification. JustGiving and GoFundMe are gatekeepers; the more open platforms (Donorbox, GiveWP) are not standards. OCAS aims to be the standard, not another platform.

## 4. Faith-based and culturally-specific requirements

Most general-purpose donation platforms either ignore Islamic giving categories entirely or bolt them on as a free-text dropdown. That is a missed opportunity:

- **Zakat** must, by Islamic law, go to one of [eight specific categories of recipient](https://quran.com/9/60) (the Asnaf). A donor giving Zakat has a legitimate religious interest in knowing which Asnaf their money is reaching. Charities like Islamic Relief and Muslim Hands already publish Zakat policies; the API should expose this as structured data.
- **Sadaqah Jariyah** (ongoing charity) implies the money funds something long-lasting (a well, a tree, a Quran printed) — donors often want a project linkage and updates.
- **Waqf** is an endowment where the capital is preserved and only returns are distributed. It is structurally different from a donation and probably warrants its own object in a future spec version.
- **Fidya** and **Kaffarah** are atonement payments with fixed per-day amounts (e.g. feeding one poor person per missed fast) — calculators and bulk pricing matter.
- **Qurbani / Udhiya** is time-locked to the four days of Eid al-Adha. The API must support time-windowed donation types that close automatically.
- **Aqiqah** is a sacrifice on the birth of a child — usually one-off, often with naming/dedication.
- **Lillah** is general donation for charitable infrastructure (masjid running costs etc.), explicitly distinct from Zakat.

Similar patterns exist outside Islam — Christian tithing, Jewish ma'aser kesafim, Hindu daana, Sikh dasvandh — and the same `donation_type` mechanism can carry those. OCAS exposes a base set and lets charities extend with `x-` prefixed custom types.

## 5. The data model, derived from the above

This section is the bridge to the OpenAPI spec.

```
Charity
  ├── registration_numbers (jurisdiction → identifier)
  ├── supported_currencies
  ├── supported_donation_types
  ├── supported_tax_relief_schemes
  ├── auth_mode (public | api_key | oauth2)
  └── webhook_capabilities

Campaign
  ├── id, name, description
  ├── start_at, end_at (nullable)
  ├── target_amount (nullable)
  ├── current_amount
  ├── images, slug
  └── allows_donation_types[]

Fund (long-running designated bucket)
  ├── id, name
  ├── restricted (bool)
  └── description

Donation
  ├── id
  ├── amount: { value (minor units), currency }
  ├── donation_type (zakat | sadaqah | ... | general | custom)
  ├── status (pending | completed | failed | refunded | cancelled)
  ├── donor (embedded or referenced)
  ├── campaign_id, fund_id (nullable)
  ├── beneficiary_country (nullable)
  ├── zakat_metadata (nullable)
  ├── tax_relief_declarations[]
  ├── dedication (in_memory_of | in_honour_of, name, notify_email?)
  ├── anonymous (bool)
  ├── message (nullable, donor's own words)
  ├── payment: { method, processor, processor_ref, intent }
  ├── created_at, completed_at, refunded_at
  └── metadata (free-form, x- extensions)

Subscription
  ├── id
  ├── amount, frequency, donation_type, etc. (as Donation)
  ├── status (active | paused | cancelled | completed)
  ├── next_payment_at
  ├── end_at (nullable)
  └── donation_ids[] (history)

Donor
  ├── id (if accounts exist)
  ├── email, names, address, country
  ├── consents (marketing channel preferences, retention)
  ├── language
  └── tax_residency (for default scheme selection)

TaxReliefDeclaration (polymorphic on scheme)
  ├── scheme (uk_gift_aid | us_501c3 | au_dgr | de_spendenbescheinigung | ...)
  ├── declared_at
  ├── declaration_text_version
  ├── covers ("this gift" | "all future gifts" | "all past 4 years and future gifts")
  └── scheme-specific fields

Receipt
  ├── id, donation_id
  ├── issued_at
  ├── url (PDF), html, plain_text
  └── locale
```

## 6. Versioning and stability

OCAS uses semantic versioning at the spec level: `v1`, `v2`, etc. in the URL path. Within a major version:

- Added optional fields → minor version (non-breaking).
- Removed or renamed fields → major version bump.
- Charities are encouraged to support the latest two major versions in parallel for at least 12 months after a major bump.

Custom extensions live under `x-` prefixed fields, as is the OpenAPI convention. Anything important enough to be used by more than one charity should be promoted into the standard via the RFC process.

## 7. What we deliberately don't model (yet)

- **Donor-advised funds (DAFs)** — complex, US-specific, future RFC.
- **Stock/equity gifts** — needs broker integration, future RFC.
- **Cryptocurrency donations** — supported as a payment method, but the tax treatment varies wildly by jurisdiction and is best left to the charity's processor.
- **Legacies / bequests** — handled out-of-band by solicitors; not really an API surface.
- **Volunteer time / in-kind gifts** — a different problem, possibly a separate spec.
- **Grants from one charity to another** — different shape entirely.

Each of these is a legitimate future addition. We'd rather ship a tight v1 and grow it than ship a sprawling v0.1 that gets nothing right.

---

*This document will continue to evolve. Open an issue if you see something missing or wrong.*
