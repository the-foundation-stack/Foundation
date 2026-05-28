// OCAS reference server.
//
// A barebones, in-memory implementation of the Open Charity API Standard.
// Run with: npm start
//
// Base path matches the spec: /api/ocas/v1
//
// This server runs in "public" auth mode, so no credentials are needed. It is
// for learning and conformance testing, NOT production: there's no persistence,
// no real payment processing, no rate limiting, and no authentication.

import express from 'express';
import { db, nextId } from './store.js';
import {
  problem,
  validateMoney,
  validateDonationType,
  validateZakatMetadata,
} from './validation.js';

const app = express();
app.use(express.json());

const BASE = '/api/ocas/v1';

// Tiny helper to send a problem response.
function sendProblem(res, p) {
  res.status(p.status).json(p.body);
}

// Fire any registered webhooks for an event. In this reference server we just
// log them rather than making real HTTP calls, so you can see what would be
// sent without needing a receiver.
function emitWebhook(eventType, data) {
  const subscribers = db.webhooks.filter(
    (w) => w.active && w.events.includes(eventType),
  );
  for (const w of subscribers) {
    const event = {
      id: nextId('evt'),
      type: eventType,
      created_at: new Date().toISOString(),
      api_version: '1.0',
      data,
    };
    // A real implementation would POST this to w.url with an OCAS-Signature
    // header (HMAC-SHA256 over the body). Here we just log it.
    console.log(`[webhook] would POST ${eventType} to ${w.url}:`, JSON.stringify(event));
  }
}

// ---------------------------------------------------------------------------
// Charity
// ---------------------------------------------------------------------------

// GET /charity — always public, advertises capabilities.
app.get(`${BASE}/charity`, (req, res) => {
  res.json(db.charity);
});

// ---------------------------------------------------------------------------
// Campaigns
// ---------------------------------------------------------------------------

app.get(`${BASE}/campaigns`, (req, res) => {
  res.json({ data: db.campaigns });
});

app.get(`${BASE}/campaigns/:id`, (req, res) => {
  const campaign = db.campaigns.find((c) => c.id === req.params.id);
  if (!campaign) {
    return sendProblem(res, problem(404, 'not_found', 'Campaign not found.'));
  }
  res.json(campaign);
});

// ---------------------------------------------------------------------------
// Funds
// ---------------------------------------------------------------------------

app.get(`${BASE}/funds`, (req, res) => {
  res.json({ data: db.funds });
});

app.get(`${BASE}/funds/:id`, (req, res) => {
  const fund = db.funds.find((f) => f.id === req.params.id);
  if (!fund) {
    return sendProblem(res, problem(404, 'not_found', 'Fund not found.'));
  }
  res.json(fund);
});

// ---------------------------------------------------------------------------
// Donations
// ---------------------------------------------------------------------------

app.post(`${BASE}/donations`, (req, res) => {
  const body = req.body || {};

  // Validate amount.
  const moneyErr = validateMoney(body.amount, 'amount');
  if (moneyErr) return sendProblem(res, moneyErr);

  // Validate donation type.
  const typeErr = validateDonationType(body.donation_type);
  if (typeErr) return sendProblem(res, typeErr);

  // Validate Zakat rules.
  const zakatErr = validateZakatMetadata(body.donation_type, body.zakat_metadata);
  if (zakatErr) return sendProblem(res, zakatErr);

  // Validate the campaign and fund exist, if referenced.
  if (body.campaign_id && !db.campaigns.find((c) => c.id === body.campaign_id)) {
    return sendProblem(res, problem(422, 'invalid_reference', 'Referenced campaign does not exist.', 'campaign_id'));
  }
  if (body.fund_id && !db.funds.find((f) => f.id === body.fund_id)) {
    return sendProblem(res, problem(422, 'invalid_reference', 'Referenced fund does not exist.', 'fund_id'));
  }

  // Idempotency: if an Idempotency-Key header was sent and we've seen it, return
  // the original donation rather than creating a duplicate.
  const idemKey = req.get('Idempotency-Key');
  if (idemKey) {
    const existing = db.donations.find((d) => d._idempotency_key === idemKey);
    if (existing) {
      return res.status(200).json(stripInternal(existing));
    }
  }

  const now = new Date().toISOString();
  const donation = {
    id: nextId('don'),
    amount: body.amount,
    donation_type: body.donation_type,
    donor: body.donor
      ? { id: nextId('donor'), ...body.donor }
      : null,
    anonymous: body.anonymous ?? false,
    campaign_id: body.campaign_id ?? null,
    fund_id: body.fund_id ?? null,
    beneficiary_country: body.beneficiary_country ?? null,
    message: body.message ?? null,
    tax_relief_declarations: body.tax_relief_declarations ?? [],
    zakat_metadata: body.zakat_metadata ?? null,
    qurbani_metadata: body.qurbani_metadata ?? null,
    aqiqah_metadata: body.aqiqah_metadata ?? null,
    cover_fees: body.cover_fees ?? false,
    status: 'completed', // No real payment step; we mark it completed instantly.
    payment: {
      processor: 'reference-sandbox',
      processor_ref: nextId('pay'),
      method_used: body.payment_method_preference ?? 'card',
      completed_at: now,
    },
    receipt_id: null,
    created_at: now,
    _idempotency_key: idemKey ?? null,
  };

  // Generate a receipt.
  const receipt = {
    id: nextId('rcpt'),
    donation_id: donation.id,
    issued_at: now,
    amount: donation.amount,
    donor_name: donation.donor
      ? `${donation.donor.first_name ?? ''} ${donation.donor.last_name ?? ''}`.trim()
      : 'Anonymous',
    charity_name: db.charity.name,
    charity_registration_numbers: db.charity.registration_numbers,
    tax_relief_schemes_applied: (donation.tax_relief_declarations || []).map((d) => d.scheme),
    pdf_url: null,
    locale: 'en-GB',
  };
  donation.receipt_id = receipt.id;

  db.donations.push(donation);
  db.receipts.push(receipt);

  emitWebhook('donation.completed', { donation: stripInternal(donation) });

  res.status(201).json(stripInternal(donation));
});

app.get(`${BASE}/donations`, (req, res) => {
  res.json({ data: db.donations.map(stripInternal) });
});

app.get(`${BASE}/donations/:id`, (req, res) => {
  const donation = db.donations.find((d) => d.id === req.params.id);
  if (!donation) {
    return sendProblem(res, problem(404, 'not_found', 'Donation not found.'));
  }
  res.json(stripInternal(donation));
});

app.post(`${BASE}/donations/:id/refund`, (req, res) => {
  const donation = db.donations.find((d) => d.id === req.params.id);
  if (!donation) {
    return sendProblem(res, problem(404, 'not_found', 'Donation not found.'));
  }
  if (donation.status === 'refunded') {
    return sendProblem(res, problem(409, 'already_refunded', 'Donation has already been refunded.'));
  }
  donation.status = 'refunded';
  emitWebhook('donation.refunded', { donation: stripInternal(donation) });
  res.json(stripInternal(donation));
});

// ---------------------------------------------------------------------------
// Subscriptions
// ---------------------------------------------------------------------------

app.post(`${BASE}/subscriptions`, (req, res) => {
  const body = req.body || {};

  const moneyErr = validateMoney(body.amount, 'amount');
  if (moneyErr) return sendProblem(res, moneyErr);

  const typeErr = validateDonationType(body.donation_type);
  if (typeErr) return sendProblem(res, typeErr);

  const validFreq = ['daily', 'weekly', 'monthly', 'quarterly', 'annually'];
  if (!validFreq.includes(body.frequency)) {
    return sendProblem(res, problem(400, 'invalid_frequency', `frequency must be one of: ${validFreq.join(', ')}.`, 'frequency'));
  }

  const now = new Date().toISOString();
  const sub = {
    id: nextId('sub'),
    amount: body.amount,
    frequency: body.frequency,
    donation_type: body.donation_type,
    donor: body.donor ? { id: nextId('donor'), ...body.donor } : null,
    fund_id: body.fund_id ?? null,
    start_at: body.start_at ?? now,
    max_payments: body.max_payments ?? null,
    status: 'active',
    created_at: now,
    next_payment_at: body.start_at ?? now,
    payments_completed: 0,
    total_donated: { value: 0, currency: body.amount.currency },
    anonymous: body.anonymous ?? false,
  };

  db.subscriptions.push(sub);
  res.status(201).json(sub);
});

app.get(`${BASE}/subscriptions`, (req, res) => {
  res.json({ data: db.subscriptions });
});

app.get(`${BASE}/subscriptions/:id`, (req, res) => {
  const sub = db.subscriptions.find((s) => s.id === req.params.id);
  if (!sub) return sendProblem(res, problem(404, 'not_found', 'Subscription not found.'));
  res.json(sub);
});

app.patch(`${BASE}/subscriptions/:id`, (req, res) => {
  const sub = db.subscriptions.find((s) => s.id === req.params.id);
  if (!sub) return sendProblem(res, problem(404, 'not_found', 'Subscription not found.'));
  // Only amount and status are editable in this reference server.
  if (req.body.amount) {
    const moneyErr = validateMoney(req.body.amount, 'amount');
    if (moneyErr) return sendProblem(res, moneyErr);
    sub.amount = req.body.amount;
  }
  if (req.body.status && ['active', 'paused'].includes(req.body.status)) {
    sub.status = req.body.status;
  }
  res.json(sub);
});

app.delete(`${BASE}/subscriptions/:id`, (req, res) => {
  const sub = db.subscriptions.find((s) => s.id === req.params.id);
  if (!sub) return sendProblem(res, problem(404, 'not_found', 'Subscription not found.'));
  sub.status = 'cancelled';
  res.json(sub);
});

// ---------------------------------------------------------------------------
// Receipts
// ---------------------------------------------------------------------------

app.get(`${BASE}/receipts/:id`, (req, res) => {
  const receipt = db.receipts.find((r) => r.id === req.params.id);
  if (!receipt) return sendProblem(res, problem(404, 'not_found', 'Receipt not found.'));
  res.json(receipt);
});

// ---------------------------------------------------------------------------
// Zakat calculator
// ---------------------------------------------------------------------------

app.get(`${BASE}/zakat/calculator`, (req, res) => {
  // Static illustrative Nisab values. A real implementation would fetch live
  // gold/silver prices.
  res.json({
    nisab: {
      gold_based: { value: 542500, currency: 'GBP' },
      silver_based: { value: 41200, currency: 'GBP' },
      as_of: new Date().toISOString(),
    },
    rate: 0.025,
    notes: 'Illustrative values from the reference server. Consult a scholar where uncertain.',
  });
});

// ---------------------------------------------------------------------------
// Webhooks
// ---------------------------------------------------------------------------

app.post(`${BASE}/webhooks`, (req, res) => {
  const body = req.body || {};
  if (typeof body.url !== 'string' || !/^https?:\/\//.test(body.url)) {
    return sendProblem(res, problem(400, 'invalid_url', 'Webhook url must be an http(s) URL.', 'url'));
  }
  if (!Array.isArray(body.events) || body.events.length === 0) {
    return sendProblem(res, problem(400, 'invalid_events', 'At least one event must be subscribed.', 'events'));
  }
  const webhook = {
    id: nextId('wh'),
    url: body.url,
    events: body.events,
    description: body.description ?? null,
    active: true,
    created_at: new Date().toISOString(),
  };
  db.webhooks.push(webhook);
  res.status(201).json(webhook);
});

app.get(`${BASE}/webhooks`, (req, res) => {
  res.json({ data: db.webhooks });
});

app.delete(`${BASE}/webhooks/:id`, (req, res) => {
  const idx = db.webhooks.findIndex((w) => w.id === req.params.id);
  if (idx === -1) return sendProblem(res, problem(404, 'not_found', 'Webhook not found.'));
  db.webhooks.splice(idx, 1);
  res.status(204).end();
});

// ---------------------------------------------------------------------------
// Fallbacks
// ---------------------------------------------------------------------------

// Root redirect for convenience.
app.get('/', (req, res) => {
  res.json({
    message: 'OCAS reference server. See the spec at https://the-foundation-stack.github.io/Foundation/open-charity-api/',
    base_path: BASE,
    try: `${BASE}/charity`,
  });
});

app.use((req, res) => {
  sendProblem(res, problem(404, 'not_found', `No route for ${req.method} ${req.path}.`));
});

// Remove internal bookkeeping fields before returning an object to the client.
function stripInternal(obj) {
  const clone = { ...obj };
  delete clone._idempotency_key;
  return clone;
}

const PORT = process.env.PORT || 3000;

// Only start listening if run directly (not when imported by tests).
if (process.argv[1] && process.argv[1].endsWith('server.js')) {
  app.listen(PORT, () => {
    console.log(`OCAS reference server listening on http://localhost:${PORT}`);
    console.log(`Try: curl http://localhost:${PORT}${BASE}/charity`);
  });
}

export { app };
