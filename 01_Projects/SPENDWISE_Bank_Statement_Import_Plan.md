# RENCANA IMPLEMENTASI (IMPLEMENTATION PLAN)
## FITUR IMPORT MUTASI REKENING (BANK STATEMENT IMPORT)
### Platform SpendWise (`https://spendwise.rikala.id`)

> **Versi Dokumen:** 1.0  
> **Tanggal:** 11 Oktober 2026  
> **Status:** Draft Arsitektur & Spesifikasi Teknis  
> **Arsitektur:** Strict Clean Architecture (Go 1.22+) & Next.js 14+ (App Router)  

---

## 1. Latar Belakang & Tujuan (Objective)

Pencatatan manual satu-per-satu (*manual bookkeeping*) merupakan titik friksi terbesar yang menyebabkan pengguna berhenti menggunakan aplikasi keuangan. Mengingat API Open Banking / agregator komersial di Indonesia mahal dan memerlukan perizinan kompleks, fitur **Import Mutasi Rekening (CSV / e-Statement)** adalah solusi strategis terbaik.

### Sasaran Utama:
1. **Zero Friction Onboarding:** Pengguna dapat memasukkan 100+ transaksi bulanan dalam hitungan detik.
2. **Deduplikasi 100% Akurat:** Transaksi yang diimpor berulang kali tidak boleh menggandakan saldo ledger (*idempotent import*).
3. **Privasi & Keamanan Penuh:** Pengguna tidak menyerahkan kredensial login perbankan mereka.
4. **Auto-Categorization:** Sistem mampu menebak kategori transaksi secara cerdas berdasarkan pola deskripsi mutasi bank lokal.

---

## 2. Cakupan Format Bank (Bank Support Matrix)

### Fase 1 (Prioritas Utama — CSV Parser):
* **BCA (myBCA & KlikBCA Individu):** CSV format dengan kolom Tanggal, Keterangan, CB, Mutasi (DB/CR), Saldo.
* **Bank Jago:** CSV standar dengan kolom Tanggal Transaksi, Deskripsi, Tipe (Debit/Kredit), Jumlah, Kategori Bank.
* **SeaBank:** CSV export mutasi rekening tabungan.
* **Format Generic CSV:** Templat standar SpendWise (`date,type,amount,merchant,note,category`).

### Fase 2 (Pengembangan Lanjutan):
* **Bank Mandiri (Livin' by Mandiri):** CSV dan PDF e-Statement.
* **Bank BRI (BRImo):** CSV / PDF.
* **OCR / PDF Parser:** Ekstraksi e-Statement resmi bertanda tangan digital.

---

## 3. Desain Skema Database (PostgreSQL 16)

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
Tambahkan kolom identitas unik mutasi (*cryptographic fingerprint*) agar transaksi duplikat otomatis terdeteksi:
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
    pattern VARCHAR(100) NOT NULL, -- Contoh: '%INDOMARET%', '%PLN%', '%SAWANA%'
    category_id UUID NOT NULL REFERENCES categories(id) ON DELETE CASCADE,
    priority INT NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_user_pattern UNIQUE(user_id, pattern)
);
```

---

## 4. Formula Deduplikasi (Transaction Fingerprint Hash)

Untuk mendeteksi apakah baris mutasi perbankan sudah pernah diimpor sebelumnya, backend Go menghitung hash SHA-256 deterministik untuk setiap baris mutasi:

$$\text{Fingerprint} = \text{SHA256}(\text{account\_id} \parallel \text{normalized\_date} \parallel \text{amount} \parallel \text{normalized\_desc} \parallel \text{balance\_after})$$

* **Normalisasi Tanggal:** `YYYY-MM-DD` (mengabaikan perbedaan zona waktu saat ekspor).
* **Normalisasi Deskripsi:** Hapus spasi berlebih, ubah ke huruf kecil (*lowercase*), dan buang noise perbankan seperti `M-BCA`, `TRSF`, `E-BANKING`, `DB`, `CR`.
* **Saldo Akhir (`balance_after`):** Menjadi pembeda mutlak jika ada 2 transaksi dengan nominal dan tanggal persis sama (misal beli 2 kopi harga sama di hari yang sama).

---

## 5. Arsitektur Backend Go (Clean Architecture Layout)

```
internal/
├── core/
│   ├── domain/
│   │   ├── statement.go             # Entitas ParsedStatement, StatementRow, BankType
│   │   └── errors.go                # ErrUnsupportedBankFormat, ErrInvalidStatement
│   ├── ports/
│   │   ├── inbound.go               # StatementUseCase Interface
│   │   └── outbound.go              # StatementRepository, TransactionRepository
│   └── usecase/
│       ├── parse_statement.go       # Parsing file, deteksi duplikat, tebak kategori
│       └── commit_statement.go      # Bulk atomic ledger insert & balance update
└── adapter/
    ├── inbound/http/
    │   └── statement_handler.go     # Chi router handler: /accounts/{id}/statements/*
    └── statement_parsers/           # Strategy Pattern Parsers
        ├── parser.go                # Interface StatementParser
        ├── bca_parser.go            # Parser khusus CSV myBCA / KlikBCA
        ├── jago_parser.go           # Parser khusus CSV Bank Jago
        └── generic_parser.go        # Parser CSV universal
```

### Interface Parser di Go (Strategy Pattern):
```go
package domain

import (
    "io"
    "time"
)

type StatementRow struct {
    Date            time.Time
    Amount          int64     // Positif = pemasukan, Negatif = pengeluaran
    RawDescription  string
    Merchant        string
    SuggestedCatID  *string
    BalanceAfter    int64
    FingerprintHash string
    IsDuplicate     bool
}

type StatementParser interface {
    BankCode() string
    Detect(headerLine string) bool
    Parse(r io.Reader, accountID string) ([]StatementRow, error)
}
```

---

## 6. Endpoint Spesifikasi REST API

### 1. `POST /api/v1/accounts/{id}/statements/parse` (Tahap Pratinjau / Preview)
* **Deskripsi:** Menerima file multipart `statement_file`, membaca baris data, mendeteksi duplikat terhadap database, dan menebak kategori. **Belum menulis ke database ledger.**
* **Header:** `Content-Type: multipart/form-data`, `Authorization: Bearer <token>`
* **Response `200 OK`:**
  ```json
  {
    "bank_detected": "bca",
    "total_rows": 24,
    "new_rows_count": 21,
    "duplicate_rows_count": 3,
    "rows": [
      {
        "row_id": "temp-01",
        "date": "2026-10-10",
        "amount": -45000,
        "raw_description": "QRIS SAID COFFEE UBUD",
        "merchant": "Said Coffee Ubud",
        "suggested_category_id": "01a128d1-b6eb-774d-8fae-82a694192cb3",
        "suggested_category_name": "Makanan & Kopi",
        "fingerprint_hash": "a8fbc839...",
        "is_duplicate": false
      },
      {
        "row_id": "temp-02",
        "date": "2026-10-09",
        "amount": -250000,
        "raw_description": "TRSF E-BANKING DB PLN PRABAYAR",
        "merchant": "PLN Prabayar",
        "suggested_category_id": "01a128d3-1298-7a73-b875-092e0ec53e0c",
        "suggested_category_name": "Tagihan & Utilitas",
        "fingerprint_hash": "b47c012d...",
        "is_duplicate": true
      }
    ]
  }
  ```

---

### 2. `POST /api/v1/accounts/{id}/statements/commit` (Tahap Simpan / Commit)
* **Deskripsi:** Menyimpan baris yang dipilih user ke dalam database transaksi secara atomik (*within ACID database transaction*) dan memperbarui saldo rekening.
* **Request Body:**
  ```json
  {
    "file_name": "mutasi_bca_oktober.csv",
    "bank_type": "bca",
    "items": [
      {
        "fingerprint_hash": "a8fbc839...",
        "date": "2026-10-10",
        "amount": -45000,
        "merchant": "Said Coffee Ubud",
        "category_id": "01a128d1-b6eb-774d-8fae-82a694192cb3",
        "note": "Imported from BCA",
        "raw_description": "QRIS SAID COFFEE UBUD"
      }
    ]
  }
  ```
* **Response `201 Created`:**
  ```json
  {
    "import_id": "01a128e0-1122-77aa-bb33-ccaabb112233",
    "imported_count": 21,
    "new_account_balance": 9677500
  }
  ```

---

## 7. Desain Alur Pengguna & Tampilan UI/UX (Frontend Next.js)

### Komponen 1: Modal "Import Mutasi Rekening"
* Tombol aksi baru di halaman Akun detail: `[+] Impor Mutasi`.
* Dropzone unggah file drag-and-drop dengan filter ekstensi `.csv`.
* Panduan singkat ekspor: *"Buka myBCA / Livin / Jago -> Mutasi Rekening -> Download CSV"*.

### Komponen 2: Interactive Staging & Review Table
* Menampilkan tabel transaksi sebelum disimpan:
  * **Kolom Checkbox:** Baris duplikat otomatis di-uncheck dengan label badge abu-abu: *"Sudah ada"*.
  * **Kolom Tanggal & Nominal:** Warna merah untuk pengeluaran, hijau untuk pemasukan.
  * **Kolom Merchant & Kategori:** Dropdown inline yang memungkinkan user mengganti kategori jika tebakan sistem salah.
* **Sticky Bottom Bar:**
  * Informasi ringkasan: *"21 transaksi baru dipilih (Total Pengeluaran: Rp 1.450.000, Pemasukan: Rp 8.000.000)"*.
  * Tombol konfirmasi: `[Impor 21 Transaksi Sekarang]`.

---

## 8. Langkah-Langkah Pengerjaan (Milestone Implementation)

| Tahap | Modul Pekerjaan | Target Deliverable |
|:---|:---|:---|
| **Sprint 1** | **Database Migration & Domain Modeling** | Skema `statement_imports`, kolom `fingerprint_hash` di `transactions`, dan entitas domain Go. |
| **Sprint 2** | **Parsers & Deduplication Engine** | Implementasi `BCAParser`, `JagoParser`, dan `GenericCSVParser` di backend beserta unit test deduplikasi hash. |
| **Sprint 3** | **API Handlers & Auto-Categorizer** | Endpoint `/statements/parse` & `/statements/commit` terintegrasi dengan transactional unit-of-work. |
| **Sprint 4** | **Frontend UI & Staging Table** | Pembuatan komponen Dropzone, parsing feedback, dan tabel interaktif di halaman `/akun/[id]`. |
| **Sprint 5** | **Uji QA & Deployment** | Pengujian dengan file CSV nyata (myBCA, Jago) dan rilis produksi ke `spendwise.rikala.id`. |

---

## 9. Pertimbangan Keamanan & Validasi (Security Checklist)

1. **Batas Ukuran Berkas:** Maksimal ukuran file CSV dibatasi 5 MB per upload untuk mencegah serangan DoS memori.
2. **Validasi MIME Type & Sanitasi Karakter:** Memeriksa header berkas `text/csv` / `text/plain` dan membersihkan karakter injeksi CSV (`=`, `+`, `-`, `@` pada awal teks) untuk mencegah formula injection saat diekspor kembali.
3. **Isolasi Akun (Multi-Tenant Scoping):** Endpoint verifikasi memastikan `account_id` wajib milik `user_id` yang terotentikasi.
4. **Idempotent Batch Commit:** Jika user secara tidak sengaja mengklik tombol commit dua kali, `UNIQUE INDEX` pada `(account_id, fingerprint_hash)` akan menangkal duplikasi di level database.
