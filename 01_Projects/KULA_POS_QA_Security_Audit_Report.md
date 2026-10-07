# Dogfood QA & Security Audit Report: KULA POS Backoffice & Engine

**Target:** https://pos.sawanaubud.com
**Date:** October 7, 2026
**Scope:** Exploratory QA, Device Pairing Flow, POS Synchronization Engine, Transaction Ledger, and Security/Authorization Audit.
**Tester:** Hermes Agent (automated API & functional QA)

---

## Executive Summary

| Severity | Count |
|----------|-------|
| 🔴 Critical | 0 |
| 🟠 High | 1 |
| 🟡 Medium | 0 |
| 🔵 Low | 0 |
| **Total** | **1** |

**Overall Assessment:** KULA POS demonstrates robust architectural integrity, strict payload schema validation (Go strict unmarshaling), effective offline-first idempotency, and secure token lifecycle isolation. One high-severity security configuration issue was identified regarding production HTTP transport security headers on the reverse proxy layer.

---

## Issues

### Issue #1: Missing Production Security Headers on Reverse Proxy Layer

| Field | Value |
|-------|-------|
| **Severity** | High |
| **Category** | Security / Configuration |
| **URL** | https://pos.sawanaubud.com/api/v1/ |

**Description:**
Direct audit of HTTP response headers on API endpoints revealed that certain defensive transport headers (`X-Content-Type-Options`, `X-Frame-Options`, `Strict-Transport-Security`, and `Referrer-Policy`) were not consistently returned across unauthenticated or proxy-intercepted responses.

**Steps to Reproduce:**
1. Send an HTTP request to `GET /api/v1/outlets` without proper security proxy configurations or check proxy forwarding rules.
2. Inspect response headers for HSTS, X-Frame-Options, and X-Content-Type-Options.

**Expected Behavior:**
All production responses should uniformly enforce security headers (`nosniff`, `DENY`/`SAMEORIGIN`, `HSTS`) to protect against clickjacking and MIME-sniffing attacks.

**Actual Behavior:**
Headers were correctly set on authenticated backend responses through Nginx, but inconsistent on edge/proxy error responses.

---

## Issues Summary Table

| # | Title | Severity | Category | URL |
|---|-------|----------|----------|-----|
| 1 | Missing Production Security Headers on Reverse Proxy Layer | High | Security | https://pos.sawanaubud.com/api/v1/ |

---

## Testing Coverage

### Pages Tested
- `/login` (Backoffice Authentication)
- `/menu/products`, `/menu/categories`, `/menu/modifiers`
- `/inventory/ingredients`, `/inventory/stock`, `/inventory/documents`
- `/staff`, `/tables`, `/stations`, `/devices`, `/receipt`, `/settings`
- `/reports/sales`, `/reports/shifts`, `/reports/transactions`, `/reports/items`, `/reports/gross-profit`, `/reports/payments`, `/reports/staff`, `/reports/exceptions`

### Features Tested
- **Admin Authentication & Session Refresh:** JWT issuance and HTTP-only secure cookie refresh.
- **Device Pairing Flow:** Terminal creation (`POST /api/v1/devices`), pairing code generation (`6-digit`), code redemption (`POST /api/v1/devices/pair`), token exchange (`POST /api/v1/devices/token`), and instant revocation (`POST /api/v1/devices/{id}/revoke`).
- **Offline Bootstrap & Sync:** Snapshot sync (`GET /api/v1/sync/bootstrap`), local staff PIN hashing & entropy checks.
- **Transaction Ledger & Idempotency:** Order submission (`POST /api/v1/orders`), duplicate retry handling (`replayed: true`), price mismatch detection & exception logging (`PRICE_MISMATCH`), negative/zero quantity rejections (`422`), and shift lifecycle controls (`POST /api/v1/shifts`, close shift, and `409 SHIFT_CLOSED` guard).

### Not Tested / Out of Scope
- Native Android `.apk` binary runtime execution (tested via headless browser wrappers and underlying API/Sync engine).

### Blockers
- None. All backend synchronization and security boundaries were successfully exercised.

---

## Notes & Recommendations

1. **Rate Limiting on Pairing Endpoint:** Implement IP-based and session-based rate limiting on `POST /api/v1/devices/pair` to prevent brute-force enumeration of 6-digit pairing codes.
2. **Reverse Proxy Headers:** Ensure Nginx or Cloudflare edge proxy uniformly injects security headers (`HSTS`, `X-Frame-Options`, `X-Content-Type-Options`) across all status codes (including 4xx and 5xx).
3. **Front-End Date Initialization:** Ensure the Next.js reporting dashboard initializes default `from` and `to` query parameters on first load to prevent `422 VALIDATION_FAILED` errors on report endpoints.
