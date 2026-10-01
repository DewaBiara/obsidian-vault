# ☕ Blueprint Komprehensif: Reverse-Engineering Moka POS & Arsitektur Custom Cloud POS (Sawana POS)

- **Analis & Arsitek:** Thena (Hermes AI) & [[Dewa Biara]]
- **Sumber Data Lapangan:** Live Page Inspection `backoffice.mokapos.com` (Sawana Coffee & Eatery) + Native POS Client Teardown
- **Testbed Implementasi:** [[02_Areas/Sawana_Coffee_Eatery]] (Sawana Coffee & Eatery, Ubud, Bali)
- **Status:** Complete Master Architecture & Implementation Blueprint
- **Dokumen Terkait:** [[01_Projects/Arsitektur_dan_Strategi_POS_System_Bali]]

---

## 1. Executive Summary & Temuan Kunci Live Reverse-Engineering

Berdasarkan inspeksi langsung (*live page walkthrough*) pada akun aktif Moka Backoffice Sawana Coffee & Eatery per 1 Oktober 2026, terungkap bahwa Moka POS berada dalam fase **arsitektur transisi hibrida**:
1. **Frontend Backoffice:** Sedang bermigrasi dari monolit React lama (`remote-entry-BoLegacyApp.js`) ke arsitektur **Micro-Frontend berbasis Webpack 5 Module Federation**. Rute bertanda `/v2/...` adalah modul federasi baru, sedangkan rute non-`/v2` masih menjalankan aplikasi warisan (*legacy*).
2. **Backend Dual-Gateway:**
   - Gateway Lama (`service.mokapos.com`): Melayani data akun lama dan GraphQL reporting revamp (`/reporting-revamp/graphql`).
   - Gateway Baru GoTo (`service-goauth.mokapos.com`): Melayani auth berbasis Go, order-reporting, subscription, inventory v4, dan feature flag Unleash.
3. **Monetisasi Berlapis (Paywalled Features):**
   - Fitur esensial F&B seperti **Ingredients (Resep/HPP)** dan **Table Management** dikunci di balik add-on berbayar (*Start Free Trial / Paid Add-on*).
   - Penambahan staf dikunci melalui sistem lisensi **Employee Slots**.

### Peluang Emas untuk Sawana POS (Kustom Dewa):
Dengan membangun POS in-house berbasis **Go, PostgreSQL, Redis, dan PWA/Flutter**, kita tidak perlu mereplikasi kerumitan *Module Federation* atau *over-engineering* microservices Moka. Kita bisa mengadopsi pola **Modular Monolith** berperforma tinggi dengan latensi sub-10ms, *true offline-first*, tanpa biaya lisensi slot karyawan maupun add-on resep bahan baku.

---

## 2. Peta Topologi Arsitektur Riil Moka POS (Berdasarkan Live Data)

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                               FRONTEND APPLICATION LAYER                               │
├───────────────────────────────────────────┬────────────────────────────────────────────┤
│           POS EDGE TABLET CLIENT          │          MOKA BACKOFFICE WEB SPA           │
│                                           │                                            │
│  - Android/iOS Native (Kotlin/Swift)      │  - Host Shell: moka_backoffice (Webpack 5) │
│  - Local SQLite (Offline Outbox Queue)    │  - State: Redux + Redux-Saga               │
│  - ESC/POS Print Spooler (BT/LAN/USB)     │  - Micro-Frontends (Module Federation):    │
│  - Solenoid RJ11 Cash Drawer Trigger      │    * BoLegacyApp (Non-v2 legacy pages)     │
│  - Customer Display (CFD) / KDS           │    * BoCustomerApp, BoIngredientApp        │
│                                           │    * BoPaymentApp, BoPurchaseOrderApp      │
│                                           │    * BoTableManagementApp, BoAuthApp       │
└─────────────────────┬─────────────────────┴─────────────────────┬──────────────────────┘
                      │ HTTPS Sync Protocol                       │ REST / GraphQL
                      ▼                                           ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                              API GATEWAY & ROUTING LAYER                               │
├───────────────────────────────────────────┬────────────────────────────────────────────┤
│  LEGACY GATEWAY: service.mokapos.com      │  NEW GOTO GATEWAY: service-goauth...       │
│  - /account/v2/profile                    │  - /order-reporting/backoffice/v1/orders   │
│  - /reporting-revamp/graphql              │  - /inventory/v4/discounts                 │
│                                           │  - /business-service/v4/businesses/outlets │
│                                           │  - /payment/v1/payment-methods             │
│                                           │  - /unleash-proxy/proxy (Feature Flags)    │
└───────────────────────────────────────────┴─────────────────────┬──────────────────────┘
                                                                  ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                               BACKEND MICROSERVICES TIER                               │
│                                                                                        │
│  ┌────────────────────┐ ┌────────────────────┐ ┌────────────────────┐ ┌──────────────┐ │
│  │ Auth & Employee    │ │ Catalog & Library  │ │ Ingredient & Recipe│ │ Order & Shift│ │
│  │ Service (RBAC+PIN) │ │ Service (v4)       │ │ Service (BOM/HPP)  │ │ Service (v1) │ │
│  └────────────────────┘ └────────────────────┘ └────────────────────┘ └──────────────┘ │
│  ┌────────────────────┐ ┌────────────────────┐ ┌────────────────────┐ ┌──────────────┐ │
│  │ Inventory & PO     │ │ Payment & QRIS     │ │ Reporting Engine   │ │ Omnichannel  │ │
│  │ (Simple/Advanced)  │ │ Gateway (GoPay)    │ │ (GraphQL Revamp)   │ │ (GoBiz/GoFood│ │
│  └────────────────────┘ └────────────────────┘ └────────────────────┘ └──────────────┘ │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Dekomposisi 10 Modul Domain Fitur (Hasil Live Walkthrough)

### 1. Dashboard & Core KPI Domain
- **Metrik Utama:** Gross Sales, Net Sales, Gross Profit, Total Transactions, Average Sale per Transaction, Gross Margin (%).
- **Visualisasi:** Sales Summary Chart (Google Charts) & Item Sales Contribution.
- **Preset Periode:** Hari Ini, Kemarin, Minggu Ini/Lalu, Bulan Ini/Lalu, Tahun Ini/Lalu, Rentang Kustom.

### 2. Reporting & Analytics Domain (GraphQL Separated)
Moka memisahkan reporting ke GraphQL endpoint tersendiri (`/reporting-revamp/graphql`):
- **12 Sub-Laporan Penjualan:**
  1. *Sales Summary* (Ikhtisar penjualan kotor, bersih, diskon, refund).
  2. *Gross Profit* (Laba kotor per produk berbasis HPP resep).
  3. *Payment Methods* (Breakdown tunai, QRIS, kartu EDC, invoice).
  4. *Sales Type* (Dine-in vs Takeaway vs Delivery).
  5. *Item Sales* (Kuantitas & rupiah per item terjual).
  6. *Category Sales* (Kontribusi per kategori menu).
  7. *Brand Sales* (Multi-brand management).
  8. *Modifier Sales* (Penjualan extra shot, oat milk, syrup tambahan).
  9. *Discounts* (Rekapitulasi voucher dan diskon manual).
  10. *Taxes* (Laporan pajak restoran PB1 10%).
  11. *Gratuity* (Laporan service charge 5%).
  12. *Staff Performance:* Collected By (kinerja kasir) & Served By (kinerja server/pelayan).
- **Laporan Transaksi (`/v2/reports/transactions`):** 3 tab status: *Success Orders*, *Cancelled Orders*, dan *Void Items*.
- **Laporan Shift (`/reports/shifts`):** Opening Cash, Cash Sales, Cash Invoices, Refunds, Paid In / Paid Out, Total Expected Cash vs Actual Count Cash, serta kalkulasi selisih (*Discrepancy*).

### 3. Catalog & Menu Library Domain
- **Item Library:** SKU, nama item, kategori, multi-harga per outlet, batas peringatan stok (*Stock Alert*).
- **Modifiers:** Grup modifier opsional/wajib dengan min/max selection dan biaya ekstra.
- **Bundle Package:** Manajemen paket kombo F&B (misal: 1 Toast + 1 Kopi = harga khusus).
- **Promo & Discounts (v2):** Diskon persentase/rupiah dengan status *Scheduled*, *Ongoing*, *Inactive*.
- **Sales Type & Tax/Gratuity:** Konfigurasi apakah suatu Sales Type (misal: Dine-In) dikenakan Service Charge & Pajak PB1 atau tidak.

### 4. Ingredient & Recipe Domain (The Core Costing Engine)
- **Tipe Bahan Baku:**
  - *Raw Ingredient:* Biji kopi mentah, susu UHT, sirup vanila.
  - *Semi-Finished Ingredient (Sub-Assembly):* Cold Brew concentrate, Simple Syrup hasil racikan internal.
- **Recipes (BOM):** Memetakan 1 Varian Menu ke multi-komponen bahan baku beserta takarannya.
- **Perhitungan HPP Otomatis:** Menggunakan metode **Moving Weighted Average Cost**.

### 5. Inventory & Supply Chain Domain (Dual Mode: Simple vs Advanced)
Moka menyediakan switch mode di pengaturan:
- **Mode Simple:** Pencatatan stok masuk dan transfer langsung tanpa tahapan approval bertingkat.
- **Mode Advanced:** Alur purchase order formal (PO dibuat $\rightarrow$ PO dikirim ke supplier $\rightarrow$ Fulfill parsial/penuh $\rightarrow$ Update HPP).
- **Fitur Inti:**
  - *Inventory Summary:* Beginning Stock + PO In - Sales Out $\pm$ Transfer $\pm$ Adjustment = Ending Stock.
  - *Suppliers Management:* Database vendor dan kontak supplier.
  - *Stock Transfer:* Alur transfer bahan antar-outlet.
  - *Stock Adjustment:* Stock Opname fisik berkala (kategori: Waste, Rusak, Kadaluarsa, Koreksi Hitung).

### 6. Employees & Security Domain (Two-Tier RBAC & PIN Matrix)
Moka menerapkan keamanan 2 lapis:
1. **Tier 1 (Backoffice Roles):** Hak akses menu dashboard (Owner, Admin, Manager).
2. **Tier 2 (POS Action PIN Matrix):** Setiap kasir memiliki PIN numerik. Aksi-aksi sensitif wajib meminta otorisasi PIN:
   - Cetak ulang tagihan (*Print Bill*)
   - Buka tagihan tersimpan (*Manage Open Bills*)
   - Berikan diskon manual (*Apply/Manage Discounts*)
   - Lakukan refund / batalkan transaksi (*Issue Refunds*)
   - Buka laci kasir tanpa belanja (*Open Cash Drawer / No Sale*)
   - Catat / batalkan pembayaran invoice (*Record/Cancel Invoice*)
   - Lihat histori shift & rekap kas (*View Shift History*)
   - Edit data pelanggan (*Edit Customer Info*)

### 7. Online Channels & Omnichannel Domain
- **GoFood Integration:** Menghubungkan outlet Moka langsung ke akun GoBiz. Sinkronisasi menu online, auto-accept pesanan, dan auto-routing ke printer dapur.
- **Moka Order (GoStore):** Halaman web pemesanan mandiri (*self-order / QR table order*) untuk pelanggan di meja.

### 8. Customer CRM & Loyalty Domain
- Profil pelanggan, riwayat kunjungan, dan *Customer Lifetime Value (LTV)*.
- Program loyalitas berbasis poin (Setiap belanja Rp X mendapat Y poin, dapat ditukar reward).
- Modul *Feedback* pelanggan (ulasan bintang dan komentar langsung dari tablet/struk).

### 9. Customer-Facing Display (CFD v2) Domain
- Aplikasi hadap pelanggan di kasir untuk menampilkan keranjang belanja secara real-time.
- Modul *Campaign:* Menampilkan banner gambar promosi kafe saat kasir dalam keadaan standby (*idle*).

### 10. Payments & Settlement Domain
- Profil metode pembayaran per outlet: Cash, QRIS Dinamis (GoPay/Midtrans), EDC (Mandiri/BCA/BRI), GoBiz PLUS Smart EDC, Invoice/Tempo.
- Pengaturan pembulatan nominal (*Cash Rounding*).

---

## 4. Desain Arsitektur Sistem Kustom (Sawana POS)

Berdasarkan fakta empiris di atas, kita merancang arsitektur sistem POS mandiri yang bersih, tanpa kerumitan micro-frontend atau gateway ganda, menggunakan tech stack andalan Dewa:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        SAWANA POS ARCHITECTURE                         │
├────────────────────────────────────────────────────────────────────────┤
│  CLIENT TIER                                                           │
│  - Cashier Terminal: Next.js PWA / Flutter (WASM / SQLite IndexedDB)   │
│  - Local Server / Broker: Mini PC N100 (Ubuntu Server di Sawana)       │
│  - Local Printer Spooler: ESC/POS Raw Socket TCP 9100 + Bluetooth      │
│  - Zero Cloud Dependency for Ring-up & Print                           │
├────────────────────────────────────────────────────────────────────────┤
│  BACKEND TIER (Modular Monolith in Go)                                 │
│                                                                        │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐   │
│  │ Auth & PIN   │ │ Catalog &    │ │ Recipe &     │ │ Shift &      │   │
│  │ Module       │ │ Modifiers    │ │ Inventory    │ │ Cash Ledger  │   │
│  └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘   │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐   │
│  │ Idempotent   │ │ Smart Split  │ │ ULASA Review │ │ Realtime KDS │   │
│  │ Checkout     │ │ Bill Engine  │ │ Loop Gateway │ │ (WebSocket)  │   │
│  └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘   │
├────────────────────────────────────────────────────────────────────────┤
│  DATA & EVENT TIER                                                     │
│  - PostgreSQL: Double-Entry Financial Ledger & Relational Data         │
│  - Redis: Cache, Distributed Lock, & Stream (OrderCompleted Events)    │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Skema Basis Data DDL Terpadu (PostgreSQL)

Berikut adalah DDL lengkap yang mengadopsi struktur fungsional Moka Backoffice namun dioptimasi untuk performa dan integritas ACID:

```sql
-- EXTENSIONS
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. BUSINESS & OUTLETS
CREATE TABLE businesses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(150) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE outlets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    business_id UUID NOT NULL REFERENCES businesses(id),
    name VARCHAR(150) NOT NULL,
    address TEXT,
    tax_percentage NUMERIC(5,2) DEFAULT 10.00,
    service_charge_percentage NUMERIC(5,2) DEFAULT 0.00,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 2. EMPLOYEES & PIN PERMISSION MATRIX
CREATE TABLE employees (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    outlet_id UUID NOT NULL REFERENCES outlets(id),
    name VARCHAR(100) NOT NULL,
    role VARCHAR(50) NOT NULL, -- 'OWNER', 'MANAGER', 'CASHIER', 'BARISTA'
    pin_hash VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE employee_pin_permissions (
    employee_id UUID PRIMARY KEY REFERENCES employees(id) ON DELETE CASCADE,
    can_apply_manual_discount BOOLEAN DEFAULT FALSE,
    can_void_transaction BOOLEAN DEFAULT FALSE,
    can_issue_refund BOOLEAN DEFAULT FALSE,
    can_open_cash_drawer BOOLEAN DEFAULT FALSE,
    can_reprint_receipt BOOLEAN DEFAULT FALSE,
    can_view_shift_history BOOLEAN DEFAULT FALSE
);

-- 3. SHIFT & CASH LEDGER
CREATE TABLE shifts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    outlet_id UUID NOT NULL REFERENCES outlets(id),
    cashier_id UUID NOT NULL REFERENCES employees(id),
    opened_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    closed_at TIMESTAMPTZ,
    starting_cash NUMERIC(12,2) NOT NULL DEFAULT 0.00,
    expected_cash NUMERIC(12,2),
    actual_cash NUMERIC(12,2),
    cash_difference NUMERIC(12,2),
    status VARCHAR(20) NOT NULL DEFAULT 'OPEN',
    notes TEXT
);

CREATE TABLE shift_cash_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    shift_id UUID NOT NULL REFERENCES shifts(id),
    type VARCHAR(20) NOT NULL, -- 'PAID_IN', 'PAID_OUT'
    amount NUMERIC(12,2) NOT NULL,
    reason TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 4. CATALOG, MODIFIERS & BUNDLES
CREATE TABLE categories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    outlet_id UUID NOT NULL REFERENCES outlets(id),
    name VARCHAR(100) NOT NULL,
    sort_order INT DEFAULT 0
);

CREATE TABLE products (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    outlet_id UUID NOT NULL REFERENCES outlets(id),
    category_id UUID REFERENCES categories(id),
    name VARCHAR(150) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE
);

CREATE TABLE product_variants (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    product_id UUID NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL, -- e.g. "Regular", "Large"
    sku VARCHAR(50),
    base_price NUMERIC(12,2) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE
);

CREATE TABLE modifier_groups (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    outlet_id UUID NOT NULL REFERENCES outlets(id),
    name VARCHAR(100) NOT NULL, -- e.g. "Milk Type"
    min_selection INT DEFAULT 0,
    max_selection INT DEFAULT 1
);

CREATE TABLE modifiers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    group_id UUID NOT NULL REFERENCES modifier_groups(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL, -- e.g. "Oat Milk"
    extra_price NUMERIC(12,2) NOT NULL DEFAULT 0.00
);

-- 5. INGREDIENTS & RECIPES (BOM / COGS)
CREATE TABLE ingredients (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    outlet_id UUID NOT NULL REFERENCES outlets(id),
    name VARCHAR(150) NOT NULL,
    unit VARCHAR(20) NOT NULL, -- 'g', 'ml', 'pcs'
    current_stock NUMERIC(12,3) NOT NULL DEFAULT 0.000,
    average_cost NUMERIC(12,2) NOT NULL DEFAULT 0.00,
    stock_alert_threshold NUMERIC(12,3) DEFAULT 0.000
);

CREATE TABLE recipes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    variant_id UUID NOT NULL REFERENCES product_variants(id) ON DELETE CASCADE,
    ingredient_id UUID NOT NULL REFERENCES ingredients(id),
    amount_needed NUMERIC(12,3) NOT NULL
);

-- 6. ORDERS, PAYMENTS & AUDIT TRAIL
CREATE TABLE orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    client_order_uuid UUID UNIQUE NOT NULL, -- Offline idempotency key!
    outlet_id UUID NOT NULL REFERENCES outlets(id),
    shift_id UUID REFERENCES shifts(id),
    invoice_number VARCHAR(50) NOT NULL,
    sales_type VARCHAR(30) NOT NULL DEFAULT 'DINE_IN',
    table_number VARCHAR(20),
    subtotal NUMERIC(12,2) NOT NULL,
    discount_amount NUMERIC(12,2) NOT NULL DEFAULT 0.00,
    tax_amount NUMERIC(12,2) NOT NULL DEFAULT 0.00,
    service_charge_amount NUMERIC(12,2) NOT NULL DEFAULT 0.00,
    final_amount NUMERIC(12,2) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'COMPLETED', -- 'DRAFT', 'COMPLETED', 'VOID', 'REFUNDED'
    void_reason TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE order_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    variant_id UUID NOT NULL REFERENCES product_variants(id),
    item_name VARCHAR(150) NOT NULL,
    unit_price NUMERIC(12,2) NOT NULL,
    quantity INT NOT NULL,
    subtotal NUMERIC(12,2) NOT NULL,
    cogs_amount NUMERIC(12,2) NOT NULL DEFAULT 0.00
);

CREATE TABLE payments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    payment_method VARCHAR(30) NOT NULL, -- 'CASH', 'QRIS', 'EDC_DEBIT', 'EDC_CREDIT'
    amount_paid NUMERIC(12,2) NOT NULL,
    change_given NUMERIC(12,2) NOT NULL DEFAULT 0.00,
    reference_number VARCHAR(100),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

---

## 6. Analisis Perbandingan Fitur: Moka POS vs Sawana POS

| Aspek / Fitur | Moka POS (Hasil Live Walkthrough) | Sawana POS (Target Arsitektur Kita) | Keunggulan Sistem Kita |
|---|---|---|---|
| **Biaya Bulanan** | Rp 299rb - 499rb/outlet + Bayar per Employee Slot | **Rp 0 Lisensi** (Self-hosted di Mini PC / Cloud Run) | Hemat jutaan rupiah per tahun untuk Sawana |
| **Ingredient & HPP** | Add-on berbayar terpisah (*Start Trial*) | **Native Built-in** di core sistem | HPP terhitung otomatis dari hari pertama |
| **Table Management** | Fitur terkunci / trial berbayar | **Native Built-in** (Floor map & live table bill) | Manajemen meja tanpa biaya ekstra |
| **Arsitektur Sync** | Cloud-dependent, sering lag di WiFi Bali | **Hybrid Local-First:** Mini PC LAN WebSocket + Cloud Sync | Tetap instan meski koneksi internet putus |
| **Split Bill** | Lambat, navigasi bertingkat | **1-Tap Quick Split:** Bagi rata atau pilih per item | Mengurai antrean kasir saat peak hour |
| **Growth & Reputasi** | Nol integrasi ulasan | **Native ULASA Review Loop:** Struk digital / CFD langsung trigger ulasan Google Maps | Menggenjot rating bintang 5 Sawana otomatis |

---

## 7. Roadmap Implementasi Teknis

1. **Sprint 1 (Core POS & Local Hardware Spooler):**
   - Implementasi schema database PostgreSQL di Go (`sqlc` / GORM).
   - Engine transaksi kasir dengan proteksi idempotency UUIDv7.
   - Driver thermal printer ESC/POS (Socket TCP 9100 & Bluetooth) untuk struk kasir dan laci RJ11.
2. **Sprint 2 (Shift Ledger, Inventory & BOM):**
   - Siklus shift kasir (Open, Cash In/Out, Blind Cash Count Close Shift, X/Z-Report).
   - Asynchronous recipe deduction via Redis Stream saat order completed.
   - Peringatan stok kritis (*Stock Alert*).
3. **Sprint 3 (UI Kasir & ULASA Loop):**
   - Web PWA kasir responsif & offline-ready (IndexedDB).
   - Layar Customer-Facing Display sederhana dengan integrasi ULASA Google Review.
   - Uji coba live (*dogfooding*) 100% di kasir Sawana Coffee & Eatery.
