# Dogfood QA & Security Audit Report: KULA POS Landing Page

**Target:** https://kula.sawanaubud.com
**Date:** October 7, 2026
**Scope:** Landing Page QA, Form Validation, Honeypot Anti-Bot Mechanism, Lead Rate Limiting, Asset Integrity, and SEO/OpenGraph Audit.
**Tester:** Hermes Agent (automated web & security QA)

---

## Executive Summary

| Severity | Count |
|----------|-------|
| 🔴 Critical | 0 |
| 🟠 High | 0 |
| 🟡 Medium | 1 |
| 🔵 Low | 1 |
| **Total** | **2** |

**Overall Assessment:** **Sangat Baik & Aman.**
Landing page `kula.sawanaubud.com` memiliki perlindungan anti-spam formulir yang luar biasa: kombinasi **honeypot trap** untuk menipu bot (mengembalikan fake 202 Accepted), validasi input ketat (Go backend), serta **rate limiter agresif** dengan cooldown window 10 menit (`Retry-After: 600s`). Semua aset dan link statis bebas dari broken link (404).

---

## Hasil Pengujian & Temuan

### 1. Form Early Access & Proteksi Anti-Bot (PASS - Excellent)
* **Honeypot Trap (`website` hidden input):**
  * Teruji dengan memasukkan URL spam pada field tersembunyi `name="website"`.
  * Hasil: Server merespons `202 {"status":"received"}`. Bot penyerang mengira berhasil, padahal payload langsung di-drop tanpa mengotori database.
* **Validasi Skema Lead (`POST /api/v1/leads`):**
  * Validasi nama (2–100 karakter), nomor WhatsApp (harus berformat nomor utuh), email (sintaks valid), tipe bisnis (whitelist: CAFE, RESTAURANT, BAR, BAKERY, OTHER), dan consent checkbox.
* **Rate Limiting Form Leads:**
  * Teruji dengan pengiriman beruntun.
  * Hasil: Setelah batas wajar terlampaui, request langsung diblokir dengan `HTTP 429 RATE_LIMITED` dengan durasi cooldown 10 menit (`Retry-After: ~600 detik`).

### 2. Keamanan & Header HTTP (PASS)
* `Strict-Transport-Security: max-age=31536000` (HSTS aktif)
* `X-Frame-Options: DENY` (Anti-clickjacking / iframe embedding)
* `X-Content-Type-Options: nosniff` (MIME sniffing protection)
* `Referrer-Policy: strict-origin-when-cross-origin`

### 3. Integritas Aset & Navigasi (PASS)
* Seluruh link anchor (`#top`, `#fitur`, `#cara-kerja`, `#harga`, `#faq`, `#daftar`) berfungsi normal.
* Link eksternal (WhatsApp direct chat dengan template pesan, login Backoffice) valid.
* Halaman legal `/kebijakan-privasi/` berstatus `200 OK`.
* 0 broken image / 0 failed JS/CSS chunks. Total bundle awal sangat efisien (~710 KB uncompressed / ~200 KB compressed).

---

## Rekomendasi Peningkatan

### 1. Meta Tag `og:image` Belum Terpasang (Medium)
* **Temuan:** Meta tag OpenGraph (`og:title`, `og:description`, `twitter:card`) sudah ada, tetapi belum memiliki `og:image` dan `twitter:image`.
* **Dampak:** Saat link `kula.sawanaubud.com` dibagikan di WhatsApp, Twitter/X, atau Telegram, kartu pratinjau (link preview) tidak menampilkan gambar/banner, sehingga rasio klik (*Click-Through Rate*) berkurang.
* **Solusi:** Tambahkan tag:
  ```html
  <meta property="og:image" content="https://kula.sawanaubud.com/og-banner.png" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="630" />
  <meta name="twitter:image" content="https://kula.sawanaubud.com/og-banner.png" />
  ```

### 2. Nomor WhatsApp Konsistensi (Low)
* Link WhatsApp di footer/tombol bantuan menggunakan nomor `+628970087058`. Pastikan nomor ini sudah terhubung dengan bot/operator WhatsApp Business resmi KULA.
