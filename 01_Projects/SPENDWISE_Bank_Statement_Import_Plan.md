# RENCANA IMPLEMENTASI (IMPLEMENTATION PLAN)
## FITUR IMPORT MUTASI REKENING (BANK STATEMENT IMPORT) & STRATEGI MONETISASI PRO
### Platform SpendWise (`https://spendwise.rikala.id`)

> **Versi Dokumen:** 2.0  
> **Tanggal:** 11 Oktober 2026  
> **Status:** Draft Arsitektur, Analisis Kompetitor & Spesifikasi Teknis  
> **Arsitektur:** Strict Clean Architecture (Go 1.22+) & Next.js 14+ (App Router)  

---

## 1. Latar Belakang & Tujuan (Objective)

Pencatatan manual satu-per-satu (*manual bookkeeping*) merupakan titik friksi terbesar yang menyebabkan pengguna berhenti menggunakan aplikasi keuangan. Mengingat API Open Banking / agregator komersial di Indonesia mahal, rapuh (sering putus koneksi bank), dan memerlukan perizinan kompleks, fitur **Import Mutasi Rekening (CSV / e-Statement)** adalah solusi strategis terbaik.

### Sasaran Utama:
1. **Zero Friction Onboarding:** Pengguna dapat memasukkan 100+ transaksi bulanan dalam hitungan detik.
2. **Deduplikasi 100% Akurat:** Transaksi yang diimpor berulang kali tidak boleh menggandakan saldo ledger (*idempotent import*).
3. **Privasi & Keamanan Penuh (Trust Design):** Pengguna memegang kendali penuh tanpa menyerahkan kredensial login perbankan mereka.
4. **Auto-Categorization:** Sistem mampu menebak kategori transaksi secara cerdas berdasarkan pola deskripsi mutasi bank lokal.

---

## 2. Analisis Pasar & Keunggulan Bersaing (Competitive Advantage)

### A. Peta Kompetitor di Indonesia
* **Finku & Sribuu:** Mengandalkan auto-sync bank (*open finance*). Kelemahannya: sering putus koneksi (*disconnect*), meminta password/OTP m-Banking (isu privasi), dan aplikasi terlalu padat dengan promosi pinjaman/asuransi.
* **Finansialku:** Berbayar (Rp 35rb/bln), namun UI/UX kuno dan proses pencatatan masih terasa kaku.
* **YNAB / Wallet:** Global, mahal (~Rp 240rb/bln untuk YNAB), dan tidak mendukung format mutasi bank lokal Indonesia (BCA, Jago, SeaBank).

### B. Posisi Unik SpendWise (The Linear of Personal Finance)
* **Privacy-First & No Bank Credentials:** Pengguna mengunggah CSV mutasi mereka sendiri. File langsung dimusnahkan setelah diparsing (tidak disimpan di server).
* **Fokus Murni Ledger:** Tanpa iklan, tanpa jualan produk pinjaman pihak ketiga.
* **Kecepatan & Estetika:** Desain minimalis berbasis Next.js 14 dan Go backend yang sangat responsif.

---

## 3. Strategi Model Bisnis & Monetisasi (Pricing & Tiers)

Untuk menjaga keberlanjutan produk tanpa mengorbankan privasi, SpendWise menerapkan model **Freemium SaaS** dengan batasan kuota yang adil:

### 1. Free Tier (Umpan Akuisisi)
* Pencatatan manual unlimited.
* Maksimal 2 akun / dompet aktif.
* Kuota Import Mutasi: **1x per bulan** (cukup untuk merasakan kemudahan impor).
* Laporan bulanan standar.

### 2. SpendWise PRO (Monetisasi Utama)
* **Harga:** **Rp 25.000 / bulan** (atau **Rp 199.000 / tahun**).
* **Fitur Eksklusif PRO:**
  * **Unlimited Bank Statement CSV Import** (BCA, Jago, SeaBank, Mandiri).
  * **Unlimited Akun & Dompet** (termasuk kartu kredit & e-wallet).
  * **Smart Rules Auto-Categorization** (sistem mengenali pola merchant berulang).
  * **Budget Rollover & Advanced Analytics**.

---

## 4. Cakupan Format Bank (Bank Support Matrix)

### Fase 1 (Prioritas Utama — CSV Parser):
* **BCA (myBCA & KlikBCA Individu):** Format CSV mutasi rekening.
* **Bank Jago:** Format CSV standar.
* **SeaBank:** Format CSV tabungan.
* **Format Generic CSV:** Templat standar SpendWise (`date,type,amount,merchant,note,category`).

### Fase 2 (Pengembangan Lanjutan):
* **Bank Mandiri (Livin'):** CSV / PDF e-Statement.
* **OCR / PDF Parser:** Ekstraksi e-Statement resmi.

---

## 5. Desain Skema Database (PostgreSQL 16)

### A. Tabel `statement_imports` (Riwayat Batch Impor)
```sql
CREATE TABLE statement_imports (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    account_id UUID NOT NULL REFERENCES accounts(id) ON DELETE CASCADE,
    file_name VARCHAR(255) NOT NULL,
    bank_type VARCHAR(50) NOT NULL, -- 'bca', 'jago', 'seabank', 'generic'
    total_rows INT NOT NULL DEFAULT 0,
    imported_rows INT NOT NULL DEFAULT 0,
    skipped_duplicates INT NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_statement_imports_user ON statement_imports(user_id, created_at DESC);
```

### B. Modifikasi Tabel `transactions`
```sql
ALTER TABLE transactions 
ADD COLUMN statement_import_id UUID REFERENCES statement_imports(id) ON DELETE SET NULL,
ADD COLUMN raw_bank_description TEXT,
ADD COLUMN fingerprint_hash VARCHAR(64);

-- Mencegah duplikasi transaksi mutasi bank yang sama pada satu akun
CREATE UNIQUE INDEX idx_transactions_account_fingerprint 
ON transactions(account_id, fingerprint_hash) 
WHERE fingerprint_hash IS NOT NULL AND deleted_at IS NULL;
```

### C. Tabel `merchant_category_rules` (Aturan Kategorisasi Otomatis)
```sql
CREATE TABLE merchant_category_rules (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    pattern VARCHAR(100) NOT NULL, -- Contoh: '%INDOMARET%', '%PLN%'
    category_id UUID NOT NULL REFERENCES categories(id) ON DELETE CASCADE,
    priority INT NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_user_pattern UNIQUE(user_id, pattern)
);
```

---

## 6. Formula Deduplikasi (Transaction Fingerprint Hash)

$$\text{Fingerprint} = \text{SHA256}(\text{account\_id} \parallel \text{normalized\_date} \parallel \text{amount} \parallel \text{normalized\_desc} \parallel \text{balance\_after})$$

* **Normalisasi Tanggal:** `YYYY-MM-DD`.
* **Normalisasi Deskripsi:** Hapus spasi berlebih, ubah ke huruf kecil (*lowercase*), dan buang noise perbankan seperti `M-BCA`, `TRSF`, `DB`, `CR`.
* **Saldo Akhir (`balance_after`):** Pembeda mutlak jika ada transaksi dengan nominal dan tanggal persis sama.

---

## 7. Arsitektur Backend Go (Clean Architecture Layout)

```
internal/
├── core/
│   ├── domain/
│   │   ├── statement.go             # Entitas ParsedStatement, StatementRow
│   │   └── errors.go                # ErrUnsupportedBankFormat, ErrProSubscriptionRequired
│   ├── ports/
│   │   └── inbound.go               # StatementUseCase Interface (Check PRO tier quota)
│   └── usecase/
│       ├── parse_statement.go       # Parsing file & deduplikasi
│       └── commit_statement.go      # Bulk atomic ledger insert & balance update
└── adapter/
    ├── inbound/http/
    │   └── statement_handler.go     # Chi router: /accounts/{id}/statements/*
    └── statement_parsers/           # Strategy Pattern Parsers (BCA, Jago, SeaBank)
```

---

## 8. Endpoint Spesifikasi REST API

### 1. `POST /api/v1/accounts/{id}/statements/parse` (Tahap Pratinjau)
* **Validasi Tier:** Middleware memeriksa apakah user memiliki status `is_pro == true` atau kuota Free bulanan masih tersedia. Jika habis, kembalikan `403 PRO_SUBSCRIPTION_REQUIRED`.
* **Response `200 OK`:** Mengembalikan daftar baris transaksi, status duplikat, dan tebakan kategori.

### 2. `POST /api/v1/accounts/{id}/statements/commit` (Tahap Simpan)
* **Deskripsi:** Menyimpan baris yang dipilih user ke dalam database transaksi secara atomik (*within ACID database transaction*) dan memperbarui saldo rekening.

---

## 9. Desain Kepercayaan Pengguna & Microcopy (Trust Design)

Pada antarmuka modal unggah file, cantumkan *microcopy* keamanan untuk menepis keraguan privasi:
> 🛡️ **Privasi & Keamanan Data Anda**
> * File CSV hanya diproses secara instan untuk membaca transaksi dan **langsung dihapus dari memori**.
> * SpendWise tidak pernah menyimpan dokumen mutasi asli Anda.
> * Data keuangan bersifat privat, terenkripsi, dan tidak pernah dibagikan ke pihak ketiga manapun.

---

## 10. Langkah-Langkah Pengerjaan (Milestone Implementation)

| Tahap | Modul Pekerjaan | Target Deliverable |
|:---|:---|:---|
| **Sprint 1** | **Database Migration & Pro Tier Check** | Skema `statement_imports`, kolom `fingerprint_hash`, dan validasi kuota Free vs Pro. |
| **Sprint 2** | **Parsers & Deduplication Engine** | Implementasi `BCAParser`, `JagoParser`, dan `GenericCSVParser` di backend. |
| **Sprint 3** | **API Handlers & Auto-Categorizer** | Endpoint `/statements/parse` & `/statements/commit` terintegrasi dengan transactional unit-of-work. |
| **Sprint 4** | **Frontend UI & Staging Table** | Komponen Dropzone, review table, penanda duplikat, dan paywall modal untuk Free tier. |
| **Sprint 5** | **Uji QA & Deployment** | Pengujian dengan file CSV nyata dan rilis ke `spendwise.rikala.id`. |
