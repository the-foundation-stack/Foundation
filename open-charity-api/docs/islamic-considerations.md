# Islamic Giving: Zakat, Sadaqah, Waqf and Beyond

OCAS treats Islamic giving categories as first-class citizens, not as a free-text dropdown afterthought. This document explains the categories the spec supports, the religious and legal reasoning behind the fields, and how a non-Muslim developer can safely build against them without needing deep fiqh knowledge.

> **A note on scope.** This document is for developers. It is not a fatwa, not a legal opinion, and not religious advice. Where the spec exposes a field, it exposes it because charities and donors care about it operationally; how a charity actually distributes funds in compliance with Shariah is a matter for that charity's scholars and trustees, not for an API spec.

## The categories OCAS supports as `donation_type`

| Value | Arabic | Meaning in one line | Time-locked? |
|---|---|---|---|
| `zakat` | زكاة | Obligatory annual alms (2.5% of qualifying wealth above Nisab). | No |
| `zakat_al_fitr` | زكاة الفطر | Per-head obligatory payment before Eid al-Fitr prayer. | Yes (end of Ramadan) |
| `sadaqah` | صدقة | General voluntary charity. | No |
| `sadaqah_jariyah` | صدقة جارية | Ongoing/long-lasting charity (e.g. a well, a tree, a Quran printed). | No |
| `lillah` | لله | "For the sake of Allah", general donation, often for masjid running costs. | No |
| `waqf` | وقف | Endowment: capital preserved, returns distributed. | No |
| `fidya` | فدية | Compensation for a missed obligatory fast that cannot be made up (e.g. illness, pregnancy). | No |
| `kaffarah` | كفارة | Atonement payment for a deliberately broken fast or oath. | No |
| `qurbani` / `udhiya` | قربان / أضحية | Sacrifice on Eid al-Adha. | Yes (Eid al-Adha days) |
| `aqiqah` | عقيقة | Sacrifice on the birth of a child. | No |
| `interest_purification` |, | Riba purification: disposal of interest income to charity without seeking reward. **Cannot be Zakat.** | No |
| `general` |, | Generic donation, no Islamic categorisation. | No |

A charity can extend this list with `x-` prefixed custom types (e.g. `x-mosque_building`), but the names above are the standard ones apps should rely on.

## Why each one needs distinct handling

### Zakat (`zakat`)

Zakat is not interchangeable with general donation. By Islamic law, Zakat funds can **only** be spent on the eight categories of recipient explicitly listed in the Quran (9:60):

1. **Fuqara** (the poor)
2. **Masakin** (the needy)
3. **'Amilin 'Alayha** (those employed to collect and administer Zakat, capped, in most scholarly opinions)
4. **Muallafat al-Qulub** (those whose hearts are to be reconciled)
5. **Fir-Riqab** (freeing those in bondage / debt slavery / modern slavery in contemporary fatawa)
6. **Gharimin** (those in debt for legitimate needs)
7. **Fi Sabilillah** (in the cause of Allah, broadly interpreted in modern jurisprudence)
8. **Ibn al-Sabil** (the stranded traveller)

Many serious Muslim donors want to know which of the eight Asnaf their Zakat is reaching. Charities like Islamic Relief, Muslim Hands, Human Appeal, and the IOM's Islamic Philanthropy Fund all publish their Zakat distribution policies.

**The `zakat_metadata` object:**

```jsonc
{
  "donation_type": "zakat",
  "zakat_metadata": {
    "asnaf_allocation": [
      { "asnaf": "fuqara", "percentage": 60 },
      { "asnaf": "masakin", "percentage": 30 },
      { "asnaf": "ibn_al_sabil", "percentage": 10 }
    ],
    "policy_url": "https://example.org/zakat-policy",
    "policy_version": "2026.1",
    "fatwa_references": [
      { "issuer": "International Islamic Fiqh Academy", "reference": "Resolution 165 (3/18)" }
    ],
    "fully_distributed_within_hijri_year": true,
    "admin_fee_deducted_from_zakat": false
  }
}
```

Two operational notes:

- **`admin_fee_deducted_from_zakat`** matters: many donors specifically want 100% of their Zakat to reach Asnaf, with admin paid from Sadaqah or other sources. Charities advertising "100% Zakat policy" set this to `false`. Apps SHOULD surface this in donor-facing UI.
- **`fully_distributed_within_hijri_year`** matters because some scholars hold that Zakat should be distributed promptly. Charities that ringfence and distribute within the Hijri year set this to `true`.

### Zakat al-Fitr (`zakat_al_fitr`)

A small fixed payment per family member due before the Eid al-Fitr prayer. Charities typically convert the traditional measure (sa') of staple food to a local cash equivalent (e.g. £5 in the UK in 2026, varies by year). Apps offering Zakat al-Fitr should:

- Show the per-head amount the charity has published for that Ramadan.
- Multiply by the number of people the donor is paying for.
- Enforce the time window so donations are processed before Eid prayer.

The `time_window` field on the charity's `donation_types` listing carries the open/close timestamps.

### Sadaqah (`sadaqah`)

The most flexible category. No restrictions on use. The `donation_type: "sadaqah"` is the safe default if you want Islamic categorisation without operational constraints.

### Sadaqah Jariyah (`sadaqah_jariyah`)

Donors expect the money to fund something long-lasting. Best practice is to link the donation to a specific project (water well, fruit tree, Quran print run, scholarship endowment). Charities expose these via `/funds` or `/campaigns`.

### Lillah (`lillah`)

Used in particular for masjid running costs (utilities, imam stipend, maintenance) where Zakat would not be appropriate.

### Waqf (`waqf`)

An endowment. Capital is preserved; only the return is distributed. Operationally, Waqf donations should be ringfenced from operational accounts. The spec currently models Waqf as a `donation_type`; a future version may promote it to its own resource with explicit principal/yield tracking.

### Fidya (`fidya`) and Kaffarah (`kaffarah`)

Both have fixed per-unit pricing set by the charity in line with scholarly consensus:

- Fidya: feed one poor person per missed fast (~£5/day at 2026 UK prices, charity-specific).
- Kaffarah: feed 60 poor people per deliberately broken obligatory fast (or 60 days of consecutive fasting, but the cash route is what the charity sees).

Apps should expose a calculator: `days_missed × per_day_amount`.

### Qurbani / Udhiya (`qurbani`)

The sacrifice of an animal (sheep, goat, cow share, camel share) during Eid al-Adha. Key constraints:

- **Time-locked.** Donations must be received in time for the charity to perform the sacrifice during the days of Tashreeq (Eid al-Adha and the three following days, per most scholars).
- **Animal type and country matter.** Donors often want to specify the animal and the country of distribution. The `qurbani_metadata` object carries this:

```jsonc
{
  "donation_type": "qurbani",
  "qurbani_metadata": {
    "animal": "sheep",                       // sheep | goat | cow_share | camel_share | cow_whole | camel_whole
    "beneficiary_country": "YE",
    "intention_for": "self",                 // self | family | deceased
    "deceased_name": null
  }
}
```

### Aqiqah (`aqiqah`)

A sacrifice on the birth of a child. The dedication carries the child's name.

```jsonc
{
  "donation_type": "aqiqah",
  "aqiqah_metadata": {
    "child_name": "Yusuf",
    "child_gender": "male",
    "animal": "sheep",
    "number_of_animals": 2
  }
}
```

### Interest Purification (`interest_purification`)

Some Muslims, observing the prohibition on Riba, dispose of interest accidentally earned (e.g. mandatory savings account interest in some jurisdictions) by giving it to charity without seeking spiritual reward. This is **not** Zakat and cannot be claimed as Zakat. Tagging it separately matters for the charity's accounting and for the donor's conscience.

## Donor experience: what apps should render

For a Muslim-oriented donation flow, the donor-facing UI typically needs:

1. A **donation type picker**, at minimum: Zakat, Sadaqah, Sadaqah Jariyah, Lillah. Time-locked types (Zakat al-Fitr, Qurbani) only appear when the window is open.
2. For Zakat specifically: a link to the charity's **Zakat policy** (from `zakat_metadata.policy_url` returned in `GET /charity` defaults, or per-campaign).
3. For Qurbani: animal picker + country picker.
4. For Fidya / Kaffarah: a small calculator.
5. A **dedication** field ("On behalf of my late father, may Allah have mercy on him").
6. The recurring frequency picker should include **daily** for Ramadan use cases.

## Zakat calculator endpoint (optional)

Charities can expose `/zakat/calculator` returning the current Nisab thresholds (gold and silver based) in their supported currencies:

```http
GET /zakat/calculator?currency=GBP

200 OK
{
  "nisab": {
    "gold_based": { "value": 569100, "currency": "GBP" },    // 87.48g × current price
    "silver_based": { "value": 51200, "currency": "GBP" },   // 612.36g × current price
    "as_of": "2026-05-27T00:00:00Z"
  },
  "rate": 0.025,
  "notes": "Most scholars use the silver Nisab as it is more inclusive of recipients."
}
```

The app then runs the calculation client-side: `if total_wealth > nisab then zakat_due = total_wealth × 0.025`.

## Trust and verification

Muslim donors care about Shariah compliance. Charities running OCAS in Muslim-serving contexts SHOULD expose, in the `/charity` response:

```jsonc
"shariah_compliance": {
  "scholars_or_board": "Internal Shariah Board",
  "fatwa_references": [
    { "issuer": "International Islamic Fiqh Academy", "year": 2021, "url": "..." }
  ],
  "annual_zakat_audit_url": "https://example.org/audits/2025-zakat.pdf",
  "hundred_percent_zakat_policy": true
}
```

None of these fields are required by the spec, but apps may filter or label charities that expose them.

## What this is not

- OCAS does **not** issue fatawa.
- OCAS does **not** verify Shariah compliance, that's the charity's responsibility and its scholars' responsibility.
- OCAS does **not** dictate how Zakat must be distributed, only how the data about distribution is shaped so donors can see it.

## Beyond Islam

The same `donation_type` + metadata pattern works for other faith traditions:

- Christian tithing: `donation_type: "tithe"` with a metadata block.
- Jewish ma'aser kesafim: `donation_type: "maaser"`.
- Hindu daana: `donation_type: "daana"`.
- Sikh dasvandh: `donation_type: "dasvandh"`.

These aren't in the v1 enum because the team building this first iteration doesn't have the lived expertise to model them correctly. **Pull requests from practitioners are very welcome.** The right people to model these are people who give in those traditions, not people who don't.
