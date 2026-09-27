# 🌐 Estimasi Biaya Pembuatan Website Profil Usaha (Company Profile)

- **Inisiator:** [[Dewa Biara]]
- **Tujuan:** Panduan biaya infrastruktur riil (Domain & Server) untuk proyek website profil usaha klien/teman.
- **Tautan Terkait:** [[01_Projects/Blueprint_Ekspansi_Software_House_Bali]] | [[01_Projects/Master_Roadmap_ULASA_ke_Software_House_Bali]]

---

## 💡 1. Fakta Menarik: Biaya Server Sebenarnya Bisa Rp 0 (Gratis)!

Untuk website **profil usaha (company profile / landing page)**, kamu **TIDAK PERLU menyewa server bulanan yang mahal**.

Dengan stack modern (Next.js, Astro, atau HTML/Tailwind):
- **Hosting di Vercel / Cloudflare Pages:** **Rp 0 / bulan (Gratis Selamanya)**.
  - Sudah termasuk sertifikat keamanan SSL (HTTPS) resmi otomatis.
  - Kecepatan akses ultra-cepat karena memakai Global Edge CDN.
  - Kapasitas bandwith gratis mencakup puluhan ribu pengunjung per bulan (sangat berlebih untuk web profil kafe/toko/villa).

---

## 📊 2. Rincian Biaya Riil (Hanya Bayar Nama Domain)

Satu-satunya biaya riil yang wajib dibayar per tahun adalah **nama domain**:

| Ekstensi Domain | Estimasi Biaya (Per Tahun) | Keterangan & Rekomendasi |
|---|---|---|
| **`.com`** *(Rekomendasi Utama)* | **Rp 140.000 – Rp 180.000** | Standar internasional, paling terpercaya di mata pelanggan dan turis bule. |
| **`.id`** | **Rp 220.000 – Rp 250.000** | Domain resmi Indonesia, sangat prestisius untuk PT/CV lokal. |
| **`.co.id`** | **Rp 110.000 – Rp 150.000** | Butuh syarat legalitas usaha (NIB/Akta). |
| **`.my.id`** *(Opsi Hemat)* | **Rp 12.000 – Rp 25.000** | Opsi termurah untuk uji coba awal. |

*Tempat Pembelian Terbaik:* Cloudflare Registrar, Niagahoster, Domainesia, atau Namecheap.

---

## ⚙️ 3. Dua Opsi Setup Infrastruktur

### 🟢 OPSI A: Vercel / Cloudflare Pages + Domain (Paling Direkomendasikan)
- **Cocok Untuk:** Web profil, menu kafe, portfolio, landing page villa.
- **Biaya Server:** **Rp 0 (Gratis)**.
- **Biaya Domain:** **~Rp 160.000 / tahun**.
- **Total Biaya Tahun Pertama:** **Hanya Rp 160.000 untuk 1 tahun penuh!**
- *(Temanmu cukup transfer uang domain Rp 160rb, web langsung online selama setahun).*

---

### 🟡 OPSI B: VPS Docker Multi-Web (Jika Membutuhkan Database / Backend Go)
- **Cocok Untuk:** Jika web usahanya butuh dashboard admin kustom, backend database PostgreSQL, atau sistem inventaris.
- **Biaya Server:** Sewa VPS (Hetzner Cloud atau IDCloudHost) seharga **~Rp 65.000 – Rp 85.000 / bulan**.
- **Kelebihan:** 1 VPS ini bisa kamu pakai bersama untuk menampung **5 hingga 10 website klien sekaligus** menggunakan Nginx Reverse Proxy / Docker container!
