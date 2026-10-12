# MASTERPLAN & SPECIFICATION: RIKALA.ID LANDING PAGE
## High-Performance Software House & Digital Product Showcase
- **Target Execution Agent:** Claude Code
- **Owner & Founder:** Dewa Biara (Rikala Tech)
- **Domain:** `https://rikala.id`
- **Document Version:** 1.0.0
- **Status:** Ready for Claude Code Execution

---

## 1. Executive Summary & Brand Positioning

**Rikala.id** adalah software house dan tech consultancy berbasis di Bali yang menggabungkan rekayasa perangkat lunak kelas enterprise (Go, TypeScript, PostgreSQL ACID, Distributed Systems) dengan pengalaman operasional lapangan riil di sektor F&B dan Hospitality.

### Unfair Advantage & Positioning:
1. **Practitioner-Led Engineering:** Founder bukan sekadar koder teoretis, melainkan pemilik aktif bisnis operasional di Bali (Sawana Coffee & Eatery dan Villa Lateng Ubud). Setiap arsitektur diuji langsung di lingkungan produksi dengan lalu lintas transaksi nyata.
2. **Financial-Grade Reliability:** Terbiasa membangun append-only ledgers, integrasi pembayaran bergaransi idempotency, sistem offline-first, dan event ingestion skala tinggi (9.8k+ req/s).
3. **Full-Spectrum Delivery:** Mampu mengeksekusi end-to-end: dari smart hardware/NFC IoT, tablet cashier apps offline-first, direct booking engine anti-komisi OTA, hingga backend microservices cloud skala besar.

---

## 2. Portfolio & Product Ecosystem Showcase

Landing page wajib menonjolkan 5 pilar produk dan rekayasa riil yang telah terbukti di produksi:

### 1. Rikala POS (`pos.rikala.id` / `pos.sawanaubud.com`)
- **Kategori:** Modern Cloud POS & Kitchen Display System (KDS).
- **Highlight:** True Offline-First Architecture (SQLite/IndexedDB lokal), WebSocket real-time kitchen screen, manajemen split bill untuk wisatawan mancanegara, integrasi otomatis review loop.
- **Testbed Produksi:** Sawana Coffee & Eatery, Ubud, Bali.

### 2. StayPilot (`staypilot`)
- **Kategori:** Boutique Villa Operations Platform & Direct Booking Engine.
- **Highlight:** Penghematan komisi OTA 15-20% melalui booking engine mandiri, sinkronisasi multi-OTA via iCal otomatis (anti-double booking), alur check-in bilingual dengan HMAC-signed prefill link, dan verifikasi dokumen identitas tamu aman.
- **Testbed Produksi:** Villa Lateng Ubud, Bali.

### 3. SpendWise (`spendwise.rikala.id`)
- **Kategori:** Multi-Wallet Financial Management Platform.
- **Highlight:** Pencatatan arus kas dengan double-entry ledger, bank statement import & categorization, PIN-level security & HttpOnly JWT, analitik laba rugi real-time.

### 4. ULASA / TapReview (`ulasa`)
- **Kategori:** Smart NFC & QR Digital Reputation Hardware + SaaS.
- **Highlight:** Stand meja berbahan kayu tropis & akrilik premium, smart review gating compliant dengan Google (feedback internal untuk bintang 1-3, auto-redirect ulasan bintang 4-5 ke Google Maps).

### 5. High-Throughput Distributed Gateway (`go-tracking-gateway`) & Enterprise Commerce
- **Kategori:** High-Scale Backend Engineering & Commerce API.
- **Highlight:** Gateway penanganan event berkecepatan 9.800 req/s (p50 latency 0.97ms, 0% error) berbasis Go & Redis Streams, append-only store credit ledger (900+ API endpoints), dan integrasi webhook Stripe bergaransi idempotency.

---

## 3. Tech Stack Specification

- **Framework:** Next.js 14/15 (App Router, React 19, TypeScript)
- **Styling:** Tailwind CSS (dengan dark mode bernuansa zinc/slate premium, aksen emerald & amber)
- **UI Components:** Shadcn UI / Radix Primitives + Lucide React icons
- **Animations:** Framer Motion (subtle scroll reveals & bento card hover effects)
- **Form Handling:** Next.js Server Actions / API Route dengan:
  - Validasi ketat (Zod)
  - Honeypot anti-bot trap (`name="website"`)
  - In-memory / IP rate limiting
  - Direct WhatsApp auto-redirect dengan prefilled message template
- **SEO & Meta:** Full OpenGraph, Twitter Cards, semantic JSON-LD Organization markup, sitemap.xml, robots.txt
- **Deployment:** Dockerfile multi-stage build + Nginx reverse proxy configuration

---

## 4. Struktur Halaman & Wireframe Desain

### A. Navigation Bar (Sticky / Glassmorphism)
- Logo: **RIKALA.ID** (Modern minimalist sans-serif typography)
- Links: Layanan, Ekosistem Produk, Studi Kasus, Keunggulan, FAQ
- CTA Button: `Konsultasi Proyek` (anchor ke `#kontak`)

### B. Hero Section
- **Badge:** `📍 Bali-Based • Enterprise-Grade Engineering • Practitioner-Led`
- **Headline:** *"Rekayasa Perangkat Lunak Skala Tinggi untuk Bisnis yang Tidak Boleh Berhenti."*
- **Sub-headline:** *"Kami merancang sistem backend berkinerja tinggi, platform POS offline-first, direct booking engine villa, dan solusi digital custom yang diuji langsung di bisnis operasional nyata."*
- **Call-to-Action:** Dual button:
  1. `Diskusikan Kebutuhan Anda` (Primary button -> WhatsApp / Form)
  2. `Eksplorasi Studi Kasus` (Secondary button -> `#portofolio`)
- **Live Metrics Counter:**
  - `9.800+` req/s Event Throughput Tested
  - `99.9%` System Availability
  - `15-20%` Margin Diselamatkan dari Komisi OTA
  - `0` Downtime pada Operasional Jam Sibuk

### C. The "Practitioner-Led" Advantage (Bento Grid)
- **Mengapa Rikala Berbeda:**
  - *Kartu 1 (Living Testbeds):* Bukan sekadar koding di atas kertas. Kami menguji langsung di kafe kami (Sawana Coffee) dan villa kami (Villa Lateng).
  - *Kartu 2 (Zero Vendor Lock-In):* 100% kode sumber dan kepemilikan infrastruktur diserahkan sepenuhnya ke klien.
  - *Kartu 3 (Financial-Grade Engineering):* ACID compliance, append-only ledgers, dan perlindungan idempotency mencegah kebocoran data & dana.
  - *Kartu 4 (Offline-First Resiliency):* Sistem tetap bekerja optimal bahkan saat koneksi internet lokal di Bali mengalami gangguan.

### D. Ekosistem Produk & Portofolio (Interactive Tabs / Cards)
Tab switcher atau card grid menampilkan 5 produk unggulan:
- Detail teknis masing-masing produk (Stack, Masalah yang Dipecahkan, Hasil Riil).
- Tombol `Lihat Live Demo` / `Studi Kasus` (menautkan ke subdomain terkait seperti `spendwise.rikala.id` atau repositori showcase).

### E. Layanan Custom Software House (Services Section)
1. **Hospitality & Villa Direct Booking Systems:**
   - Booking engine mandiri, kalender iCal sinkronisasi anti-double booking, payment gateway Midtrans/Xendit/Stripe.
2. **F&B Cloud POS & Kitchen Automation:**
   - Aplikasi kasir multi-outlet, KDS real-time, manajemen resep & COGS/HPP.
3. **High-Throughput Backend & Microservices:**
   - Arsitektur Go, distributed caching Redis Streams, optimasi PostgreSQL, Clean Architecture.
4. **Digital Reputation & Smart NFC Solutions:**
   - Hardware stand akrilik-kayu custom, review gating platform, automated reputation boosting.

### F. Tech Stack & Engineering Standards
Grid logo/badge teknologi:
- **Languages:** Go (Golang), TypeScript, Python, SQL
- **Frameworks:** Next.js, React, Gin, Chi, FastAPI, NestJS
- **Databases:** PostgreSQL, Redis Streams, SQLite, Typesense
- **Infra:** Docker, Google Cloud Platform (Cloud Run, Cloud Build), Nginx, Cloudflare

### G. Interactive Consultation Form / Project Inquiries
- Input Fields: Nama Lengkap, Nomor WhatsApp, Email Bisnis, Jenis Layanan (Villa System, POS Kafe, Custom Backend, Lainnya), Estimasi Timeline, Deskripsi Kebutuhan.
- Field Tersembunyi: Honeypot trap anti-spam bot.
- Tombol: `Kirim Permintaan & Buka WhatsApp Langsung`

### H. FAQ Section (Accordion)
- Berapa estimasi waktu pengerjaan proyek kustom?
- Apakah kami mendapatkan source code lengkap setelah proyek selesai? (Ya, 100% milik klien).
- Bagaimana dengan dukungan pemeliharaan (*maintenance SLA*) setelah go-live?
- Apakah Rikala bisa mengintegrasikan sistem dengan software kasir atau PMS yang sudah ada?

### I. Footer
- Branding Rikala.id, lokasi (Ubud & Seminyak, Bali), direct email (`halo@rikala.id`), WhatsApp business link, link kebijakan privasi & syarat ketentuan.

---

## 5. Claude Code Implementation Roadmap

### Phase 1: Environment & Scaffolding
```bash
# 1. Inisialisasi Next.js project
npx create-next-app@latest rikala-web --typescript --tailwind --eslint --app --src-dir --import-alias "@/*" --use-npm

# 2. Install dependencies
cd rikala-web
npm install lucide-react clsx tailwind-merge framer-motion
```

### Phase 2: Design Tokens & Base Theme
- Setup font: `Inter` atau `Plus Jakarta Sans` untuk heading/body.
- Konfigurasi warna di `tailwind.config.ts`:
  - `background`: Dark modern zinc (`#09090b` / `#0f172a`) dengan light mode support.
  - `primary`: Emerald accent (`#10b981` / `#059669`) untuk trust & performa.
  - `accent`: Amber warm gold (`#f59e0b` / `#d97706`) untuk luxury hospitality touch.

### Phase 3: Komponen & Halaman Utama
- Buat modular components di `src/components/`:
  - `navbar.tsx`
  - `hero.tsx`
  - `metrics.tsx`
  - `advantages.tsx`
  - `portfolio.tsx`
  - `services.tsx`
  - `tech-stack.tsx`
  - `consultation-form.tsx`
  - `faq.tsx`
  - `footer.tsx`

### Phase 4: Server Action & Form Handling
- Buat endpoint `src/app/api/leads/route.ts` atau Server Action `submitLead()`:
  - Cek honeypot (`website` field). Jika terisi bot, kembalikan fake success `200 OK`.
  - Validasi panjang teks dan nomor telepon.
  - Format respon untuk me-redirect ke WhatsApp dengan teks pesan tersusun rapi.

### Phase 5: Build, Test, & Dockerization
- Test build production: `npm run build`.
- Siapkan `Dockerfile` (multi-stage Node.js Alpine) dan `docker-compose.yml`.
- Siapkan template Nginx reverse proxy untuk domain `rikala.id`.
