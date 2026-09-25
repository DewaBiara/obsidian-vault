# 📍 Pilot Project: Ekstraksi Data Bisnis Ubud via Outscraper & Apify

- **Inisiator:** [[Dewa Biara]]
- **Wilayah Uji Coba:** Ubud, Gianyar, Bali
- **Tujuan:** Menarik data seluruh kafe, restoran, villa, dan spa di Ubud untuk validasi pipeline penjualan B2B ULASA.
- **Tautan Terkait:** [[01_Projects/Analisis_Strategi_Scraping_Database_Bisnis_Bali]] | [[02_Areas/Villa_Lateng_Ubud]]

---

## 🎯 1. Mengapa Memulai dari Ubud adalah Keputusan Terbaik?

1. **Home Ground Advantage:** Dewa Biara mengoperasikan **Villa Lateng Ubud** dan memahami peta jalanan Ubud secara langsung (Jl. Monkey Forest, Jl. Hanoman, Jl. Gootama, Jl. Raya Sanggingan, Penestanan, Sayan).
2. **Karakteristik Pasar Ubud:** 
   - Sangat didominasi wisatawan mancanegara (bule Australia, Eropa, Amerika) yang **95% memilih tempat makan & villa berdasarkan ulasan Google Maps**.
   - Banyak pemilik kafe/resto independen dan ekspat yang sangat peduli pada reputasi online.
3. **Volume Terukur (Size):** Diperkirakan terdapat sekitar **1.500 – 2.500 bisnis pariwisata aktif di Ubud**. Ukuran data ini pas untuk kuota uji coba (free tier / biaya < $5) tanpa membebani storage.

---

## ⚖️ 2. Perbandingan: Outscraper vs Apify untuk Ubud

| Fitur | Outscraper (`outscraper.com`) | Apify (`apify.com`) |
|---|---|---|
| **Kemudahan Pemakaian** | ⭐⭐⭐⭐⭐ Sangat simpel (Tinggal ketik query di browser) | ⭐⭐⭐⭐ Butuh pilih "Actor" (Google Maps Scraper) |
| **Free Tier Awal** | 500 records gratis | $5 kredit gratis per bulan (~2.000–2.500 records) |
| **Ekstraksi Kontak Tambahan** | Nomor telepon Google Maps, website | Nomor telepon + **Instagram, FB, & Email** yang di-crawl dari website bisnis |
| **Kecepatan** | ~3–5 menit untuk 1.000 data | ~5–10 menit |
| **Rekomendasi Pemakaian** | **Paling cepat & praktis untuk langsung download CSV.** | **Paling kaya data jika ingin menyasar akun Instagram tempat usaha.** |

---

## 📋 3. Rencana Kata Kunci (Search Queries) untuk Ubud

Untuk mendapatkan hasil yang komprehensif tanpa duplikasi berlebih:

### Batch 1: F&B (Kafe, Restoran, Bar)
- `cafe in Ubud Bali`
- `specialty coffee Ubud Bali`
- `restaurant in Ubud Bali`
- `vegan vegetarian restaurant Ubud Bali`
- `bar lounge Ubud Bali`

### Batch 2: Hospitality (Villa, Resort, Hotel)
- `villa in Ubud Bali`
- `boutique hotel Ubud Bali`
- `resort Ubud Bali`
- `guest house Ubud Bali`

### Batch 3: Wellness (Spa, Massage, Yoga)
- `spa in Ubud Bali`
- `massage center Ubud Bali`
- `yoga studio Ubud Bali`

---

## 🚀 4. Langkah Praktis Menjalankannya (Step-by-Step)

### Opsi A: Menggunakan Outscraper (Tanpa Koding, 3 Menit Jadi)
1. Buka `https://outscraper.com` dan daftar dengan akun Google (dapat gratis 500 data).
2. Pilih layanan: **Google Maps Data Scraper**.
3. Pada kolom **Queries**, masukkan:
   ```text
   cafe in Ubud Bali
   restaurant in Ubud Bali
   villa in Ubud Bali
   spa in Ubud Bali
   ```
4. Di bagian **Location**, isi: `Ubud, Gianyar, Bali, Indonesia`.
5. Set limit per query: `150` atau `200` agar tetap masuk kuota gratis.
6. Klik **Get Data** -> Tunggu 3 menit -> Unduh file **CSV / Excel**.

---

## 🧹 5. Skrip Pemrosesan Data & Lead Scoring (Python)

Setelah file CSV dari Outscraper/Apify diunduh, kita gunakan skrip otomasi untuk:
1. Normalisasi nomor telepon ke format WhatsApp internasional (`+628...`).
2. Menghitung **Lead Score**:
   - **HOT LEADS:** Rating `3.8 – 4.3` dengan `30 – 300 ulasan` (Sangat butuh proteksi ulasan buruk).
   - **NEW VENUES:** Ulasan `< 20` (Butuh percepatan ulasan bintang 5).
   - **HIGH VOLUME:** Ulasan `> 500` (Target stand kasir).
3. Mengelompokkan prospek berdasarkan nama jalan (Jl. Hanoman, Jl. Monkey Forest, Jl. Raya Ubud, dll).
