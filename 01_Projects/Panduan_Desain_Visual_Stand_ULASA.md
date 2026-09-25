# 🎨 Panduan Desain Visual & Cara Pembuatan Stand ULASA

- **Inisiator:** [[Dewa Biara]]
- **Brand:** ULASA (*One Tap. Five Stars.*)
- **Tujuan:** Panduan cetak dan perakitan fisik untuk Stand Meja Makan (A6) dan Stand Kasir (A5/L-Shape).
- **Tautan Terkait:** [[01_Projects/Spesifikasi_Model_Prototype_dan_Stand_Kasir]] | [[01_Projects/Branding_dan_Design_System_UI_UX]]

---

## 📐 1. Tata Letak (Layout Hierarchy) Kertas Insert

### Diagram Anatomi Visual Stand A6 (105 x 148 mm):
```
+-----------------------------------------------------------+
|                                                           |  <- Margin atas: 15mm
|                 [ LOGO SAWANA / RESTO ]                   |  <- Lebar logo: 35-40mm (Center)
|                                                           |
|                   Enjoyed Your Time?                      |  <- Font Serif (Playfair Display / Georgia), 16pt
|                Bagikan Pengalaman Anda                    |  <- Font Sans (Inter / Plus Jakarta Sans), 10pt
|                                                           |
|                         ╭─────╮                           |
|                         │ 📳  │                           |  <- LINGKARAN TARGET TAP
|                         │ TAP │                           |     Diameter: 40mm
|                         ╰─────╯                           |     Warna aksen: Warm Gold / Forest Green
|                                                           |     (Chip NFC NTAG213 ditempel persis di belakang ini)
|                     TAP PHONE HERE                        |  <- All-caps, Bold, Tracking lebar, 9pt
|               Tempelkan HP Anda di Sini                   |  <- Font Sans, 8pt, warna abu gelap
|                                                           |
| - - - - - - - - - - - - - - - - - - - - - - - - - - - - - |  <- Garis pemisah halus (opsional)
|                                                           |
|    ┌───────┐     Kamera tanpa NFC?                        |
|    │  QR   │     Scan QR Code di samping                  |  <- QR Code ukuran 22x22mm di pojok kiri bawah
|    └───────┘                                              |
|                                                           |
|                                         Powered by ULASA  |  <- Watermark kecil di pojok kanan bawah (7pt)
+-----------------------------------------------------------+
  [═══════════════════════════════════════════════════════]    <- Tatakan Kayu Pinus (Wooden Base)
```

---

## 🎨 2. Spesifikasi Warna & Tipografi (Print Ready)

* **Palet Warna Cetak (CMYK):**
  - **Background:** Off-White / Warm Cream (`#FDFBF7` -> CMYK: 1, 1, 3, 0) — *Tampak hangat, estetik, dan tidak silau.*
  - **Teks Utama:** Deep Espresso Charcoal (`#1F1A17` -> CMYK: 60, 60, 60, 90).
  - **Aksen Target Tap & Bintang:** Ulasa Warm Gold (`#C5A880` -> CMYK: 20, 30, 50, 0) atau Forest Green (`#2D5A43`).
* **Bahan Cetak:**
  - **Kertas:** Art Paper **260 gsm** atau **310 gsm**.
  - **Finishing:** **Laminasi Doff (Matte)**. *PENTING: Jangan gunakan Glossy* agar tidak memantulkan lampu kafe dan QR code tetap mudah dibaca kamera HP.

---

## 🛠️ 3. Langkah Demi Langkah Pembuatan Mandiri

### Langkah 1: Buat Desain di Canva atau Figma
1. Buka Canva/Figma, buat ukuran kanvas kustom:
   - **Meja Makan:** `10.5 cm x 14.8 cm` (A6).
   - **Meja Kasir:** `14.8 cm x 21.0 cm` (A5).
2. Masukkan logo Sawana Coffee & Eatery atau Villa Lateng Ubud di bagian atas.
3. Buat lingkaran target di tengah dengan diameter 40mm berikon smartphone / gelombang sinyal tap.
4. Letakkan QR Code dinamis di pojok bawah.
5. Export file sebagai **PDF Print (CMYK / High Quality 300 DPI)**.

### Langkah 2: Cetak di Percetakan Digital Terdekat
- Bawa file PDF ke digital printing di Denpasar/Gianyar.
- Minta cetak di kertas Art Paper 260gsm + Laminasi Doff (biaya sekitar Rp 3.000 – Rp 5.000 per lembar A4 yang muat 4 kartu A6).

### Langkah 3: Pemasangan Chip NFC & Perakitan Fisik
1. Ambil 1 lembar kertas A6 yang sudah dipotong rapi.
2. Ambil 1 stiker chip NFC (NTAG213/215).
3. **Tempelkan stiker NFC di bagian BELAKANG kertas**, tepat di tengah-tengah lingkaran *"TAP PHONE HERE"*.
4. Selipkan kertas ke dalam slot akrilik bening A6.
5. Tancapkan akrilik ke tatakan kayu pinus.

### Langkah 4: Program Chip NFC dalam 5 Detik
1. Dekatkan HP Android/iPhone yang sudah terpasang aplikasi **NFC Tools** (atau via Web Admin ULASA).
2. Tulis URL tujuan (misal: `https://tap.ulasa.id/t/swn-01`).
3. Selesai! Stand siap ditaruh di meja Sawana Coffee.
