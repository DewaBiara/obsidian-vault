# 📱 Arsitektur Aplikasi Admin & NFC Tag Provisioning (Smart Review SaaS)

- **Dokumen:** Rancang Bangun Sistem Admin, Provisioning NFC, & Manajemen Langganan
- **Inisiator:** [[Dewa Biara]]
- **Tanggal:** 2026-09-24
- **Status:** Perencanaan Arsitektur
- **Tautan Terkait:** [[01_Projects/Deep_Analysis_NFC_Review_SaaS_Bali]] | [[01_Projects/Bahan_dan_Setup_Hardware_NFC]]

---

## 🎯 1. Mengapa Ide Ini Sangat Tepat?

Menggantungkan proses penulisan tag ke aplikasi pihak ketiga (*NFC Tools*) memiliki kelemahan fatal saat skala bisnis membesar:
1. **Rawan Human-Error:** Rentan salah ketik slug/URL saat menulis puluhan tag meja.
2. **Tidak Terintegrasi ke Database:** Tidak ada pencatatan serial number (UID chip NFC) ke meja mana tag tersebut dipasang.
3. **Lambat:** Harus copy-paste manual satu per satu.

Dengan membuat **Aplikasi Admin Terpusat**:
* Tag langsung di-pairing ke database merchant dalam 1 detik.
* Manajemen langganan (*subscription billing & trial*) terpantau otomatis.
* Merchant bisa mengganti target link dan konfigurasi ulasan secara dinamis kapan saja.

---

## 💡 2. Fitur Kunci: Web NFC API (Tanpa Perlu Bikin Native App!)

Sebagai web/backend developer, kamu **tidak perlu membuat aplikasi mobile Android/iOS native dari nol** hanya untuk fitur write NFC.
Browser modern (Google Chrome di Android) sudah memiliki standar resmi **Web NFC API** (`NDEFReader`):
```javascript
// Contoh One-Click Write di Web Admin PWA (Chrome Android):
async function provisionTag(venueSlug, tableNumber) {
  if ('NDEFReader' in window) {
    const ndef = new NDEFReader();
    await ndef.write({
      records: [{
        recordType: "url",
        data: `https://tap.bali.id/r/${venueSlug}?tbl=${tableNumber}`
      }]
    });
    alert(`Tag Meja ${tableNumber} Berhasil Ditulis!`);
  }
}
```
**Keuntungan:** Web Admin berbentuk **PWA (Progressive Web App)** bisa dibuka di laptop maupun HP Android, langsung siap tap dan tulis!

---

## 🏛️ 3. Modul Utama Aplikasi Admin

### Modul A: Provisioning & Hardware Management (Internal Dewa/Admin)
1. **Form Provisioning Cepat:**
   - Pilih Merchant: `Sawana Coffee & Eatery`
   - Input Nomor Meja: `Meja 01`
   - Klik tombol **"Write & Pair Tag"** -> Tempelkan stiker NFC ke HP -> Chip otomatis terisi URL unik dan tercatat di database dengan status `active`.
2. **UID Tag Lock / Protection:**
   - Opsi mengunci (*read-only*) tag agar tidak bisa ditimpa/di-hack oleh pengunjung iseng.

### Modul B: Merchant & Subscription Engine
1. **Merchant Profile:**
   - Nama bisnis, alamat, koordinat, kontak manajer, WhatsApp alert.
2. **Subscription Lifecycle Management:**
   - Status: `Trial (14 hari)`, `Active (Paid)`, `Past Due`, `Suspended`.
   - Periode billing (Bulanan / Tahunan).
   - Auto-suspension: Jika langganan habis, redirect gateway otomatis menampilkan halaman notifikasi atau fallback ke menu digital biasa.

### Modul C: Dynamic Routing & Review Policy Control
1. **Destination Target:**
   - Google Maps Review URL (Place ID).
   - Alternatif: Instagram profil, WiFi portal, TripAdvisor, atau katalog menu.
2. **Smart Reputation Gate Toggle:**
   - `[ON/OFF]` Filter Bintang 1-3.
   - Kustomisasi pesan ramah pada halaman mikro feedback.
   - Nomor WhatsApp tujuan komplain privat.

### Modul D: Real-Time Analytics & Reporting
- Grafik jumlah tap harian & jam-jam sibuk.
- Heatmap meja teramai (misal: Meja 4 & Meja 7 paling sering tap review).
- Total ulasan tersaring vs lolos ke Google Maps.

---

## 🗄️ 4. Skema Database Relasional (PostgreSQL)

```sql
-- 1. Tabel Merchant / Venue
CREATE TABLE merchants (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(150) NOT NULL, -- Contoh: "Sawana Coffee & Eatery"
    slug VARCHAR(100) UNIQUE NOT NULL, -- "sawana-coffee"
    category VARCHAR(50) NOT NULL, -- "fnb" / "villa" / "spa"
    google_place_id VARCHAR(150),
    direct_review_url TEXT NOT NULL,
    whatsapp_manager VARCHAR(30),
    smart_filter_enabled BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. Tabel Langganan (Subscriptions)
CREATE TABLE subscriptions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    merchant_id UUID REFERENCES merchants(id) ON DELETE CASCADE,
    plan_tier VARCHAR(50) DEFAULT 'pro', -- starter / pro / enterprise
    status VARCHAR(30) DEFAULT 'trial', -- trial, active, past_due, canceled
    trial_ends_at TIMESTAMPTZ,
    current_period_end TIMESTAMPTZ NOT NULL,
    price_cents INT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. Tabel Stand Fisik / NFC Tags
CREATE TABLE nfc_tags (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    merchant_id UUID REFERENCES merchants(id) ON DELETE CASCADE,
    tag_uid VARCHAR(100) UNIQUE, -- Serial number dari chip NFC (opsional)
    table_label VARCHAR(50) NOT NULL, -- "Meja 05" / "Resepsionis"
    slug_code VARCHAR(50) UNIQUE NOT NULL, -- "swn-05" -> url: tap.id/t/swn-05
    is_active BOOLEAN DEFAULT TRUE,
    total_taps INT DEFAULT 0,
    last_tapped_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 4. Tabel Event Logs (Analitik Tap)
CREATE TABLE tap_events (
    id BIGSERIAL PRIMARY KEY,
    tag_id UUID REFERENCES nfc_tags(id) ON DELETE CASCADE,
    ip_hash VARCHAR(64),
    user_agent TEXT,
    device_os VARCHAR(30), -- iOS / Android
    rating_given INT, -- Null jika langsung redirect, 1-5 jika via gate
    action_taken VARCHAR(50), -- "redirect_google", "private_complaint"
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX idx_tap_events_tag_created ON tap_events(tag_id, created_at DESC);
```

---

## 🚀 5. Roadmap Pengembangan MVP

1. **Sprint 1 (Backend Core - Go):**
   - API CRUD Merchant & NFC Tag.
   - Endpoint redirect ultra-cepat (<10ms) dengan Redis caching.
2. **Sprint 2 (Frontend Admin & Provisioning - Next.js / React PWA):**
   - Halaman login & dashboard analitik sederhana.
   - Fitur **"Write NFC Tag"** menggunakan browser Web NFC API langsung dari smartphone admin.
3. **Sprint 3 (Pilot Testing):**
   - Pasang tag hasil provisioning aplikasi di Sawana Coffee & Villa Lateng Ubud.
