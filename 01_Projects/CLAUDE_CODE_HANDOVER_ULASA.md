# 🚀 CLAUDE CODE HANDOVER SPECIFICATION: ULASA (Smart NFC Review & Reputation SaaS)

> **Dokumen Handover Teknis Resmi untuk Claude Code CLI**  
> Proyek: **ULASA** (`ulasa-gateway`)  
> Brand: **ULASA** — *"One Tap. Five Stars."*  
> Inisiator: I Dewa Gde Putra Anga Biara (Dewa Biara)  
> Tanggal: 2026-09-24  

---

## 📌 1. RINGKASAN PROYEK & TUJUAN ARSITEKTUR

**ULASA** adalah platform *Dual-Tier Smart NFC Review Gateway & Admin Provisioning SaaS* yang dirancang khusus untuk industri F&B, hospitality, dan pariwisata di Bali (dengan pilot venue awal: **Sawana Coffee & Eatery** dan **Villa Lateng Ubud**).

Sistem ini memadukan:
1. **Perangkat Fisik Stand Meja:** Akrilik tatakan kayu A6 ber-chip NFC (NTAG213/215) + Dynamic QR Code.
2. **High-Performance Redirect Gateway (Go + Redis):** Menangani routing dinamis dengan latensi sub-10ms dan logging asinkron tanpa memblokir response.
3. **Dual-Tier Business Model:**
   - **Opsi 1 (Beli Putus / Lifetime Static):** Direct 302 Redirect langsung ke Google Maps Review.
   - **Opsi 2 (Smart SaaS):** Me-redirect ke micro-landing page berfitur *Smart Reputation Gate* (filter ulasan bintang 1–3 dialihkan ke WhatsApp manajer resto, bintang 4–5 ke Google Maps).
4. **Admin PWA & Web NFC Provisioner (Next.js 15):** Penulisan chip NFC fisik langsung dari browser mobile Google Chrome di Android menggunakan standar resmi **Web NFC API (`NDEFReader`)** dengan sekali tap.

---

## 🎨 2. BRANDING & UI/UX DESIGN SYSTEM SPECIFICATION

### A. Brand Identity
- **Nama Brand:** **ULASA** (Ulasa.id / Ulasa Bali)
- **Tagline:** *"One Tap. Five Stars."* / *"Ulasan Bintang 5 Sekali Tempel"*
- **Vibe & Mood:** Hangat, elegan, tropis, minimalis, dan terpercaya (khas Bali hospitality, Ubud, dan Canggu).

### B. Design Tokens (Tailwind CSS Configuration)
```javascript
// tailwind.config.ts color extensions
colors: {
  ulasa: {
    cream: '#FDFBF7',      // Background utama (Warm Off-White)
    surface: '#FFFFFF',    // Card background
    espresso: '#1F1A17',   // Text utama & headings (Deep Dark Roast)
    muted: '#78716C',      // Subtitle & borders (Warm Stone Gray)
    gold: '#C5A880',       // Accent primer, star active, NFC tap icon
    goldHover: '#B39368',
    forest: '#2D5A43',     // Secondary accent (Deep Tropical Green)
    forestLight: '#E8F0EC',
    danger: '#DC2626',
    success: '#16A34A',
  }
}
```

### C. Tipografi
- **Headings (Brand & Resto Name):** Serif hangat (`Playfair Display`, `Georgia`, atau `Merriweather`).
- **Body & UI Elements:** Clean modern sans-serif (`Inter` atau `Plus Jakarta Sans`).

---

### D. Spesifikasi UI/UX: Public Smart Gate (`/f/[code]`)
*Target: Pengunjung restoran/villa yang menempelkan smartphone di meja makan.*

* **Layout Container:** Max-width 420px, terpusat di tengah layar (*screen-centered*), padding 24px, background `ulasa-cream`.
* **Komponen Tampilan:**
  1. **Venue Header:**
     - Avatar/Logo bundar (diameter 64px) dengan border halus.
     - Nama Venue: misal *"Sawana Coffee & Eatery"* (Font serif, 20px, bold, `ulasa-espresso`).
     - Pertanyaan Ramah: *"Bagaimana pengalaman Anda hari ini?"* (Font sans, 14px, `ulasa-muted`).
  2. **Interactive 5-Star Rating Component:**
     - 5 Bintang SVG berukuran besar (masing-masing 44x44px untuk touch-target jempol yang nyaman).
     - Warna bintang default: `#E7E5E4` (Stone 200).
     - Hover/Selected: `#C5A880` (Ulasa Gold) dengan animasi getar lembut (*subtle spring/bounce*).
  3. **Behavior Rating 4 & 5 (Positive Flow):**
     - Seketika memicu animasi konfeti mini (*canvas-confetti*).
     - Menampilkan feedback visual sekejap: *"Terima kasih! Mengalihkan ke Google Review..."*
     - Auto-redirect ke link Google Review resmi merchant dalam 800ms.
  4. **Behavior Rating 1, 2, & 3 (Smart Reputation Filter Flow):**
     - Membuka form masukan internal yang santun dan empatik:
       - Header: *"Mohon maaf atas ketidaknyamanan Anda. Apa yang bisa kami perbaiki?"*
       - Textarea masukan masukan (placeholder: *"Ceritakan pengalaman Anda kepada manajer kami..."*).
       - Input no. WhatsApp opsional (placeholder: *"No. WhatsApp Anda (opsional untuk kami tindak lanjuti)"*).
       - Tombol Aksi: **"Kirim Masukan Langsung ke Manajer"** (`bg-ulasa-forest`, text putih).
       - Klik tombol akan membuat link `https://wa.me/{whatsapp_manager}?text=...` berisi teks keluhan yang sudah tersusun rapi, dan mencatat event ke database.
  5. **Footer Kepatuhan Regulasi Google (Mandatory):**
     - Teks kecil di bagian paling bawah:  
       `Ingin tetap menulis ulasan langsung di Google Maps? [Klik di sini]` (Link langsung ke Google Maps).

---

### E. Spesifikasi UI/UX: Admin PWA & NFC Provisioner (`/admin`)
*Target: Dewa saat melakukan setup dan penulisan stand NFC di lokasi kafe/villa menggunakan HP Android.*

* **Responsive Mobile PWA:** Header sticky dengan logo **ULASA**, toggle tab (Venues, Tags, Analytics).
* **Fitur Utama: "Quick Provisioning Card":**
  - Dropdown Venue: Pilih `Sawana Coffee & Eatery` atau `Villa Lateng Ubud`.
  - Input Label Meja: misal `Meja 05 - Indoor` atau `Resepsionis`.
  - Auto-generated Slug Code: misal `swn-05`.
  - **Pulsing NFC Action Button:**
    - Tombol besar dengan ikon gelombang NFC yang berdenyut (*pulse animation*).
    - Status teks: *"Dekatkan chip NFC ke belakang HP Anda, lalu tekan tombol di bawah"*.
    - Tombol: **[ 📳 TULIS & PAIRING KE CHIP ]**.
    - Integrasi Web NFC API (`new NDEFReader().write(...)`).
    - Feedback: Suara notifikasi sukses (*audio chime*), getaran haptic HP (*vibrate 100ms*), dan toast hijau *"Berhasil! Tag Meja 05 Siap Dipasang."*
* **Tabel Manajemen Tag:**
  - Menampilkan daftar meja, total tap, tier (Lifetime vs SaaS), switch toggle status *Smart Gate* (On/Off), dan tombol copy link.

---

## 🏛️ 3. ARSITEKTUR TEKNIS & TECH STACK

- **Backend API:** Go 1.22+ (Gin Web Framework), PostgreSQL driver (`pgx/v5`), Redis client (`go-redis/v9`).
- **Frontend App:** Next.js 15 (App Router), React 19, TypeScript, Tailwind CSS, Lucide React Icons.
- **Database & Cache:** PostgreSQL 16 (Relational persistence), Redis 7 (In-memory URL lookup & rate limiting).
- **Infrastruktur:** Multi-stage Dockerfile untuk Backend & Frontend, `docker-compose.yml` terintegrasi.

```
ulasa-gateway/
├── backend/
│   ├── cmd/server/main.go
│   ├── internal/
│   │   ├── config/config.go
│   │   ├── database/postgres.go
│   │   ├── database/redis.go
│   │   ├── handler/redirect_handler.go
│   │   ├── handler/admin_handler.go
│   │   ├── handler/feedback_handler.go
│   │   ├── middleware/cors.go
│   │   ├── model/entity.go
│   │   ├── repository/merchant_repo.go
│   │   ├── repository/tag_repo.go
│   │   └── service/redirect_service.go
│   ├── migrations/
│   │   └── 001_initial_schema.sql
│   ├── Dockerfile
│   └── go.mod
├── frontend/
│   ├── public/
│   │   └── sounds/chime.mp3
│   ├── src/
│   │   ├── app/
│   │   │   ├── admin/page.tsx               # Admin Dashboard & NFC Provisioner
│   │   │   ├── f/[code]/page.tsx            # Smart Reputation Gate Micro-Landing
│   │   │   ├── layout.tsx
│   │   │   └── globals.css
│   │   ├── components/
│   │   │   ├── NfcWriterCard.tsx            # Web NFC API Implementation
│   │   │   ├── StarRating.tsx               # Interactive 5-star with Confetti
│   │   │   └── FeedbackModal.tsx            # 1-3 star WhatsApp fallback
│   │   ├── lib/
│   │   │   └── api.ts
│   │   └── types/index.ts
│   ├── Dockerfile
│   └── package.json
└── docker-compose.yml
```

---

## 🗄️ 4. SKEMA DATABASE POSTGRESQL LENGKAP (`001_initial_schema.sql`)

```sql
-- Extension UUID
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. Merchants Table (Tempat Usaha)
CREATE TABLE merchants (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(150) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    category VARCHAR(50) NOT NULL DEFAULT 'fnb', -- 'fnb', 'villa', 'spa'
    google_place_id VARCHAR(150),
    direct_review_url TEXT NOT NULL,
    whatsapp_manager VARCHAR(30) NOT NULL,
    smart_filter_enabled BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. Subscriptions Table (Dual-Tier Lifecycle)
CREATE TABLE subscriptions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    merchant_id UUID REFERENCES merchants(id) ON DELETE CASCADE,
    tier VARCHAR(50) NOT NULL DEFAULT 'lifetime_static', -- 'lifetime_static' | 'smart_saas'
    status VARCHAR(30) NOT NULL DEFAULT 'active',        -- 'trial' | 'active' | 'suspended'
    trial_ends_at TIMESTAMPTZ,
    current_period_end TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. NFC Tags Table (Stand Fisik per Meja)
CREATE TABLE nfc_tags (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    merchant_id UUID REFERENCES merchants(id) ON DELETE CASCADE,
    tag_uid VARCHAR(100) UNIQUE,
    table_label VARCHAR(50) NOT NULL,
    slug_code VARCHAR(50) UNIQUE NOT NULL, -- Di-encode ke NFC: https://tap.ulasa.id/t/swn-01
    is_active BOOLEAN DEFAULT TRUE,
    total_taps INT DEFAULT 0,
    last_tapped_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX idx_nfc_tags_slug ON nfc_tags(slug_code);

-- 4. Tap Events Table (Analytics & Feedback Log)
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

-- SEED DATA AWAL: Bisnis Milik Dewa Biara
INSERT INTO merchants (id, name, slug, category, direct_review_url, whatsapp_manager, smart_filter_enabled)
VALUES 
(
    'a0000000-0000-0000-0000-000000000001',
    'Sawana Coffee & Eatery',
    'sawana-coffee',
    'fnb',
    'https://search.google.com/local/writereview?placeid=ChIJN1t_tDeuEmsRUsoyG83frY4',
    '6281239718505',
    TRUE
),
(
    'a0000000-0000-0000-0000-000000000002',
    'Villa Lateng Ubud',
    'villa-lateng',
    'villa',
    'https://search.google.com/local/writereview?placeid=ChIJb2u_tDeuEmsRUsoyG83frY5',
    '6281239718505',
    TRUE
);

INSERT INTO subscriptions (merchant_id, tier, status)
VALUES 
('a0000000-0000-0000-0000-000000000001', 'smart_saas', 'active'),
('a0000000-0000-0000-0000-000000000002', 'smart_saas', 'active');

INSERT INTO nfc_tags (merchant_id, table_label, slug_code)
VALUES 
('a0000000-0000-0000-0000-000000000001', 'Meja 01 (Indoor)', 'swn-01'),
('a0000000-0000-0000-0000-000000000001', 'Meja 02 (Garden)', 'swn-02'),
('a0000000-0000-0000-0000-000000000002', 'Resepsionis Villa', 'ltg-rec');
```

---

## 💻 5. IMPLEMENTASI FITUR KUNCI

### A. Core Redirect Handler (`GET /t/:slug_code` di Go)
```go
func (h *RedirectHandler) HandleTap(c *gin.Context) {
    slug := c.Param("slug_code")
    ctx := c.Request.Context()

    // 1. Cek Cache Redis (Sub-5ms)
    tagData, err := h.cache.GetTagMetadata(ctx, slug)
    if err != nil {
        // Fallback DB Query
        tagData, err = h.repo.FindTagBySlug(ctx, slug)
        if err != nil {
            c.JSON(http.StatusNotFound, gin.H{"error": "Tag tidak terdaftar"})
            return
        }
        _ = h.cache.SetTagMetadata(ctx, slug, tagData, 10*time.Minute)
    }

    // 2. Non-blocking Asynchronous Tap Logging via Goroutine
    go h.logTapEvent(tagData.ID, c.Request.UserAgent())

    // 3. Dual-Tier Branching Logic
    if tagData.Tier == "lifetime_static" || !tagData.SmartFilterEnabled {
        // Opsi 1 (Beli Putus): Direct 302 Redirect ke Google Maps
        c.Redirect(http.StatusFound, tagData.DirectReviewURL)
        return
    }

    // Opsi 2 (Smart SaaS): Redirect ke Micro-Landing Page Smart Gate
    frontendURL := fmt.Sprintf("%s/f/%s", h.cfg.FrontendBaseURL, slug)
    c.Redirect(http.StatusFound, frontendURL)
}
```

### B. Web NFC API Implementation di Next.js PWA (`NfcWriterCard.tsx`)
```typescript
'use client';
import { useState } from 'react';

export default function NfcWriterCard({ targetUrl, tableLabel }: { targetUrl: string; tableLabel: string }) {
  const [status, setStatus] = useState<'idle' | 'scanning' | 'success' | 'error'>('idle');
  const [errorMessage, setErrorMessage] = useState('');

  const handleWriteNfc = async () => {
    if (!('NDEFReader' in window)) {
      setStatus('error');
      setErrorMessage('Web NFC API tidak didukung browser ini. Buka via Google Chrome di HP Android.');
      return;
    }

    try {
      setStatus('scanning');
      const ndef = new (window as any).NDEFReader();
      
      // Tulis URL ke chip fisik
      await ndef.write({
        records: [{ recordType: 'url', data: targetUrl }]
      });

      setStatus('success');
      // Trigger haptic vibration & sound
      if (navigator.vibrate) navigator.vibrate(100);
    } catch (err: any) {
      setStatus('error');
      setErrorMessage(err.message || 'Gagal menulis ke chip NFC.');
    }
  };

  return (
    <div className="bg-ulasa-surface p-6 rounded-2xl shadow-sm border border-stone-200 text-center">
      <h3 className="font-serif text-lg font-bold text-ulasa-espresso mb-1">Pairing Stand: {tableLabel}</h3>
      <p className="text-xs text-ulasa-muted mb-4 font-mono break-all">{targetUrl}</p>

      {status === 'scanning' && (
        <div className="my-4 animate-pulse flex flex-col items-center">
          <div className="w-16 h-16 rounded-full bg-ulasa-gold/20 flex items-center justify-center text-ulasa-gold text-2xl">
            📳
          </div>
          <span className="text-sm font-medium text-ulasa-espresso mt-2">Tempelkan chip NFC ke bodi HP...</span>
        </div>
      )}

      {status === 'success' && (
        <div className="my-4 p-3 bg-emerald-50 text-emerald-800 rounded-xl text-sm font-medium">
          ✅ Chip Berhasil Ditulis & Terhubung ke Database!
        </div>
      )}

      {status === 'error' && (
        <div className="my-4 p-3 bg-rose-50 text-rose-800 rounded-xl text-xs">
          ⚠️ {errorMessage}
        </div>
      )}

      <button
        onClick={handleWriteNfc}
        className="w-full py-3 px-4 bg-ulasa-espresso hover:bg-black text-white font-medium rounded-xl transition duration-150 shadow-sm"
      >
        {status === 'scanning' ? 'Mendengarkan NFC...' : '📳 Tulis & Pairing Tag Meja'}
      </button>
    </div>
  );
}
```

---

## 📋 6. PROMPT SIAP TEMPEL UNTUK CLAUDE CODE CLI

Salin seluruh teks dalam kotak di bawah ini dan langsung jalankan di terminal Claude Code:

```text
Bangunkan repositori penuh bernama `ulasa-gateway` (sistem SaaS brand "ULASA: One Tap. Five Stars." untuk smart review restoran dan villa di Bali) berdasarkan arsitektur berikut:

1. Backend (Go 1.22+ Gin, PostgreSQL, Redis, Docker):
   - Endpoint `GET /t/:slug_code`: redirect latensi rendah (<10ms). Jika tier `lifetime_static` -> 302 langsung ke Google Maps review. Jika tier `smart_saas` -> 302 ke frontend smart gate `/f/:slug_code`.
   - Logging tap asinkron via goroutine ke tabel `tap_events` (mencatat OS, user-agent, timestamp).
   - CRUD API untuk Merchant dan NFC Tag di `/api/v1/merchants` dan `/api/v1/tags`.
   - Endpoint `/api/v1/feedback` untuk menampung masukan ulasan bintang 1-3.

2. Frontend (Next.js 15 App Router, Tailwind CSS, TypeScript):
   - Halaman Smart Gate `/f/[code]`: UI micro-page bergaya Bali luxury minimalis (palet Warm Cream #FDFBF7, Espresso #1F1A17, Gold #C5A880). Tampilkan nama resto dan 5 bintang rating besar. Rating 4-5 memicu efek konfeti lalu redirect ke Google Maps. Rating 1-3 memunculkan formulir masukan santun dengan tombol kirim ke WhatsApp manajer. Sertakan link kepatuhan Google di footer.
   - Halaman Admin PWA `/admin`: dashboard pengelolaan venue, daftar meja, dan komponen `NfcWriterCard` yang mengimplementasikan browser Web NFC API (`NDEFReader`) untuk pairing dan penulisan chip NFC langsung dari HP Android.

3. Konfigurasi & Data:
   - Skema migrasi PostgreSQL lengkap dengan seed data Sawana Coffee & Eatery dan Villa Lateng Ubud.
   - `docker-compose.yml` terkonfigurasi untuk menjalankan Backend, Frontend, Postgres, dan Redis.
   - Unit test untuk router dan redirect service.
```
