// Minimal request validation.
//
// This is intentionally light. A production implementation would validate
// against the OpenAPI schema directly (e.g. with a library like express-openapi-
// validator). Here we hand-roll a few checks so the logic stays visible and the
// dependency list stays at exactly one package (express).

export function problem(status, code, message, field) {
  // Shape mirrors the OCAS Error schema.
  const body = { error: { code, message } };
  if (field) body.error.field = field;
  return { status, body };
}

// Validates a Money object: { value: integer >= 0, currency: 3-letter code }.
export function validateMoney(money, fieldPath) {
  if (money == null || typeof money !== 'object') {
    return problem(400, 'invalid_amount', 'Amount is required.', fieldPath);
  }
  if (!Number.isInteger(money.value)) {
    return problem(
      400,
      'invalid_amount',
      'Amount value must be an integer in minor units (e.g. 2500 for £25.00).',
      `${fieldPath}.value`,
    );
  }
  if (money.value <= 0) {
    return problem(400, 'invalid_amount', 'Amount must be greater than zero.', `${fieldPath}.value`);
  }
  if (typeof money.currency !== 'string' || !/^[A-Z]{3}$/.test(money.currency)) {
    return problem(
      400,
      'invalid_currency',
      'Currency must be a 3-letter ISO 4217 code, e.g. GBP.',
      `${fieldPath}.currency`,
    );
  }
  return null;
}

// The canonical OCAS donation types.
const DONATION_TYPES = new Set([
  'general',
  'zakat',
  'sadaqah',
  'sadaqah_jariyah',
  'waqf',
  'lillah',
  'fidya',
  'kaffarah',
  'qurbani',
  'udhiyyah',
  'aqiqah',
  'interest_purification',
]);

// The 8 canonical Asnaf (Qur'an 9:60).
const ASNAF = new Set([
  'fuqara',
  'masakin',
  'amilin_alayha',
  'muallafat_al_qulub',
  'fir_riqab',
  'gharimin',
  'fi_sabilillah',
  'ibn_al_sabil',
]);

export function validateDonationType(type) {
  if (typeof type !== 'string' || !DONATION_TYPES.has(type)) {
    return problem(
      400,
      'invalid_donation_type',
      `donation_type must be one of: ${[...DONATION_TYPES].join(', ')}.`,
      'donation_type',
    );
  }
  return null;
}

// If the donation is Zakat and includes asnaf_allocation, the percentages must
// be valid Asnaf categories and sum to 100. interest_purification can never be
// declared as Zakat.
export function validateZakatMetadata(donationType, zakatMetadata) {
  if (donationType === 'interest_purification' && zakatMetadata) {
    return problem(
      422,
      'invalid_zakat',
      'interest_purification cannot carry zakat_metadata; purification of interest is not Zakat.',
      'zakat_metadata',
    );
  }

  if (!zakatMetadata || !zakatMetadata.asnaf_allocation) return null;

  const allocation = zakatMetadata.asnaf_allocation;
  if (!Array.isArray(allocation) || allocation.length === 0) {
    return problem(400, 'invalid_zakat', 'asnaf_allocation must be a non-empty array.', 'zakat_metadata.asnaf_allocation');
  }

  let total = 0;
  for (const entry of allocation) {
    if (!ASNAF.has(entry.asnaf)) {
      return problem(
        400,
        'invalid_asnaf',
        `Unknown Asnaf category "${entry.asnaf}". Must be one of: ${[...ASNAF].join(', ')}.`,
        'zakat_metadata.asnaf_allocation',
      );
    }
    if (typeof entry.percentage !== 'number' || entry.percentage <= 0) {
      return problem(400, 'invalid_asnaf', 'Each Asnaf allocation needs a positive percentage.', 'zakat_metadata.asnaf_allocation');
    }
    total += entry.percentage;
  }

  if (Math.round(total) !== 100) {
    return problem(
      422,
      'invalid_zakat',
      `Asnaf allocation percentages must sum to 100 (got ${total}).`,
      'zakat_metadata.asnaf_allocation',
    );
  }

  return null;
}
