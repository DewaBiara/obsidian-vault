# 🎨 Branding & UI/UX Design System: Smart NFC Review Platform

- **Dokumen:** Identitas Merek, Konsep Visual Hardware, & Desain Antarmuka (UI/UX)
- **Inisiator:** [[Dewa Biara]]
- **Tanggal:** 2026-09-24
- **Tautan Terkait:** [[01_Projects/Spesifikasi_Teknis_TapReview_Gateway]] | [[01_Projects/Deep_Analysis_NFC_Review_SaaS_Bali]]

---

## 🏷️ 1. Opsi Nama Branding (Brand Identity)

Karakteristik yang dibutuhkan: Modern, ringkas, mudah diucapkan oleh staf lokal maupun ekspat/turis asing di Bali, serta terkesan seperti platform teknologi berkelas (bukan sekadar tukang cetak akrilik).

### Opsi 1: **"Ulasa"** (atau **Ulasa.id** / **Ulasa Bali**) — *Rekomendasi Utama*
- **Filosofi:** Berakar dari kata bahasa Indonesia *"Ulasan"* (Review/Feedback). Terdengar anggun, ramah, dan bernuansa tropis.
- **Tagline:** *"One Tap. Five Stars."* / *"Reputasi Digital Terbaik untuk Bisnis Bali."*
- **Cocok Untuk:** Branding lokal yang profesional, menaungi F&B, boutique villa, dan spa.

### Opsi 2: **"TapVibe"** (atau **TapVibe Bali**)
- **Filosofi:** Menggabungkan aksi fisik (*Tap*) dengan atmosfer/suasana tempat (*Vibe*). Sangat relate dengan kultur kafe dan beach club di Canggu & Seminyak.
- **Tagline:** *"Share the Vibe, Leave a Star."*

### Opsi 3: **"Karsa Review"** (Sub-Brand Ekosistem)
- **Filosofi:** Memperluas ekosistem software [[Karsa]] yang sudah kamu bangun.
- **Tagline:** *"Smart Reputation & Guest Experience."*

---

## 🪵 2. Desain Fisik Stand Meja (Hardware Industrial Design)

Vibe Bali mengutamakan material alami, minimalis, dan elegan (tidak terkesan seperti promosi murah).

### Spesifikasi Visual Stand Akrilik + Kayu A6 (10x15 cm):
```
┌───────────────────────────────────────┐
│              [LOGO VENUE]             │  <- 25mm dari atas (Sawana Coffee / Villa Lateng)
│                                       │
│          Enjoyed Your Time?           │  <- Heading: Playfair Display / Serif hangat
│       Bagikan Pengalaman Anda         │  <- Subheading: Inter / Sans-serif halus
│                                       │
│                ╭─────╮                │
│                │ 📳  │                │  <- Ikon NFC / Smartphone Tap (Gold / Forest Green)
│                │ TAP │                │     Diameter 40mm (posisi chip NTAG213 di belakang)
│                ╰─────╯                │
│            TAP PHONE HERE             │  <- All Caps, Tracking lebar, 9pt bold
│                                       │
│  - - - - - - - - - - - - - - - - - -  │
│                                       │
│   ┌───────┐   No NFC? Scan QR Code    │  <- QR Code dinamis cadangan di pojok kiri bawah
│   │ QR    │   Kamera HP tanpa NFC     │
│   └───────┘                           │
│                                       │
│                     Powered by ULASA  │  <- Watermark kecil elegan di pojok kanan bawah
└───────────────────────────────────────┘
     [═════════════════════════════]       <- Base Tatakan Kayu Pinus / Jati Belanda Natural
```

* **Palet Warna Fisik:**
  - Background: Off-White / Warm Cream (`#FDFBF7`) — memberi kesan mewah, ramah di mata.
  - Teks Utama: Deep Charcoal / Espresso (`#1F1A17`) — bukan hitam pekat.
  - Aksen / Ikon Tap: Soft Gold (`#C5A880`) atau Forest Green (`#2D5A43`).

---

## 📱 3. Desain Antarmuka Public Smart Gate (`/f/:slug_code`)

Halaman web responsif ultra-ringan yang dimuat pengunjung saat melakukan *tap* di meja.

### Prinsip UX:
1. **Zero Loading Delay:** HTML/CSS dikompresi di bawah 15KB agar terbuka seketika (<500ms) di koneksi seluler 4G.
2. **Micro-Interactions yang Menyenangkan:** Bintang memiliki efek hover/tap lembut (bouncing animation) dengan getaran haptic di smartphone.

### Alur Tampilan Layar (Wireframe):

```
+---------------------------------------+
|                                       |
|           [Logo Resto/Villa]          |
|                                       |
|        Sawana Coffee & Eatery         |
|   Bagaimana pengalaman Anda hari ini?  |
|                                       |
|        ⭐   ⭐   ⭐   ⭐   ⭐         |  <- 5 Tombol Bintang Besar (Mudah di-tap jempol)
|                                       |
|  - - - - - - - - - - - - - - - - - -  |
|                                       |
|  [Jika Bintang 4 atau 5 ditekan]:     |
|  -> Animasi confetti kecil ✨         |
|  -> Langsung auto-redirect ke Google  |
|     Review dalam 0.8 detik.           |
|                                       |
|  [Jika Bintang 1, 2, atau 3 ditekan]: |
|  -> Muncul form santun & empatik:     |
|     "Mohon maaf atas ketidaknyamanan  |
|      Anda. Apa yang bisa kami         |
|      tingkatkan?"                     |
|     [Textarea: Masukan Anda...]       |
|     [Input: No WhatsApp (opsional)]   |
|     [Tombol: Kirim ke Manajer (WA)]   |
|                                       |
|  [Footer Legal Kepatuhan Google]:     |
|  "Ingin tetap menulis di Google Maps? |
|   Klik di sini"                       |
+---------------------------------------+
```

---

## 💻 4. Desain Dashboard Admin PWA (`/admin`)

Dioptimalkan untuk penggunaan mobile di smartphone Android/iPhone milik Dewa saat melakukan *provisioning* fisik di kafe/villa.

### Layar Provisioning (Fitur Kunci):
- **Header:** Pemilihan Venue (`Sawana Coffee & Eatery`).
- **Input Meja:** Nomor meja (`Meja 08 - Outdoor`).
- **Kartu Animasi NFC:**
  - Kotak besar dengan animasi gelombang berdenyut (*pulsing wave animation*).
  - Teks instruksi: *"Tekan tombol di bawah lalu tempelkan chip NFC ke punggung HP Anda."*
  - Tombol Besar: **[ 📳 TULIS & PAIRING TAG ]**
  - Saat sukses: Muncul suara/getaran sukses dan status berubah hijau: `Meja 08 Siap Digunakan! (URL: tap.ulasa.id/t/swn-08)`.

---

## 🎯 5. Kesimpulan Brand Strategy
Dengan nama **Ulasa**, kamu memposisikan bisnismu sebagai **"Konsultan Reputasi & Tamu"** di Bali:
- Nilai yang kamu jual ke pemilik kafe bukan sekadar "akrilik", melainkan: **"Ulasan Bintang 5 Bertambah, Komplain Negatif Langsung Diselesaikan di Meja."**
