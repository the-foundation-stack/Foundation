// Basic conformance-style tests for the OCAS reference server.
// Run with: npm test
//
// Uses Node's built-in test runner and the global fetch (Node 20+), so there
// are no test dependencies to install.

import { test, before, after } from 'node:test';
import assert from 'node:assert/strict';
import { app } from '../src/server.js';

let server;
let base;

before(async () => {
  await new Promise((resolve) => {
    server = app.listen(0, () => {
      const { port } = server.address();
      base = `http://localhost:${port}/api/ocas/v1`;
      resolve();
    });
  });
});

after(() => {
  server.close();
});

test('GET /charity returns the capability profile', async () => {
  const res = await fetch(`${base}/charity`);
  assert.equal(res.status, 200);
  const body = await res.json();
  assert.equal(body.name, 'Hope Mosque Foundation');
  assert.ok(Array.isArray(body.supported_donation_types));
  assert.ok(body.supported_donation_types.includes('zakat'));
});

test('POST /donations creates a donation and a receipt', async () => {
  const res = await fetch(`${base}/donations`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      amount: { value: 2500, currency: 'GBP' },
      donation_type: 'sadaqah',
      donor: { first_name: 'Aisha', last_name: 'Khan', email: 'aisha@example.com' },
    }),
  });
  assert.equal(res.status, 201);
  const body = await res.json();
  assert.ok(body.id.startsWith('don_'));
  assert.equal(body.status, 'completed');
  assert.ok(body.receipt_id, 'a receipt should be generated');

  // The receipt should be fetchable.
  const receiptRes = await fetch(`${base}/receipts/${body.receipt_id}`);
  assert.equal(receiptRes.status, 200);
  const receipt = await receiptRes.json();
  assert.equal(receipt.donation_id, body.id);
});

test('POST /donations rejects a zero amount', async () => {
  const res = await fetch(`${base}/donations`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      amount: { value: 0, currency: 'GBP' },
      donation_type: 'sadaqah',
    }),
  });
  assert.equal(res.status, 400);
  const body = await res.json();
  assert.equal(body.error.code, 'invalid_amount');
});

test('POST /donations rejects Zakat whose Asnaf does not sum to 100', async () => {
  const res = await fetch(`${base}/donations`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      amount: { value: 2500, currency: 'GBP' },
      donation_type: 'zakat',
      zakat_metadata: {
        asnaf_allocation: [
          { asnaf: 'fuqara', percentage: 50 },
          { asnaf: 'masakin', percentage: 40 },
        ],
      },
    }),
  });
  assert.equal(res.status, 422);
  const body = await res.json();
  assert.equal(body.error.code, 'invalid_zakat');
});

test('POST /donations rejects interest_purification carrying zakat_metadata', async () => {
  const res = await fetch(`${base}/donations`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      amount: { value: 2500, currency: 'GBP' },
      donation_type: 'interest_purification',
      zakat_metadata: { asnaf_allocation: [{ asnaf: 'fuqara', percentage: 100 }] },
    }),
  });
  assert.equal(res.status, 422);
  const body = await res.json();
  assert.equal(body.error.code, 'invalid_zakat');
});

test('Idempotency-Key prevents duplicate donations', async () => {
  const payload = {
    amount: { value: 1000, currency: 'GBP' },
    donation_type: 'sadaqah',
  };
  const headers = {
    'Content-Type': 'application/json',
    'Idempotency-Key': 'test-key-123',
  };
  const first = await fetch(`${base}/donations`, {
    method: 'POST', headers, body: JSON.stringify(payload),
  });
  const firstBody = await first.json();
  assert.equal(first.status, 201);

  const second = await fetch(`${base}/donations`, {
    method: 'POST', headers, body: JSON.stringify(payload),
  });
  const secondBody = await second.json();
  assert.equal(second.status, 200, 'replay should return 200, not create a new one');
  assert.equal(secondBody.id, firstBody.id, 'replay should return the same donation');
});

test('POST /donations/:id/refund marks a donation refunded', async () => {
  const create = await fetch(`${base}/donations`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ amount: { value: 500, currency: 'GBP' }, donation_type: 'sadaqah' }),
  });
  const donation = await create.json();

  const refund = await fetch(`${base}/donations/${donation.id}/refund`, { method: 'POST' });
  assert.equal(refund.status, 200);
  const refunded = await refund.json();
  assert.equal(refunded.status, 'refunded');
});
