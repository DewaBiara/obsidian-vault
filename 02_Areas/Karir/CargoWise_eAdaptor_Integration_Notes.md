# 🔌 CargoWise: eAdaptor, eAdaptor Next, EDI Client & Middleware — Catatan Riset

**Tanggal riset:** 9 November 2026
**Konteks:** Onboarding Backend Engineer di OneByOne Logistical — permintaan integrasi ke CargoWise (CW1)
**Status verifikasi:** Bagian teknis diverifikasi dari dokumentasi vendor/konsultan. Klaim yang tidak terverifikasi ditandai eksplisit.

---

## 0. Peta Besar — 3 Lapisan yang Berbeda

```
Sistem kamu / klien EDI  →  Middleware / Relay  →  eAdaptor  →  CargoWise (CW)
   (ERP, WMS, Shopify)        (opsional, sering wajib)   (gateway)      (TMS)
```

Kesalahan umum: menganggap "eAdaptor", "EDI Client", dan "EDI mapping" itu satu hal.
Kenyataannya **tiga hal berbeda di tiga tempat**:

| Komponen | Di mana | Apa |
|---|---|---|
| **eAdaptor** | Antara sistem luar ↔ CargoWise | Gateway pesan berbasis XML |
| **EDI Client** | Di dalam CargoWise | Entitas konfigurasi koneksi per sistem luar |
| **EDI Mapping** | Di sisi kita (kode/transform) | Konversi format bisnis ↔ XML CargoWise |
| **Middleware/Relay** | Antara eAdaptor ↔ banyak sistem | Fan-out, transform, filter, strip data |

---

## 1. eAdaptor — Gateway Integrasi CargoWise

**Definisi:** antarmuka pesan berbasis **XML** — bukan REST API biasa dengan JSON.
Semua data masuk/keluar CargoWise lewat sini.

**Dua arah:**

- **Inbound** — sistem luar mengirim XML ke CargoWise (push/query/add/update record)
- **Outbound** — CargoWise mengirim notifikasi saat Milestone/Trigger terjadi

> ⚠️ **PENTING:** eAdaptor **tidak aktif secara default**. Harus diajukan support request ke WiseTech dulu sebelum bisa dipakai. Kalau instance belum pernah dipakai untuk integrasi, ini langkah pertama — dan bisa makan waktu.

**Dokumentasi developer eAdaptor TIDAK publik.** WiseTech hanya membuka aksesnya untuk pelanggan yang membeli modul eAdaptor, dan partner harus tanda NDA. Ini yang disebut "knowledge barrier" — harus commit dulu baru boleh belajar.

---

## 2. eAdaptor Legacy vs eAdaptor Next

Ini transisi terbesar yang sedang terjadi di seluruh ekosistem CargoWise.

### Legacy eAdaptor

| Aspek | Detail |
|---|---|
| Transport | **SOAP** (WSDL: `eAdapterStreamedService.wsdl`) |
| Auth | **Basic Auth** — username/password + `clientId` |
| Method SOAP | `Ping`, `SendStream`, `ProcessStream` (deprecated) |
| Return value | **TIDAK ADA hasil** — hanya terima pesan, status dicari manual |
| Format | XML wajib, harus dikompres & di-wrap dengan cara spesifik |

`SendStream` hanya mengindikasikan CW **menerima** pesan. Untuk tahu hasilnya:
- Cek **EDI Interchange** di UI CargoWise, ATAU
- Baca langsung dari database CW (kalau punya read access), ATAU
- Pakai **tracking UUID** yang kita generate dan kirim bersama pesan

### eAdaptor Next

Dari halaman fitur resmi CargoWise (`cargowise.com/cargowise-mega-features`):
> *"With improved traceability, multi-system support, and advanced messaging capabilities, eAdaptor Next fully replaces SOAP for both inbound and outbound communication."*

| Aspek | Detail |
|---|---|
| Transport | **REST over HTTP** dengan payload XML |
| Auth Inbound | **OAuth 2.0** — pakai **client certificate**, bukan password |
| Auth Outbound | **Basic Authentication** |
| Auth On-premise | Basic Auth **masih tersedia khusus instance on-premise** |
| Token | **JWT** (JSON Web Token) di alur otentikasi |
| Multi-system | Tiap sistem luar punya kredensial & batas akses sendiri |
| Tanpa SOAP | UniversalInterchange XML dikirim **tanpa** SOAP envelope |

**Alur otentikasi Inbound OAuth (dari dokumentasi Complect):**

1. Di CargoWise: `Maintain > EDI Messaging > EDI Client Details` → New
2. Tick **Enabled** di Config, lalu di tab **Inbound** tick **Active**
3. Set **Authorisation Type** = `OAU`
4. Pilih **Branch** dan **Department**
5. Kirim **CSR (Certificate Signing Request)** yang kita generate → klik **Verify** (harus hijau) → klik **Generate Certificate**
6. CargoWise membuat **identity baru di authentication server**-nya (butuh waktu; pakai **Refresh Certificates**)
7. Setelah selesai, field **OAuth Authority URL**, **OAuth Client ID**, dan **Scope** terisi otomatis
8. Download certificate dari **Certificate List**

Contoh format OAuth Authority URL: `https://login.microsoftonline.com/{tenantId}/v2.0`

> ⚠️ **Sertifikat kedaluwarsa ~1 tahun.** WiseTech menghubungi *Technical Contact* sebelum expiry. Kalau ini tidak ditangani, integrasi **mati total**. Ini termasuk penyebab downtime paling umum — masukin ke kalender monitoring.

### Tenggat Januari 2027 — ⚠️ KLAIM PIHAK KETIGA

Beberapa konsultan (Elicit Technology, SFL Tech, Enkay Tech, Zinnovate) menyebut **legacy eAdaptor dipensiunkan Januari 2027** dan klien wajib migrasi ke eAdaptor Next.

**Yang perlu dicatat jujur:** saya **tidak menemukan pengumuman resmi WiseTech** yang mengonfirmasi tanggal itu secara langsung. Semua sumber adalah vendor konsultan yang punya kepentingan komersial di proyek migrasi.

**Tindakan:** konfirmasi langsung ke Account Manager WiseTech atau dokumentasi partner sebelum memakai tanggal ini sebagai dasar perencanaan proyek.

---

## 3. EDI Client — Konfigurasi di Dalam CargoWise

**Bukan produk terpisah.** Ini entitas konfigurasi di dalam CargoWise:
`Maintain > EDI Messaging > EDI Client Details`

**Satu EDI Client = satu titik koneksi untuk satu sistem luar.**

### Field penting

**Basic tab**
- **Connection Type** = `EAN - eAdaptorNext`
- **Client Name** (samakan dengan nama di sistem kita, memudahkan tracking)
- **Enabled** ✅

**Inbound tab** (sistem luar → CargoWise)
- **Active** ✅
- **Authorisation Type** = `OAU` (OAuth) atau Basic (on-premise)
- **Branch** & **Department**
- **Certificate List** (CSR → Verify → Generate Certificate → Download Certificate)

**Outbound tab** (CargoWise → sistem luar)
- **Authorisation Type** = Basic Authentication
- **Active** ✅ (kalau tidak butuh outbound, **un-tick** — kalau dibiarkan aktif, validasi save akan gagal karena field outbound kurang)
- **Endpoint URL** (satu-satunya!)

**Settings** (yang harus diberikan ke sistem luar)
- OAuth Authority URL
- OAuth Client ID
- Scope
- Certificate file
- eAdaptor Next Service URL

**Field tambahan per kasus** — mis. untuk warehouse order processing, sistem luar juga butuh **Organization Code** dan **Warehouse Code**.

### Prinsip penting

> **Satu sistem luar = satu EDI Client = satu sertifikat.**

Jangan pakai satu kredensial untuk banyak sistem. Melanggar least-privilege, menyulitkan audit, dan satu kebocoran = semua terpapar.

---

## 4. EDI Mapping — Kerjaan Paling Berat

Ada **dua dialek XML** di CargoWise.

### a. Universal XML — skema standar lintas dokumen

**Root envelope:**
```xml
<?xml version="1.0" encoding="utf-8"?>
<UniversalInterchange xmlns="http://www.cargowise.com/Schemas/Universal/2011/11" version="1.1">
  <Header>...</Header>
  ...
</UniversalInterchange>
```

**Dua tipe payload:**

| Tipe | Isi | Kegunaan |
|---|---|---|
| **XUS** (XML Universal Shipment) | Record lengkap: consignor/consignee, container & cargo, referensi customs, dokumen eDocs terlampir | Transfer record penuh |
| **XUE** (XML Universal Event) | Sengaja tipis: ID record + event + timestamp | Update milestone real-time |

### b. Native XML — format internal level rendah

- Dipakai untuk entitas spesifik yang **tidak diekspos** Universal XML
- Contoh nyata: **Universal XML tidak bisa search Organisasi** — itu wajib Native XML
- Sering dipakai untuk import massal (Actions → Data Transfer → Import Native XML)

### Kapan pakai yang mana

| Kebutuhan | Format |
|---|---|
| Integrasi standar lintas modul (shipment, booking, invoice) | **Universal XML** (XUS/XUE) |
| Akses objek yang tidak ada di Universal (party/organization search) | **Native XML** |
| Update field spesifik di modul tertentu | **Native XML** |

### ⚠️ Jebakan mapping yang paling mahal

**Modul Forwarding, Customs, Warehouse, dan Transport masing-masing punya object tree BERBEDA di dalam skema XUS yang sama.**

Customs declaration dan warehouse receipt tinggal di cabang object tree berbeda, meskipun keduanya bisa muncul di dalam envelope Universal Shipment yang sama.

**Artinya:** sebelum mapping satu field pun, tentukan dulu **modul CW mana yang memiliki data itu**. Salah paham di sini bisa menghabiskan berminggu-minggu development.

---

## 5. Middleware — Kenapa Hampir Selalu Wajib

### 5 Constraint Arsitektur eAdaptor (dari analisis produksi CargoMode)

**1. Single outbound endpoint**
CargoWise hanya mengizinkan **SATU** Outbound Service URL di System Registry. Titik.
Kalau ada 3 sistem yang butuh notifikasi (ERP, WMS, aplikasi customer) → **wajib relay/proxy**.

**2. Async processing — tidak ada respons langsung**
Kirim pesan → CargoWise balas **tracking UUID**, bukan hasil.
Status sebenarnya muncul belakangan di **EDI Interchange**.

Konsekuensi arsitektur:
- Butuh mekanisme polling status, ATAU baca DB CW langsung
- Butuh **timeout + penanganan partial failure untuk semuanya**
- Kalau timeout: **apakah pesan masuk atau tidak?** Tidak ada cara tahu tanpa cek tracking UUID

> Ini **masalah idempotency yang persis sama** dengan integrasi SAP dan sistem enterprise lain.

**3. XML-only**
Konsumen non-XML (API modern/JSON) butuh transformasi.

**4. Default UI tidak berlaku**
Pesan API harus **self-contained** — semua field yang biasanya diisi otomatis oleh UI CargoWise (default value, derived field) harus diisi sendiri.

**5. Field locking setelah customs dimulai**
Begitu customs process berjalan, field tertentu **terkunci**. Update setelah titik itu akan ditolak.

### Pola yang terbukti: Hub-and-Spoke dengan Relay

```
CargoWise Outbound (SOAP, 1 URL)
        ↓
   eAdaptor Relay / Middleware
   ├─ Filter    → pilih pesan per modul/organisasi
   ├─ Transform → XUS → JSON / CSV / EDI (X12, EDIFACT)
   ├─ Strip     → buang data sensitif (job costing, internal notes)
   └─ Forward   → API, SFTP, message queue, email, storage
        ↓
   Sistem A, B, C ...
```

**Tiga fungsi relay yang paling sering dipakai:**

1. **Forwarding ke banyak sistem** — mengatasi batas satu URL
2. **Kirim ke SFTP sebagai EDI** — banyak partner masih butuh file EDI via SFTP
3. **Strip data sensitif** — ⚠️ XUS mengandung **job costing** dan **internal notes**

> 🔒 **JANGAN PERNAH kirim XUS mentah ke pihak ketiga.** Ini risiko komersial (bocor harga & margin), bukan cuma risiko teknis.

**Prasyarat sebelum relay bisa dipakai:**
- eAdaptor Outbound Service aktif
- **Organization Proxy** dikonfigurasi
- **Workflow Template** dibuat

---

## 6. Workflow Template — Pemicu Outbound

Supaya CargoWise mengirim pesan keluar, harus ada **Workflow Template** (`Maintain > Workflow`).

### Template Selection Criteria
- Pilih **Process Type** yang butuh mengirim outbound message
- Opsional filter **Client** — kalau per-client, butuh **satu template per client**

### Completion Trigger Actions
Di setiap Milestone/Trigger yang perlu kirim pesan, tambahkan:

| Field | Nilai |
|---|---|
| **Action** | `XUS` (detail lengkap) atau `XUE` (minimal: ID + event) |
| **Recipient** | `ORP` (Organization Proxy) |

**Contoh spesifik — Order Fulfillment:**
Template dengan Process Type `WOU` (Warehouse Release). Di Milestones, yang **Finalized** butuh Completion Trigger Action: Action = `XUS`, Recipient = `ORP`.

### Debugging — kalau workflow tidak firing

1. `Maintain > System > Service Tasks`
2. Cari **`Code` = `LWK`** (Event Log Walker Service)
3. Buka Service tersebut → tab **Log Files**
4. Cari berdasarkan tanggal & jam milestone yang memicu

Ini satu-satunya cara cepat menemukan kenapa trigger tidak jalan.

---

## 7. Implikasi untuk Peran Backend Engineer

### Yang kemungkinan besar dibangun

1. **Relay / Adapter Layer**
   Terima XUS/XUE dari eAdaptor → transform ke format internal → forward.
   → **Ini persis kasus penggunaan Clean Architecture + CQRS**: domain "shipment" bersih, adapter CargoWise di lapisan luar.

2. **Message Status Tracker**
   Karena async, butuh tabel/queue yang menyimpan tracking UUID + polling status.
   → Ini **write model** untuk state pesan; laporan status jadi **read model**.

3. **Idempotency Layer**
   Hash payload + reference key, supaya resend setelah timeout tidak membuat duplikat.
   → Pola sama seperti integrasi SAP.

4. **Retry + Dead Letter Queue**
   Pesan yang ditolak CW harus masuk review queue **dengan alasan**, bukan hilang diam-diam.

### Yang WAJIB ditanyakan di awal

| Pertanyaan | Kenapa penting |
|---|---|
| Instance CW **cloud atau on-premise**? | Menentukan OAuth (cloud) vs Basic Auth (on-prem) |
| Sudah **eAdaptor Next atau masih legacy**? | Legacy → migrasi ke Next proyek tersendiri |
| Modul CW mana yang dipakai (Forwarding/Customs/Warehouse/Transport)? | Menentukan object tree mana yang relevan |
| Ada akses **read ke database CW**? | Kalau ada, tracking status jauh lebih efisien daripada polling |
| Ada **test/training instance**? | Jangan bangun apa pun langsung ke production |
| Siapa **admin CargoWise** yang bisa generate certificate & setup EDI Client? | Tanpa ini, mentok total |
| eAdaptor sudah **diaktifkan** oleh WiseTech di instance itu? | Default-nya tidak aktif |

---

## 8. Sumber Daya Praktis

### Library open source

| Library | Bahasa | Lisensi | Catatan |
|---|---|---|---|
| `SteeleConsulting/cargowise-eadapter` | Node.js/TypeScript | MIT | Handle SOAP + kompresi XML. Bagus untuk memahami cara kerja `SendStream` |
| `yob/cargowise` | Ruby | Open source | SOAP wrapper |
| `oliverbj/cord` | PHP | Open source | Client library |
| `Chizaruu/CargowiseNETLibrary` | .NET 8 | — | Model C# di-generate dari XSD resmi CargoWise |

### Dokumentasi & referensi

| Sumber | Tipe | Isi |
|---|---|---|
| **Complect Solutions docs** (`complect.io/docs/cargowise-integrations`) | Publik, pihak ketiga | **Paling detail** — langkah setup EDI Client, Workflow Template, XUS/XUE |
| **CargoMode "eAdapter in Production"** (`cargomo.de`) | PDF gratis Ch.1 | Analisis constraint arsitektur — paling jujur soal realita produksi |
| **CargoWise mega features** (`cargowise.com/cargowise-mega-features`) | Resmi WiseTech | Pernyataan resmi eAdaptor Next menggantikan SOAP |
| **Chain.io CargoWise API Documentation** | Publik, pihak ketiga | Penjelasan Universal vs Native XML, gating akses |
| **Dokumentasi developer resmi** | ❌ TIDAK PUBLIK | Hanya untuk pelanggan yang beli modul eAdaptor + NDA |

---

## 9. Ringkasan Satu Halaman

> **eAdaptor** = gateway XML CargoWise, tidak aktif default, dokumentasi tidak publik.
> **eAdaptor Next** = versi modern: REST/HTTP + OAuth 2.0 (client certificate) + JWT, menggantikan SOAP. Legacy diprediksi pensiun Jan 2027 (klaim konsultan, belum terverifikasi resmi).
> **EDI Client** = konfigurasi koneksi per sistem luar, di `Maintain > EDI Messaging > EDI Client Details`. Satu sistem = satu client = satu sertifikat.
> **EDI Mapping** = kerjaan berat. Dua dialek: **Universal XML** (XUS lengkap / XUE tipis) dan **Native XML** (objek spesifik). Modul berbeda = object tree berbeda dalam skema sama.
> **Middleware** = wajib kalau >1 sistem, karena outbound cuma boleh satu URL. Relay berfungsi: filter, transform, strip data sensitif, forward.
> **Async everywhere** = kirim → dapat tracking UUID → cek status manual. Idempotency dan timeout handling bukan opsional, ini fondasi.
> **Workflow Template** = pemicu outbound. Action XUS/XUE, Recipient ORP. Debug via Service Task `LWK`.

---

## 10. Hubungan ke Topik Lain

- **Clean Architecture + CQRS** → relevan langsung untuk membangun adapter layer CargoWise. Lihat `Catatan_Onboarding_OneByOne.md`
- **SAP ECC 6.0** → pola integrasi enterprise yang sama (async, idempotency, timeout tanpa kepastian). Lihat file yang sama
- **MDM (Intune) & Hubstaff** → konteks perangkat kerja & monitoring. Lihat file yang sama

---

*Catatan ini dibuat 9 November 2026. Klaim yang ditandai "klaim pihak ketiga" atau "belum terverifikasi" harus dikonfirmasi ulang ke sumber resmi sebelum dipakai untuk keputusan proyek.*
