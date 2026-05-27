# Authentication

OCAS supports three authentication modes. The mode is declared by the charity in `GET /charity` and apps should branch on it. The same OCAS-compliant app can therefore work transparently against a small village mosque running in `public` mode and against a large international NGO running full OAuth 2.0.

## The three modes

### Mode 1: `public`

No authentication required for `POST /donations` and other write endpoints that operate on a single resource owned by the requester.

**Use when:**
- The charity wants the maximum possible embedding surface.
- Donations don't need to be linked to a donor account.
- Read endpoints (`/campaigns`, `/charity`) are always public anyway.

**Risk profile:** the charity must protect itself against abuse with rate limits, anti-fraud (CAPTCHA on the front end, AVS / 3DS on the payment), and donation minima/maxima. The OCAS server itself does not authenticate the caller; the *payment processor* enforces fraud rules at the point of money movement.

**Listing endpoints** (e.g. `GET /donations` returning everyone's donations) are **never** exposed in `public` mode. They require at least an API key.

### Mode 2: `api_key`

The charity issues one or more long-lived bearer tokens. Each token is associated with a partner app and a set of scopes.

```http
Authorization: Bearer ocas_live_partner_a8f3e9c2d4b6...
```

Scopes follow the pattern `<resource>:<action>`:

- `donations:write`, create donations on behalf of users
- `donations:read`, read donations (typically scoped to the partner's own donations)
- `subscriptions:write`
- `subscriptions:read`
- `campaigns:read` (often public anyway, but required if the charity hides drafts)
- `donors:read`, `donors:write`
- `webhooks:manage`

**Use when:**
- Trusted partner integrations (a faith-based app, a CRM, a workplace giving platform).
- Server-to-server. The token is never exposed to a browser or mobile client.

**Token format:** opaque, prefixed `ocas_live_` or `ocas_test_`, minimum 32 bytes of entropy after the prefix. Charities are encouraged to rotate keys and offer key revocation through their admin UI.

**Where to put the secret:** the partner app's server-side env vars / secret manager. Never ship in a mobile binary; if you need to donate from a mobile app, either use `public` mode against an OCAS server that accepts unauthenticated donations, or proxy through your own backend.

### Mode 3: `oauth2`

Full OAuth 2.0 Authorization Code Flow with PKCE (RFC 7636) for public clients, and Client Credentials for server-to-server. The charity exposes:

- `GET /.well-known/oauth-authorization-server`, RFC 8414 metadata document
- `GET /oauth/authorize`
- `POST /oauth/token`
- `POST /oauth/revoke`
- `POST /oauth/introspect` (optional, RFC 7662)

**Use when:**
- Donors have accounts at the charity.
- The app needs to act on behalf of a specific donor (read their donation history, manage their subscriptions).
- The charity wants to issue short-lived access tokens with refresh tokens.

**Scopes** (in addition to those above):
- `openid`, return an ID token
- `profile`, `email`, standard OIDC scopes
- `donor:self`, operate on the authenticated donor's resources only

**ID Token:** if the charity supports OpenID Connect, an ID token signed with RS256 or ES256 SHOULD be returned alongside the access token. Apps can then identify the donor without an additional `/userinfo` call.

**Token lifetime:** access tokens SHOULD expire within 1 hour. Refresh tokens MAY be long-lived but MUST be revocable.

## Discovery: how an app knows which mode to use

```http
GET /charity HTTP/1.1
Host: example-charity.org

200 OK
Content-Type: application/json

{
  "name": "Example Charity",
  "legal_name": "Example Charity Limited",
  "registration_numbers": [
    { "jurisdiction": "GB", "type": "charity_commission", "value": "1234567" },
    { "jurisdiction": "GB", "type": "hmrc_charities", "value": "AB12345" }
  ],
  "auth": {
    "mode": "oauth2",
    "discovery_url": "https://example-charity.org/.well-known/oauth-authorization-server",
    "supported_scopes": ["openid", "profile", "email", "donations:write", "donor:self"]
  },
  ...
}
```

For `public` mode:

```json
"auth": { "mode": "public" }
```

For `api_key` mode:

```json
"auth": {
  "mode": "api_key",
  "key_request_url": "https://example-charity.org/developers/apply",
  "header_format": "Bearer"
}
```

## Choosing a mode (for charities)

| You are... | Recommended mode |
|---|---|
| A small mosque or local charity, want to maximise reach | `public` |
| A mid-sized charity with a few partner integrations | `api_key` |
| A large charity with a donor portal | `oauth2` |
| A charity using a SaaS CRM that already does OAuth | `oauth2` |

You can also support multiple modes simultaneously: e.g. `public` for anonymous one-off donations and `oauth2` for donor-account features. Declare the primary mode in `GET /charity`; the OAuth metadata document is always discoverable separately if present.

## Transport security

- TLS 1.2 minimum, TLS 1.3 recommended. Plain HTTP is rejected.
- HSTS recommended with `max-age=31536000; includeSubDomains`.
- HTTP/2 or HTTP/3 recommended for performance, not required.

## Idempotency

`POST /donations` and `POST /subscriptions` SHOULD support the `Idempotency-Key` header. Sending the same key with the same body returns the original response without creating a duplicate. Keys SHOULD be at least 16 bytes of entropy and SHOULD be retained server-side for 24 hours minimum.

```http
POST /donations
Idempotency-Key: 7f3e8a2c-1d4b-4f8e-9c3a-2b5d6e7f8901
```

## Rate limiting

The spec doesn't mandate specific limits, but charities running OCAS in `public` mode SHOULD:

- Limit `POST /donations` to a small number per IP per minute.
- Apply a global limit per charity to avoid pricing surprises with the payment processor.
- Return `429 Too Many Requests` with `Retry-After` header.

## Webhooks (server-side auth, in reverse)

When the charity calls *out* to a registered webhook URL, it signs the request body with HMAC-SHA256:

```http
POST /webhook
Content-Type: application/json
OCAS-Signature: t=1735689600,v1=5257a869e7ecebeda32affa62cdca3fa51cad7e77a0e56ff536d0ce8e108d8bd
OCAS-Event: donation.completed

{ ... }
```

The receiver verifies by computing `HMAC-SHA256(secret, "{t}.{body}")` and constant-time-comparing with `v1`. Timestamps older than 5 minutes are rejected to prevent replay.

## Future work

- DPoP (RFC 9449) for stronger token binding in browser clients.
- mTLS for very high-trust server-to-server use cases (e.g. regulators).
- WebAuthn for donor authentication where supported.


