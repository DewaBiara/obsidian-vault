# 📘 Spesifikasi Teknis & Blueprint: tap-review-gateway (Claude Code Ready)

- **Target Implementasi:** Claude Code CLI
- **Nama Repositori Rekomendasi:** `tap-review-gateway`
- **Inisiator:** [[Dewa Biara]]
- **Tanggal:** 2026-09-24
- **Tautan Terkait:** [[01_Projects/Deep_Analysis_NFC_Review_SaaS_Bali]] | [[01_Projects/Arsitektur_Admin_dan_NFC_Provisioning_App]] | [[01_Projects/Strategi_Dual_Offering_Hardware_vs_SaaS]]

---

## 1. Ringkasan Proyek & Tujuan Arsitektur
Sistem ini merupakan platform **Dual-Tier Smart NFC Review Gateway & Admin Provisioning SaaS** untuk restoran, kafe, dan villa di Bali.
1. **Dual-Offering Model:** Mendukung **Opsi 1 (Beli Putus / Direct Redirect)** dan **Opsi 2 (Smart SaaS dengan Reputation Gate & Analitik)**.
2. **High-Throughput & Low-Latency:** Endpoint redirect Go dengan caching Redis berkecepatan sub-10ms.
3. **Zero Native App Overhead:** Provisioning penulisan chip NFC dilakukan langsung dari browser mobile admin menggunakan standar resmi **Web NFC API (`NDEFReader`)**.

---

## 2. Tech Stack & Struktur Direktori

- **Backend:** Go 1.22+ (Gin Web Framework), `pgx/v5` (PostgreSQL Driver), `go-redis/v9`.
- **Frontend:** Next.js 15 (App Router, Tailwind CSS, TypeScript, Web NFC API).
- **Database & Cache:** PostgreSQL 16 & Redis 7.
- **DevOps:** Docker & Docker Compose (`docker compose up`).

```
tap-review-gateway/
├── backend/
│   ├── cmd/server/main.go
│   ├── internal/
│   │   ├── config/config.go
│   │   ├── database/db.go
│   │   ├── handler/redirect.go
│   │   ├── handler/admin.go
│   │   ├── middleware/cors.go
│   │   ├── model/models.go
│   │   ├── repository/merchant_repo.go
│   │   └── service/redirect_service.go
│   ├── migrations/
│   │   └── 001_init.sql
│   ├── Dockerfile
│   └── go.mod
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── admin/page.tsx          (Dashboard & Provisioning PWA)
│   │   │   ├── f/[code]/page.tsx       (Smart Reputation Gate UI)
│   │   │   └── layout.tsx
│   │   ├── components/NfcWriterModal.tsx
│   │   └── lib/api.ts
│   ├── Dockerfile
│   └── package.json
└── docker-compose.yml
```

---

## 3. Skema Database PostgreSQL (`001_init.sql`)

```sql
-- 1. Merchants Table (Venues: Sawana Coffee, Villa Lateng, etc.)
CREATE TABLE merchants (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(150) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    category VARCHAR(50) NOT NULL DEFAULT 'fnb',
    google_place_id VARCHAR(150),
    direct_review_url TEXT NOT NULL,
    whatsapp_manager VARCHAR(30),
    smart_filter_enabled BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. Subscriptions Table (Dual-Tier Lifecycle)
CREATE TABLE subscriptions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    merchant_id UUID REFERENCES merchants(id) ON DELETE CASCADE,
    tier VARCHAR(50) NOT NULL DEFAULT 'lifetime_static', -- 'lifetime_static' | 'smart_saas'
    status VARCHAR(30) NOT NULL DEFAULT 'active',        -- 'trial' | 'active' | 'past_due' | 'suspended'
    trial_ends_at TIMESTAMPTZ,
    current_period_end TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. NFC Tags Table (Physical Stand per Table/Spot)
CREATE TABLE nfc_tags (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    merchant_id UUID REFERENCES merchants(id) ON DELETE CASCADE,
    tag_uid VARCHAR(100) UNIQUE,
    table_label VARCHAR(50) NOT NULL,
    slug_code VARCHAR(50) UNIQUE NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    total_taps INT DEFAULT 0,
    last_tapped_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX idx_nfc_tags_slug ON nfc_tags(slug_code);

-- 4. Tap Events Table (Analytics & Feedback Logs)
CREATE TABLE tap_events (
    id BIGSERIAL PRIMARY KEY,
    tag_id UUID REFERENCES nfc_tags(id) ON DELETE CASCADE,
    device_os VARCHAR(30),
    user_agent TEXT,
    rating_given INT,
    feedback_text TEXT,
    action_taken VARCHAR(50), -- 'direct_redirect' | 'rating_4_5_google' | 'rating_1_3_private'
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX idx_tap_events_tag_created ON tap_events(tag_id, created_at DESC);
```

---

## 4. Logika Bisnis & Fitur Inti

### A. Core Redirect Engine (`GET /t/:slug_code`)
1. **Cache Resolution:** Cari metadata tag di Redis (`tag:{slug_code}`). Jika miss, query DB lalu set Redis TTL 10 menit.
2. **Non-blocking Tap Counter:** Dispatch goroutine untuk increment `total_taps` dan simpan log ke `tap_events`.
3. **Dual-Tier Branching:**
   - Jika `tier == 'lifetime_static'` ATAU `smart_filter_enabled == false`: Return HTTP 302 Redirect ke `direct_review_url` (Google Maps).
   - Jika `tier == 'smart_saas'` DAN `smart_filter_enabled == true`: Return Redirect ke `/f/:slug_code`.

### B. Micro-Landing Smart Gate (`/f/:slug_code`)
- Tampilkan pertanyaan ramah: *"Bagaimana pengalaman Anda di {Nama Merchant}?"*
- Bintang 4–5: Langsung buka URL Google Review resmi.
- Bintang 1–3: Muncul form masukan internal singkat. Saat dikirim, menghasilkan link WhatsApp ke manajer resto dengan draf komplain siap kirim.
- Footer Compliance: Link teks netral *"Tetap ingin menulis ulasan di Google Maps? Klik di sini"*.

### C. Web NFC Provisioning PWA (`/admin`)
- Form admin di smartphone Android: Pilih Merchant -> Masukkan Nomor Meja -> Klik **"Write Tag"**.
- Browser Web NFC API menulis URL `https://<domain>/t/<slug_code>` ke chip dalam 1 detik.

---

## 5. PROMPT SIAP PAKAI UNTUK CLAUDE CODE CLI

Salin teks berikut dan tempelkan ke sesi Claude Code milikmu:

```text
Buatkan repositori bernama `tap-review-gateway` yang merupakan sistem Dual-Tier Smart NFC Review Gateway & Admin Provisioning SaaS untuk restoran, kafe, dan villa di Bali.

Stack Teknis:
- Backend: Go 1.22+ (Gin Web Framework), PostgreSQL (database), Redis (caching URL redirect), Docker & Docker Compose.
- Frontend: Next.js 15 (App Router, Tailwind CSS, TypeScript) mencakup:
  1. Halaman Public Smart Gate (`/f/[code]`): responsif mobile, micro-page untuk menyaring rating bintang 1-5. Rating 4-5 langsung ke Google Review, rating 1-3 membuka form komplain privat ke WhatsApp manajer.
  2. Halaman Admin PWA (`/admin`): CRUD Merchant, CRUD NFC Tag, manajemen paket Beli Putus vs SaaS, serta fitur Provisioning NFC menggunakan browser Web NFC API (`NDEFReader`).

Fitur Kunci Backend:
1. Endpoint `GET /t/:slug_code`: redirect latensi rendah (<10ms) dengan Redis cache hit. Jika tier `lifetime_static` -> HTTP 302 langsung ke Google Maps. Jika tier `smart_saas` -> redirect ke `/f/:slug_code`.
2. Async Event Logger: pencatatan log tap ke tabel PostgreSQL secara non-blocking via goroutine.
3. REST API CRUD Admin di `/api/v1/merchants` dan `/api/v1/tags`.
4. Endpoint Feedback di `/api/v1/feedback` untuk menerima masukan bintang 1-3.

Sertakan:
- File migrasi database PostgreSQL lengkap.
- Dockerfile untuk backend dan frontend, serta `docker-compose.yml` yang langsung berjalan siap pakai.
- Seed data awal untuk merchant 'Sawana Coffee & Eatery' (slug: sawana-coffee) dan 'Villa Lateng Ubud' (slug: villa-lateng).
- Automated unit test untuk redirect handler dan service.
```
