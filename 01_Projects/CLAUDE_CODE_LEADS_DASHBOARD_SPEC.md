# 📋 Claude Code Prompt & Spesifikasi: ULASA Bali Leads Intelligence Web App

Gunakan spesifikasi ini langsung sebagai instruksi utama saat menjalankan **Claude Code CLI**:

---

## 🎯 Goal
Bangun aplikasi web dashboard interaktif yang modern, responsif, dan elegan untuk menampilkan database prospek bisnis Bali (798 tempat usaha di Ubud, Canggu, dan Seminyak) untuk produk **ULASA** (*Smart NFC Review & Reputation SaaS*).

---

## 📁 Sumber Data
- File data master tersedia di: `bali_master_leads_798.csv` (atau `bali_master_leads.json`).
- Struktur kolom:
  - `name`: Nama tempat usaha (contoh: *Clear Cafe*, *Finns Beach Club*, *La Favela*).
  - `region`: Wilayah (*Ubud*, *Canggu*, *Seminyak*).
  - `category`: Kategori (*Kafe*, *Restoran*, *Vila*, *Spa*, *Bar*).
  - `rating`: Rating Google Maps (contoh: *4.3*, *4.7*).
  - `reviews`: Jumlah ulasan (contoh: *4563*, *24629*).
  - `lead_tier`: Segmentasi prospek:
    - `TIER_HOT`: Rating 3.8 – 4.4 (Sangat butuh filter Smart Gate).
    - `TIER_VOLUME`: Reviews > 500 (Target Stand Kasir A5).
    - `TIER_NEW`: Reviews < 30 (Butuh percepatan ulasan bintang 5 pertama).
    - `TIER_GROWTH`: Rating solid ulasan 30–500.
  - `phone`: Nomor WhatsApp/telepon internasional (`+628...`).
  - `address`: Alamat lengkap di Bali.
  - `place_id`: Google Maps Place ID unik.
  - `gmaps_url`: URL langsung ke Google Maps.
  - `reason`: Alasan / justification lead scoring.

---

## 🎨 Design System & Estetika (Brand ULASA)
- **Tema:** Dark mode modern bernuansa *Bali Luxury Hospitality*.
- **Palet Warna:**
  - Background: `#0F0F11` (Deep Charcoal) & Card: `#18181B`.
  - Accent / Brand: `#C5A880` (Warm Gold).
  - Success / Volume: `#2D5A43` / `#10B981` (Forest Green).
  - Warning / Hot: `#F59E0B` (Amber).
  - Border: `#27272A`.
- **Tipografi:** Sans-serif modern (Plus Jakarta Sans / Inter) untuk body, dan Serif elegan (Playfair Display) untuk judul/angka KPI.

---

## ⚡ Fitur Utama yang Harus Dibangun:
1. **Executive KPI Cards:**
   - Total Leads (798)
   - Hot Leads Count (48)
   - Volume Titans Count (198)
   - New Stays & Dining Count (359)
2. **Filter & Search Real-Time:**
   - Filter Tab: All, Ubud, Canggu, Seminyak.
   - Filter Tier: All, Hot Leads, Volume Titans, New Venues.
   - Fuzzy Search: Search bar instan berdasarkan nama venue, jalan, atau kategori.
3. **Dual View Modes:**
   - **Grid Card View:** Kartu visual elegan dengan rating stars, alamat, dan tombol CTA.
   - **Table View:** Tabel data dengan fitur sorting berdasarkan rating atau jumlah ulasan.
4. **Personalized WhatsApp Pitch Generator (Modal):**
   - Setiap kartu memiliki tombol *"💡 Pitch Script"*.
   - Saat diklik, modal menampilkan draf teks WhatsApp yang terisi otomatis dengan nama kafe, wilayah, rating, dan ulasan mereka saat ini, lengkap dengan tombol *"Copy Script"* dan tombol langsung chat *"💬 Open WhatsApp"*.
5. **Direct Actions:**
   - Direct link ke Google Maps (`gmaps_url`).
   - Direct link ke WhatsApp (`https://wa.me/<phone>`).
