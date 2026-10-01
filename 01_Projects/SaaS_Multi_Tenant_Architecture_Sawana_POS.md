# 🏢 TRANSISI KE MULTI-TENANT SAAS: DAMPAK ARSITEKTUR & DESAIN SISTEM

- **Inisiator:** [[Dewa Biara]]
- **Topik:** Transformasi Sawana POS dari Single-Store Internal ke B2B Multi-Tenant F&B SaaS
- **Tautan Terkait:** [[01_Projects/CLAUDE_CODE_SAWANA_POS_SPEC]] | [[01_Projects/Riset_Arsitektur_MokaPOS_dan_Desain_Sistem_POS]]

---

## 1. Perubahan Paradigma: Single-Store vs B2B Multi-Tenant SaaS

Ketika sistem POS diubah dari konsumsi internal (Sawana Coffee) menjadi platform SaaS komersial untuk ratusan restoran/kafe, terjadi pergeseran mendasar pada **5 layer arsitektur**:

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           B2B MULTI-TENANT POS SAAS                             │
├─────────────────────────────────────────────────────────────────────────────────┤
│  1. TENANT ISOLATION LAYER                                                      │
│     JWT Claims: { user_id, business_id, outlet_id, role, plan }                 │
│     PostgreSQL: Row-Level Security (RLS) / Tenant-Scoped Middleware             │
├─────────────────────────────────────────────────────────────────────────────────┤
│  2. DEVICE PROVISIONING & LICENSING                                             │
│     Backoffice generates 6-digit Pairing Code -> Tablet exchanges for Device JWT│
│     Control active registers per plan (e.g. 1 Tablet included, +50k/extra)      │
├─────────────────────────────────────────────────────────────────────────────────┤
│  3. CLIENT HARDWARE INDEPENDENCE (ZERO LOCAL SERVER ASSUMPTION)                 │
│     Restoran lain TIDAK punya Mini PC. Printing wajib 100% Client-Driven:        │
│     * Android/iOS App -> Direct Bluetooth SPP / Raw TCP Socket ke Printer LAN  │
│     * Web PWA -> Web Bluetooth API / Web Serial API                             │
├─────────────────────────────────────────────────────────────────────────────────┤
│  4. BILLING & SUBSCRIPTION ENGINE                                               │
│     Plans: Starter (1 Outlet, 1 Reg), Growth (Multi-Outlet), Enterprise         │
│     Automated Billing: Midtrans / Xendit Recurring Payment / E-Invoice VA       │
├─────────────────────────────────────────────────────────────────────────────────┤
│  5. NOISY NEIGHBOR & MULTI-TENANT EVENT PIPELINE                                │
│     Redis Rate Limiter per Tenant (Token Bucket by business_id)                 │
│     Dynamic Payment Gateway Credential Injection (Platform QRIS vs Custom MID)  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Dampak Detail per Komponen Arsitektur

### A. Strategi Database: Shared Database, Shared Schema + PostgreSQL RLS
Untuk SaaS F&B dengan target efisiensi biaya infrastruktur (GCP Cloud Run + Cloud SQL / Managed Postgres):
- **JANGAN** gunakan Database-per-tenant (terlalu mahal, ribet migrasi 100 DB).
- **GUNAKAN:** Shared Database dengan kolom `business_id` wajib di setiap tabel transaksional, dilindungi oleh **PostgreSQL Row-Level Security (RLS)** atau Context Middleware di Go.
- **Mekanisme di Go:**
  Setiap request masuk membawa JWT berisi `business_id`. Middleware Go meng-inject nilai ini ke SQL session:
  ```go
  // Middleware set tenant session
  tx.Exec(ctx, "SET LOCAL app.current_business_id = $1", claims.BusinessID)
  ```
  Dan policy database otomatis membatasi:
  ```sql
  CREATE POLICY tenant_isolation_policy ON orders
  USING (business_id = current_setting('app.current_business_id')::uuid);
  ```

### B. Device Pairing Flow (Registrasi Tablet Kasir Baru)
Di sistem internal, kasir bisa langsung login akun. Di sistem SaaS, pemilik resto ingin membatasi jumlah tablet kasir yang aktif sesuai paket langganan:
1. Owner membuka Backoffice web $\rightarrow$ Menu *Registers & Devices* $\rightarrow$ Klik *Tambah Kasir Meja 1*.
2. Backoffice menghasilkan **6-Digit Pairing Code** (berlaku 10 menit), misal: `849-201`.
3. Kasir mengunduh aplikasi POS di tablet baru $\rightarrow$ Buka aplikasi $\rightarrow$ Masukkan kode `849-201`.
4. Tablet menukar kode tersebut ke server dan menerima `device_token` permanen yang terikat ke `(business_id, outlet_id, register_id)`.
5. Jika pemilik resto memutus akses dari Backoffice (*Revoke Device*), tablet kasir seketika logout otomatis.

### C. Abstraksi Hardware Tanpa Ketergantungan Mini PC
Di Sawana, kamu bisa meletakkan Mini PC sebagai local server. Tapi resto klien di Canggu/Seminyak tidak memiliki server lokal.
- **Arsitektur Printer Harus 100% Client-Side:**
  - Tablet kasir berkomunikasi langsung ke printer melalui **Bluetooth** atau **TCP Socket IP lokal subnet kafe** (Port 9100).
  - Byte generator ESC/POS dijalankan langsung di sisi client (JavaScript/WASM atau Dart Flutter), bukan di cloud server.
  - Dengan cara ini, cloud backend sama sekali tidak perlu memikirkan jaringan lokal printer tiap resto.

### D. Billing, Subscription & Feature Gating
Perlu tabel baru untuk mengelola masa aktif langganan dan fitur:
- Paket langganan:
  - **Starter (Rp 149.000/bln):** 1 Outlet, 1 Kasir, Manajemen Menu & Kasir Dasar.
  - **Pro (Rp 249.000/bln):** Resep Bahan Baku (HPP), Multi-Kasir, Table Management, Smart Split Bill. (Ini langsung membunuh Moka yang mengenakan biaya hingga 499rb+).
- **Payment Processing:** Integrasi Midtrans / Xendit Recurring Subscription atau Virtual Account otomatis untuk memperpanjang masa aktif.
- **Grace Period Engine:** Jika telat bayar, sistem memberikan masa tenggang 3 hari sebelum mengunci akses ke mode *Read-Only*.

### E. Integrasi Pembayaran Dinamis (Platform QRIS vs Custom MID)
Sebagai SaaS, resto klien bisa memiliki 2 skenario pembayaran non-tunai:
1. **Facilitator Model (Aggregated):** Resto klien langsung menggunakan QRIS dari akun payment gateway SaaS kita (uang masuk ke rekening platform dulu, lalu di-payout berkala ke resto setelah dipotong MDR). Ini paling disukai kafe kecil karena tidak perlu ribet daftar izin BI/Midtrans.
2. **Direct Merchant ID (Custom MID):** Resto besar yang sudah punya akun Midtrans/Xendit sendiri bisa memasukkan `Server Key` mereka di menu *Settings*, sehingga uang QRIS langsung masuk ke rekening bank mereka sendiri.

---

## 3. Tambahan Skema Database untuk SaaS (PostgreSQL DDL)

Tambahkan tabel berikut ke skema database:

```sql
-- 1. SUBSCRIPTIONS & PLANS
CREATE TYPE subscription_status AS ENUM ('TRIALING', 'ACTIVE', 'PAST_DUE', 'CANCELLED');

CREATE TABLE subscription_plans (
    id VARCHAR(50) PRIMARY KEY, -- 'starter_monthly', 'pro_monthly'
    name VARCHAR(100) NOT NULL,
    price NUMERIC(14,2) NOT NULL,
    max_outlets INT NOT NULL DEFAULT 1,
    max_devices_per_outlet INT NOT NULL DEFAULT 1,
    features JSONB NOT NULL DEFAULT '{}' -- {"inventory_bom": true, "table_mgmt": true}
);

CREATE TABLE business_subscriptions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    business_id UUID UNIQUE NOT NULL REFERENCES businesses(id) ON DELETE CASCADE,
    plan_id VARCHAR(50) NOT NULL REFERENCES subscription_plans(id),
    status subscription_status NOT NULL DEFAULT 'TRIALING',
    trial_ends_at TIMESTAMPTZ,
    current_period_start TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    current_period_end TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 2. DEVICE REGISTRATION & PAIRING
CREATE TABLE devices (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    business_id UUID NOT NULL REFERENCES businesses(id) ON DELETE CASCADE,
    outlet_id UUID NOT NULL REFERENCES outlets(id) ON DELETE CASCADE,
    device_name VARCHAR(100) NOT NULL, -- e.g. "Tablet Kasir Bar Utama"
    device_fingerprint VARCHAR(255),
    pairing_code VARCHAR(10),          -- 6-digit one-time code
    pairing_code_expires_at TIMESTAMPTZ,
    device_token_hash VARCHAR(255),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    last_synced_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```
