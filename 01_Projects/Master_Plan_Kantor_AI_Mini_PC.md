# MASTER BLUEPRINT: KANTOR AI MANDIRI (VIRTUAL OFFICE MULTI-AGENT)
*Arsitektur Multi-Agent Enterprise-Grade Berjalan 24/7 di Dedicated Mini PC Server*

- **Dokumen ID:** `PLAN-VIRTUAL-OFFICE-2026-V1`
- **Author:** Thena & Dewa Biara
- **Tanggal Dibuat:** 18 Oktober 2026
- **Status:** Final Master Plan (Menunggu Pengadaan Mini PC)
- **Target Hardware:** Mini PC Headless Home Server (Intel N100 / AMD Ryzen, 16GB–32GB RAM, 512GB NVMe SSD, Ubuntu Server 24.04 LTS)

---

## 1. Visi & Filosofi Sistem
Membangun "Kantor AI" mandiri berbasis *Hierarchical Multi-Agent System* yang dapat bekerja 24/7 mengotomatiskan riset, konten, operasional, dan intelligence bisnis untuk seluruh unit usaha (Sawana Coffee & Eatery, Villa Lateng Ubud, Rikala, dan Client Software Projects).

User berkomunikasi melalui **Discord** dengan **Thena (Chief of Staff)**. Thena menerjemahkan arahan bisnis menjadi instruksi teknis kepada **Office Manager Agent**, yang kemudian mengorkestrasi para **Worker Agents (Karyawan AI)** secara paralel atau serial, menyimpan hasil ke database/Notion, dan melaporkan kemajuan secara real-time.

---

## 2. Struktur Departemen & Karyawan AI (Agent Roles & SOP)

```
                       ┌─────────────────────────┐
                       │   Owner / Dewa Biara    │
                       └────────────┬────────────┘
                                    │ (Natural Language via Discord)
                                    ▼
                       ┌─────────────────────────┐
                       │  Thena (Chief of Staff) │
                       └────────────┬────────────┘
                                    │ (REST / Webhook API)
                                    ▼
       ═════════════════════════════════════════════════════════════════════════════════════
       │                      OFFICE MANAGER AGENT (Orchestrator)                          │
       │                 (Model: Claude 3.5 Sonnet via OpenRouter)                         │
       ═════════════════════════════════════════════════════════════════════════════════════
              │                      │                      │                      │
      ┌───────┴──────┐       ┌───────┴──────┐       ┌───────┴──────┐       ┌───────┴──────────┐
      │ DEPARTEMEN   │       │ DEPARTEMEN   │       │ DEPARTEMEN   │       │ RIKALA TECH      │
      │ RISET & DATA │       │ KONTEN & ADS │       │ OPERASIONAL  │       │ ENGINEERING DIV  │
      └───────┬──────┘       └───────┬──────┘       └───────┬──────┘       └───────┬──────────┘
              ▼                      ▼                      ▼                      ▼
     [Market Analyst]        [Copywriter]           [SOP & Policy]         [Product Manager]
     [Competitor Scout]      [Hook & Scriptwriter]  [Customer Service]     [UI/UX Designer]
     [Financial Auditor]     [Visual Prompt Eng]    [Lead Outreach]        [Backend Architect]
                                                                           [Frontend Engineer]
                                                                           [QA & Sec Auditor]
                                                                           [DevOps Specialist]
```

### Departemen 1: Riset Pasar & Data Intelligence (`Dept-Research`)
1. **Agent: Market & Competitor Scout**
   - **Tugas:** Scraping data kompetitor lokal Bali (harga menu kopi, review Google Maps, promo villa), memantau pergerakan bursa/IHSG, dan menyajikan ringkasan benchmarking.
   - **Model:** DeepSeek V3/V4 via OmniRouter (Low cost, high throughput).
   - **Tools:** Internal Python Scraper, Google Search API, HTTP RPC parser.
2. **Agent: Financial & Revenue Auditor**
   - **Tugas:** Mengaudit data transaksi POS harian (Sawana/Rikala), memetakan rasio HPP, menghitung margin, dan mendeteksi anomali stok.
   - **Model:** Claude 3.5 Haiku / DeepSeek via OmniRouter.
   - **Output:** Markdown tabel keuangan mingguan & rekomendasi efisiensi.

### Departemen 2: Konten & Pemasaran Kreatif (`Dept-Creative`)
1. **Agent: Copywriter & Narrative Strategist**
   - **Tugas:** Menulis naskah konten berdasarkan data riset. Menguasai framework copywriting: *AIDA*, *PAS (Problem-Agitate-Solution)*, dan *Before-After-Bridge*.
   - **Spesialisasi:** Caption Instagram Reels Sawana/Villa, script video TikTok, proposal klien software house.
   - **Model:** DeepSeek / Kimi / GPT-4o-mini via OmniRouter.
2. **Agent: Visual Prompt Engineer**
   - **Tugas:** Mengubah narasi konten menjadi parameter prompt visual presisi tinggi untuk Midjourney / Flux / DALL-E (lengkap dengan aspect ratio, lighting, color grading).

### Departemen 3: Operasional & Outreach Bisnis (`Dept-Operations`)
1. **Agent: SOP & System Architect**
   - **Tugas:** Menyusun dokumen SOP standar karyawan fisik (barista, housekeeping villa, admin kasir) dan panduan kepatuhan operasional.
   - **Model:** Claude 3.5 Sonnet (OpenRouter).
2. **Agent: B2B Lead Outreach & Cold Messenger**
   - **Tugas:** Membaca database lead (hasil scraper Google Maps Canggu/Seminyak/Ubud) dan menghasilkan draf penawaran personal untuk WhatsApp/Email/Instagram DM.

### Departemen 4: Rikala Tech Engineering Division (`Dept-Engineering`)
*Divisi khusus untuk mengeksekusi end-to-end software development project internal maupun klien Rikala Tech dengan **Hybrid Model Architecture** (Claude 3.5 Sonnet + DeepSeek-V3/R1).*

1. **Agent: Product Manager (PM Agent)**
   - **Tugas:** Mengubah ide mentah/kebutuhan klien menjadi PRD (*Product Requirement Document*), User Stories, kriteria penerimaan (*Acceptance Criteria*), dan breakdown scope per modul/sprint.
   - **Model:** **Claude 3.5 Sonnet** via OpenRouter (High Context & Semantic Reasoning).
   - **Output:** File markdown PRD terstruktur lengkap dengan user journey.
2. **Agent: UI/UX Designer Agent**
   - **Tugas:** Menghasilkan spesifikasi arsitektur informasi, wireframe text-spec, dan Design System Tokens (skema warna Tailwind, font hierarchy, component spacing, layout behavior) yang siap diterjemahkan langsung oleh Frontend.
   - **Model:** **Claude 3.5 Sonnet / GPT-4o** via OpenRouter.
3. **Agent: Backend Architect & Engineer**
   - **Tugas:** Merancang arsitektur API (OpenAPI/Swagger 3.0), skema database relasional (PostgreSQL DDL / Prisma schema), caching strategy (Redis), idempotency key handling, dan struktur clean code (Go / NestJS / Node.js).
   - **Model:** **DeepSeek-V3** via OmniRouter (Super fast & cost-efficient workhorse).
4. **Agent: Frontend Engineer**
   - **Tugas:** Membangun antarmuka pengguna interaktif (React, Next.js, Vite SPA, Tailwind CSS), integrasi REST/GraphQL API hooks, form validation (Zod/React Hook Form), serta memastikan responsivitas layar mobile/desktop.
   - **Model:** **DeepSeek-V3** via OmniRouter.
5. **Agent: QA & Security Auditor**
   - **Tugas:** Merancang skenario pengujian komprehensif (Unit Test, Integration Test, E2E Test Cases via Playwright/Jest), melakukan audit celah keamanan (OWASP Top 10, Auth RBAC, SQL injection prevention, idempotency race condition, edge cases).
   - **Model:** **DeepSeek-R1** via OmniRouter (Deep reasoning & chain-of-thought code auditing).
6. **Agent: DevOps & Release Engineer**
   - **Tugas:** Menghasilkan `Dockerfile` multi-stage build yang ringan, `docker-compose.yml`, CI/CD workflow (GitHub Actions), serta panduan deployment ke GCP Cloud Run atau VPS.
   - **Model:** **DeepSeek-V3** via OmniRouter.

---

## 3. Topologi Infrastruktur Hardware (Dedicated Mini PC)

### Spesifikasi Rekomendasi Mini PC:
* **Processor:** Intel 12th Gen Alder Lake-N **N100** (4 Core 4 Thread, 6W TDP hemat listrik) ATAU **AMD Ryzen 5 5500U/6600H** (jika ingin multi-agent lokal berat).
* **RAM:** **16 GB DDR4/DDR5** (atau 32 GB jika selisih harga tipis) — *Wajib cukup agar bisa menjalankan multi-service tanpa swap disk*.
* **Storage:** **512 GB M.2 NVMe SSD** (kecepatan baca/tulis > 2000 MB/s, tahan bertahun-tahun untuk logging dan database).
* **Koneksi:** Gigabit LAN (kabel RJ45 langsung ke router WiFi) + UPS mini (DC UPS) agar tidak mati saat listrik padam mendadak.
* **Suhu & Daya:** Konsumsi listrik ~10–25 Watt (biaya listrik PLN hanya sekitar Rp15.000 – Rp30.000 per bulan jika hidup 24/7).

### Network & Remote Access Setup (Tanpa IP Publik Statis):
* **Tailscale Mesh VPN:** Hubungkan Mini PC, Laptop, dan HP ke dalam 1 jaringan private mesh. Kamu bisa SSH dan buka dashboard kantor AI dari mana saja di dunia secara aman.
* **Cloudflare Tunnel (`cloudflared`):** Untuk mengekspos webhook Discord / Webhook eksternal ke Mini PC tanpa perlu port-forwarding router dan tanpa risiko IP rumah terbuka ke internet.

---

## 4. Arsitektur Software & Container Stack (Docker Compose)

Semua komponen berjalan dalam satu file `docker-compose.yml` modular di Mini PC:

```
[ Internet / Cloud ]
   │
   ├── OpenRouter (Claude 3.5 Sonnet / High Reasoning)
   └── Discord Gateway (User Chat Channel)
   │
[ Mini PC Server (Local Network via Tailscale) ]
   ├── Container 1: reverse-proxy (Traefik / Nginx Proxy Manager)
   ├── Container 2: omni-router (Local LLM Gateway / Proxy)
   ├── Container 3: virtual-office-backend (FastAPI + LangGraph Engine)
   ├── Container 4: virtual-office-web (Dashboard UI / Realtime SSE)
   ├── Container 5: postgres-db (State Checkpointing & History)
   ├── Container 6: redis-broker (Task Queue & PubSub Event)
   └── Container 7: hermes-agent (Thena Local Daemon)
```

---

## 5. Protokol Interaksi Antar-Agen (Execution Workflow)

Setiap instruksi dari Dewa Biara di Discord mengikuti alur siklus kerja 5 tahap:

1. **Ingestion & Intent Classification:**
   - Dewa: *"Thena, buatkan strategi promo akhir pekan untuk Sawana Ubud dan siapkan 3 hook konten Instagram Reels."*
   - Thena memvalidasi parameter dan meneruskannya ke `POST /api/tasks`.
2. **Decomposition (Office Manager):**
   - Manager Agent menganalisis tugas dan membagi menjadi 2 tiket kerja (*Work Orders*):
     - `Task 1 (Dept-Research)`: Analisis data menu terlaris dan promo kompetitor kafe sekitar.
     - `Task 2 (Dept-Creative)`: Pembuatan 3 variasi script Reels berdasarkan hasil Task 1.
3. **Parallel / Sequential Execution (Workers):**
   - Agen Riset mengambil data dari internal knowledge base / database.
   - Setelah selesai, output dilempar sebagai input ke Copywriter Agent.
4. **Quality Review (Manager):**
   - Manager Agent memeriksa apakah hook sudah memenuhi kaidah retensi penonton 3 detik pertama dan sesuai tone of voice Sawana. Jika kurang memuaskan, Manager menginstruksikan revisi internal otomatis.
5. **Human Approval Delivery:**
   - Thena merangkum hasil akhir ke Discord lengkap dengan opsi: `[Approve]`, `[Revisi]`, atau `[Simpan ke Notion]`.

### B. Workflow Khusus Divisi Tech (Rikala Tech Software Pipeline):
Jika tugasnya adalah membangun fitur/aplikasi baru (misal: *"Buatkan modul split bill untuk Sawana POS"*):
1. **PM Agent:** Merilis PRD, daftar endpoint yang dibutuhkan, dan acceptance criteria.
2. **UI/UX Designer Agent:** Merancang token komponen Tailwind, layout form/tabel, dan micro-interaction flow.
3. **Backend Architect Agent:** Menghasilkan file migration PostgreSQL, skema Prisma/Go struct, endpoint handler dengan validasi input & idempotency logic.
4. **Frontend Engineer Agent:** Mengonsumsi skema API dan merangkai komponen React/Next.js UI.
5. **QA & Security Auditor Agent:** Menjalankan automated test, mengecek race condition, dan menerbitkan checklist "Ready to Merge / Deploy".
6. **Delivery:** Thena melaporkan ke Dewa Biara di Discord dengan ringkasan PRD, diff kode, dan hasil test pass 100%.

---

## 6. Roadmap Eksekusi Tanpa Masalah (Execution Checklist Saat Mini PC Tiba)

### Fase 1: Setup Baremetal & OS (Estimasi: 1–2 Jam)
- [ ] Flash Ubuntu Server 24.04 LTS ke flashdisk menggunakan BalenaEtcher / Rufus.
- [ ] Install OS secara headless (set username, hostname: `athena-node`, disable sleep/hibernate).
- [ ] Pasang SSH Key authentication (disable password login).
- [ ] Install Docker Engine & Docker Compose plugin resmi.
- [ ] Install Tailscale dan hubungkan node ke Tailnet pribadi.

### Fase 2: Deploy Gateway & Database Core (Estimasi: 1 Jam)
- [ ] Setup `docker-compose-core.yml` berisi PostgreSQL, Redis, dan Omni Router.
- [ ] Verifikasi Omni Router berjalan di port lokal (`http://127.0.0.1:3000`) dan tes ping API key.
- [ ] Setup volume backup otomatis harian ke Google Drive / GitHub private.

### Fase 3: Scaffold & Deploy `virtual-office-ai` (Estimasi: 2 Jam via Claude Code)
- [ ] Jalankan Claude Code di laptop untuk scaffolding source code sesuai spesifikasi `Spesifikasi_Teknis_Kantor_AI.md`.
- [ ] Push repository ke GitHub.
- [ ] Di Mini PC, lakukan `git clone` dan jalankan via container `virtual-office-backend`.
- [ ] Uji coba endpoint SSE `/api/tasks/{task_id}/stream` melalui browser via IP Tailscale.

### Fase 4: Integrasi Thena & Discord Dispatcher (Estimasi: 30 Menit)
- [ ] Hubungkan Thena bot ke backend lokal via network bridge.
- [ ] Lakukan *end-to-end dry run*: kirim tugas dari Discord -> eksekusi multi-agent -> laporan balik di Discord.
- [ ] Rayakan: Kantor AI mandiri pertama resmi beroperasi 24/7! 🚀
