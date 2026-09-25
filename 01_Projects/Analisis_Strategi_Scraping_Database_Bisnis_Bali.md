# 🗺️ Analisis & Strategi Ekstraksi Database Bisnis Bali (Google Maps)

- **Inisiator:** [[Dewa Biara]]
- **Brand:** ULASA (*One Tap. Five Stars.*)
- **Tujuan:** Mengumpulkan data seluruh bisnis F&B, hospitality, dan pariwisata di Bali per kabupaten & kecamatan untuk pipeline prospek B2B.
- **Tautan Terkait:** [[01_Projects/Deep_Analysis_NFC_Review_SaaS_Bali]] | [[01_Projects/CLAUDE_CODE_HANDOVER_ULASA]]

---

## 🎯 1. Evaluasi Strategis: Mengapa Ide Ini Sangat Brilian?

Membangun database prospek mandiri adalah **senjata penjualan paling mematikan (*unfair sales engine*)**:
1. **Total Addressable Market (TAM) yang Terpetakan:** Kamu memiliki daftar nama tempat, alamat, nomor telepon/WhatsApp bisnis, kategori, dan koordinat GPS di seluruh Bali.
2. **Lead Scoring Otomatis (Menemukan Prospek Paling Butuh ULASA):**
   - **Tier 1 (Prospek Paling Panas):** Tempat dengan **Rating 3.8 – 4.3 dan ulasan 30–200**. Tempat-tempat ini sangat khawatir rating mereka turun ke bawah 4.0 dan sangat butuh fitur *Smart Reputation Gate* ULASA untuk mencegah ulasan bintang 1 baru.
   - **Tier 2 (Bisnis Baru):** Tempat dengan ulasan **< 30 ulasan**. Mereka butuh stand ULASA untuk *kickstart* ulasan bintang 5 dengan cepat.
   - **Tier 3 (Viral/High Volume):** Tempat dengan ulasan **> 1.000 ulasan** (Beach club, resto legendaris). Target penjualan Stand Khusus Meja Kasir dalam jumlah banyak.
3. **Hyper-Localized Sales Route:** Sales door-to-door atau penawaran WhatsApp bisa dikelompokkan per jalan (misal: sepanjang Jl. Pantai Batu Bolong Canggu atau Jl. Hanoman Ubud).

---

## ⚖️ 2. Perbandingan 4 Metode Ekstraksi Data dari Google Maps

| Metode | Biaya | Kecepatan | Risiko Blokir / CAPTCHA | Kelengkapan Data | Rekomendasi |
|---|---|---|---|---|---|
| **1. Google Places API Resmi** | Sangat Mahal (~$35–$50 per 1.000 request) | Cepat & Stabil | 0% (Resmi) | Lengkap | ❌ Tidak Efisien untuk Bootstrapping (bisa habis Rp 10–15 jt untuk 20k tempat). |
| **2. Scraper Python Mandiri (Selenium / Playwright)** | Gratis (Hanya bayar proxy) | Lambat | Sangat Tinggi (Google Maps menerapkan anti-bot agresif, infinite-scroll, canvas) | Sering Gagal di Tengah Jalan | ⚠️ Terlalu membuang waktu maintenance script anti-bot. |
| **3. Managed Scraper (Outscraper / Apify) — *PILIHAN TERBAIK*** | **Sangat Murah (~$2–$3 per 1.000 data)** | Sangat Cepat | 0% (Platform yang mengurus IP rotasi & captcha) | Sangat Lengkap (Nama, Alamat, Phone, Rating, Reviews, Place ID, Web, IG) | ✅ **SANGAT DIREKOMENDASIKAN** (~Rp 300rb sudah dapat 10.000 data bersih). |
| **4. OpenStreetMap (Overpass API)** | Gratis 100% | Sangat Cepat | 0% | Hanya nama, koordinat, dan telepon (Tanpa data rating/ulasan Google) | Opsi komplementer gratis. |

---

## 📍 3. Peta Prioritas Wilayah Ekstraksi (Fokus Fase 1)

Jangan langsung menyedot seluruh pulau Bali (wilayah seperti Jembrana, Tabanan barat, atau Bangli memiliki densitas turis yang rendah). 

Fokuskan pada **3 Zona Emas (Golden Triangle Bali)**:

### Ring 1: Kawasan Konsentrasi F&B Tertinggi (Badung & Gianyar)
1. **Badung - Kuta Utara:** Canggu, Tibubeneng, Pererenan, Kerobokan.
2. **Gianyar - Ubud:** Ubud Central, Sayan, Kedewatan, Tegallalang, Penestanan.
3. **Badung - Kuta Selatan:** Seminyak, Jimbaran, Uluwatu, Bingin, Nusa Dua.
4. **Denpasar - Denpasar Selatan:** Sanur (kawasan ekspat & wisatawan Eropa).

### Filter Kategori Bisnis yang Wajib Ditarik:
- `restaurant`, `cafe`, `coffee_shop`, `bar`, `beach_club`
- `villa`, `hotel`, `resort`, `guest_house`
- `spa`, `massage`, `yoga_studio`, `beauty_salon`

---

## 🗄️ 4. Rancangan Skema Database Prospek (`prospect_venues`)

Data hasil ekstraksi disimpan ke dalam database PostgreSQL ULASA:

```sql
CREATE TABLE prospect_venues (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(200) NOT NULL,
    category VARCHAR(50) NOT NULL, -- fnb, villa, spa
    regency VARCHAR(50) NOT NULL,  -- Badung, Gianyar, Denpasar
    district VARCHAR(50) NOT NULL, -- Kuta Utara, Ubud, Sanur
    address TEXT,
    phone_number VARCHAR(30),
    whatsapp_number VARCHAR(30),
    google_place_id VARCHAR(150) UNIQUE,
    google_maps_url TEXT,
    rating NUMERIC(2,1),          -- Contoh: 4.2
    reviews_count INT,            -- Contoh: 145
    lead_score VARCHAR(10),       -- 'HOT', 'WARM', 'COLD'
    outreach_status VARCHAR(30) DEFAULT 'uncontacted', -- 'uncontacted', 'wa_sent', 'visited', 'trial_active', 'closed_won'
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX idx_prospect_location ON prospect_venues(regency, district);
CREATE INDEX idx_prospect_rating ON prospect_venues(rating, reviews_count);
```

---

## ⚖️ 5. Aspek Kepatuhan Hukum & Privasi

1. **Informasi Direktori Publik:**
   - Data profil bisnis di Google Maps (nama resto, alamat, jam buka, nomor telepon toko) adalah informasi direktori komersial publik. Pengumpulannya untuk riset pasar B2B adalah sah secara hukum (tidak melanggar UU Pelindungan Data Pribadi selama tidak mengikis identitas pribadi individu/karyawan).
2. **Etika Pendekatan (Anti-Spam Outreach):**
   - Jangan gunakan nomor WhatsApp ini untuk broadcast blast robotik.
   - Gunakan pendekatan personal yang bernilai:  
     *"Halo tim [Nama Kafe], saya Dewa dari ULASA Bali. Kami melihat [Nama Kafe] di Canggu ulasannya sudah 180+ dengan rating bagus 4.3. Kami ingin menawarkan uji coba stand meja proteksi ulasan bintang 5 gratis selama 14 hari..."*

---

## 🚀 6. Rekomendasi Langkah Selanjutnya
1. Gunakan platform managed scraper seperti **Outscraper** (bisa login dengan akun Google, tersedia kuota gratis 500 data awal).
2. Lakukan uji coba penarikan data pertama untuk 1 kecamatan: **Kuta Utara (Canggu)** dengan kata kunci: *"cafe in Canggu Bali"* dan *"restaurant in Canggu Bali"*.
3. Impor hasilnya ke spreadsheet atau database untuk kita lakukan *lead scoring*.
