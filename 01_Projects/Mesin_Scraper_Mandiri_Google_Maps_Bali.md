# ⚡ ULASA Bali Google Maps Lead Collector (Mesin Scraper Mandiri)

- **Inisiator:** [[Dewa Biara]]
- **Tujuan:** Mengumpulkan data seluruh bisnis di Bali tanpa biaya langganan scraper pihak ketiga ($0 biaya).
- **Lokasi Script:** `/workspace/scripts/bali_gmaps_collector.py`
- **Output Hasil:** `/workspace/ubud_custom_collector_results.csv`
- **Tautan Terkait:** [[01_Projects/Pilot_Data_Scraping_Ubud_Google_Maps]] | [[01_Projects/Analisis_Strategi_Scraping_Database_Bisnis_Bali]]

---

## 💡 1. Mengapa Apify Memberikan Sedikit Data?
Pada Apify, setiap crawl meluncurkan *headless browser* Chromium berat yang memakan Compute Units (CUs) mahal, dan dibatasi 100 tempat per pencarian. Akibatnya saldo $5 habis hanya untuk ~110 tempat.

---

## 🛠️ 2. Arsitektur Mesin Scraper Mandiri Kita (Direct HTTP Reverse-Engineered)

Kita membangun script Python mandiri (`bali_gmaps_collector.py`) yang beroperasi dengan teknik:
1. **Direct Internal RPC GET:** Melakukan request langsung ke endpoint internal RPC Google Maps (`/search?tbm=map...`) via HTTP standar tanpa membuka Chromium/Selenium sama sekali.
2. **Speed & Efficiency:** 
   - 1 query hanya butuh **~1,2 detik**.
   - Bebas biaya API ($0.00).
   - Mengambil data: Nama Tempat, Kategori, Rating Bintang, Jumlah Ulasan, Google Place ID, Alamat Lengkap, dan URL Google Maps.
3. **Sub-Corridor Multi-Grid Scanning:**
   - Karena Google Maps membatasi maksimal 20–100 hasil per tampilan satu kata kunci, kita memecah wilayah per jalan/koridor utama (contoh Ubud: Jl. Hanoman, Jl. Raya Ubud, Monkey Forest, Penestanan, Sayan, Tegallalang).
   - 11 query pencarian koridor jalanan Ubud berhasil mengumpulkan **183 tempat usaha unik dalam 15 detik**!
4. **Lead Scoring Terintegrasi:**
   - Otomatis mengelompokkan ke: `TIER_HOT`, `TIER_VOLUME`, `TIER_NEW`, dan `TIER_GROWTH`.

---

## 🚀 3. Perluasan ke Seluruh Bali (Full Coverage)
Dengan skrip mandiri ini, kita bisa menambahkan daftar query untuk seluruh kecamatan di Bali:
- **Canggu:** Jl. Pantai Batu Bolong, Jl. Pantai Berawa, Jl. Nelayan, Jl. Echo Beach, Pererenan.
- **Seminyak & Kuta:** Jl. Kayu Aya (Oberoi), Jl. Petitenget, Jl. Raya Seminyak, Sunset Road.
- **Uluwatu & Jimbaran:** Jl. Labuansait, Bingin, Padang Padang, Balangan.
- **Sanur:** Jl. Danau Tamblingan, Jl. Cemara.

Estimasi: **5.000 – 10.000 tempat usaha se-Bali** bisa kita kumpulkan dalam hitungan menit secara gratis 100%!
