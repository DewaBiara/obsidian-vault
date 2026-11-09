# 🎓 Catatan Onboarding & Pembelajaran Teknis — OneByOne Logistical

**Tanggal:** 9 November 2026
**Konteks:** Backend Engineer baru di OneByOne Logistical (Bali, hybrid Sunset Bureau Seminyak). Mulai 7 November 2026.
**Tujuan:** Konsolidasi semua topik teknis yang muncul di masa onboarding — supaya tidak hilang dan bisa dipelajari ulang.

---

## 📋 Daftar Isi

1. [Onion / Clean Architecture + CQRS](#1-onion--clean-architecture--cqrs)
2. [SAP ECC 6.0](#2-sap-ecc-60)
3. [MDM (Microsoft Intune) vs Hubstaff](#3-mdm-microsoft-intune-vs-hubstaff)
4. [CargoWise eAdaptor](#4-cargowise-eadaptor)
5. [Workshop Kantor — Apa itu](#5-workshop-kantor)

---

## 1. Onion / Clean Architecture + CQRS

### Masalah yang diselesaikan

Di aplikasi biasa, logika bisnis lambat laun **menempel ke framework, ORM, dan HTTP**. Begitu database berubah — atau mau unit-test tanpa DB — semuanya ikut berantakan.

Clean/Onion Architecture **membalik arah ketergantungan**: logika bisnis tidak tahu apa pun soal database, framework, atau HTTP.

### 🔑 The Dependency Rule (inti semuanya)

> **Panah dependensi hanya boleh mengarah ke dalam. Lapisan dalam tidak boleh mengimpor apa pun dari lapisan luar.**

### Pemetaan Layer

| Onion | Clean | Isinya |
|---|---|---|
| Domain Model | Entities | Struct/class bisnis murni, aturan validasi, invariant |
| Domain Services | Use Cases | Alur satu aksi bisnis (mis. `TransferFunds`) |
| Application Services | Interface Adapters | Konversi HTTP↔domain, repository implementation |
| Infrastructure | Frameworks & Drivers | Postgres, Redis, NestJS, Kafka, SDK SAP/CargoWise |

**Sejarah (istilahnya berbeda, konsepnya sama):**
- **Hexagonal / Ports & Adapters** — Alistair Cockburn, 2005
- **Onion Architecture** — Jeffrey Palermo, 2008
- **Clean Architecture** — Robert C. Martin, 2012

### Yang paling penting: Ports & Adapters

```go
// domain/ledger/repository.go  ← interface didefinisikan DI DALAM
type Repository interface {
    Save(ctx context.Context, e *Entry) error
    FindByID(ctx context.Context, id EntryID) (*Entry, error)
}
```

```go
// infrastructure/postgres/ledger_repo.go  ← implementasi di LUAR
type ledgerRepo struct{ db *sql.DB }
func (r *ledgerRepo) Save(ctx context.Context, e *ledger.Entry) error { ... }
```

> **Kuncinya:** interface didefinisikan di sisi **domain**, bukan di sisi database. Ini yang bikin domain bisa dites tanpa Postgres, dan memungkinkan ganti adapter tanpa menyentuh logika bisnis.

### Struktur folder konkret (Go)

```
/internal
  /ledger
    /domain        ← Entry, Money, aturan saldo. Nol import eksternal.
    /app           ← UseCases: PostEntry, ReverseEntry. Hanya import domain
    /ports         ← interface Repository, EventPublisher
  /adapters
    /http          ← handler, DTO, mapping error
    /postgres      ← implementasi Repository
    /redis         ← implementasi cache/idempotency store
/cmd/api           ← wiring, main.go
```

**Aturan praktis:** kalau file di `/domain` punya `import` selain `errors`/`time`, ada yang salah.

### ⚖️ Trade-off (jujur — ini yang sering tidak disebut)

**Biaya nyata:**
- Boilerplate naik signifikan — satu fitur bisa jadi 5 file
- Banyak mapping antar layer (`domain.Entry` → `dto.Response`) — membosankan
- **Untuk CRUD biasa (tabel master, config), arsitektur ini murni kerugian** — tidak ada logika bisnis yang dilindungi

**Kapan layak:** ada logika bisnis nyata yang harus dilindungi — ledger, pembayaran, idempotency, aturan multi-step, integrasi pihak ketiga kompleks.
**Kapan tidak:** endpoint yang intinya cuma `SELECT` lalu kirim JSON.

---

### CQRS (Command Query Responsibility Segregation)

**Definisi:** pisahkan model yang **menulis** dari model yang **membaca**.

- **Command** — mengubah state. `CreateLedgerEntry`, `ApproveRefund`. **Tidak mengembalikan data** (maksimal ID atau status).
- **Query** — membaca state. `GetLedgerSummary`. **Tidak boleh mengubah apa pun**.

**Asal:** **CQS** (Bertrand Meyer, 1988) — satu method tidak boleh sekaligus mengubah dan mengembalikan data. CQRS = penerapannya di level arsitektur (dipopulerkan Greg Young, ~2010).

#### Tiga Level CQRS — ini yang paling sering disalahpahami

**Level 1 — Pemisahan di kode** *(90% kasus cukup ini)*
Database **satu**. Cuma class/handler-nya dipisah.

```go
type PostEntryCommand struct { AccountID string; Amount Money }
type PostEntryHandler struct{ repo Repository; publisher EventPublisher }

type GetEntryQuery struct { ID string }
type GetEntryHandler struct{ readDB *sql.DB }   // boleh query langsung
```

> **Perhatikan:** handler query **tidak lewat repository domain**. Dia boleh langsung SQL ke read model. Ini **bukan pelanggaran** — justru intinya.

**Level 2 — Pemisahan read model (fisik terpisah)**
Tulis ke DB utama (normalized), baca dari DB/view lain yang dioptimalkan (denormalized, materialized view, Redis, Elasticsearch). Sinkronisasi via event atau CDC.

**Level 3 — Event Sourcing** *(opsional, JANGAN dicampur)*
State tidak disimpan sebagai baris, tapi **rangkaian event**. Saldo = replay semua event.
> Ini topik terpisah dan **BUKAN syarat CQRS**. Banyak orang menolak CQRS karena mengira harus pakai event sourcing — **keliru**.

#### Kenapa orang mau CQRS

1. **Model baca & tulis memang berbeda bentuknya.** Menulis butuh invariant ketat (normalized, transaksional). Membaca butuh data tergabung (denormalized, cepat). Satu model untuk keduanya selalu ada yang dikorbankan.
2. **Skala baca vs tulis tidak seimbang.** Biasanya baca 100× lebih banyak.
3. **Query jadi sederhana.** "Ringkasan transaksi 12 bulan" tanpa CQRS = JOIN 8 tabel. Dengan read model = satu tabel.

#### ⚖️ Trade-off

- **Eventual consistency** — read model tertinggal dari write model (meski 50ms). User simpan data, refresh, belum muncul. **Harus ditangani di UI.**
- **Duplikasi kode** — dua model, dua jalur
- **Debugging lebih sulit** — "kenapa angka read beda dengan write?"
- **Biaya infrastruktur** kalau sampai Level 2

> **Aturan praktis:** mulai Level 1. Naik ke Level 2 hanya kalau ada **bukti** query-nya lambat, bukan karena prediksi.

---

### 🔗 Hubungan keduanya

```
Clean Architecture  → soal ARAH DEPENDENSI (bagaimana kode diorganisir)
CQRS                → soal PEMISAHAN TANGGUNG JAWAB baca vs tulis
```

**Bisa pakai Clean tanpa CQRS. Bisa pakai CQRS tanpa Clean. Bisa dua-duanya.**

Dalam praktik, CQRS Level 1 **sangat cocok** dengan Clean Architecture karena Command/Query Handler itu memang "Use Case" versi Clean.

**⚠️ Yang TIDAK benar:**
- ❌ "CQRS berarti harus microservices"
- ❌ "CQRS berarti harus pakai Kafka / event sourcing"

---

### 🎯 Kenapa senior minta ini (konteks OneByOne)

1. **Integrasi CargoWise / SAP.** Integrasi enterprise penuh kasus aneh: timeout setelah transaksi berhasil, payload duplikat, master data tidak konsisten. Clean Architecture memisahkan "aturan integrasi" dari "cara memanggil pihak ketiga" — jadi saat jalur berubah (eAdaptor Legacy → Next, IDoc → OData), logikanya tidak ikut dirombak.
2. **Kalau ada ledger/finansial.** Write model ketat (jurnal balance, idempotent, immutable), read model cepat (ringkasan, laporan). Ini contoh paling klasik kenapa CQRS ada.
3. **Standar kode tim.** Di perusahaan jasa, engineer berpindah proyek. Arsitektur seragam = orang bisa pindah tanpa belajar ulang.

---

### 📚 Rencana Belajar Konkret

**Minggu 1 — pahami, jangan bikin dulu**
- Baca artikel asli: Palermo "Onion Architecture" (2008), Uncle Bob "The Clean Architecture" (2012), Martin Fowler "CQRS" (2011)
- Baca "CQRS Documents" Greg Young — paling jujur soal kapan **tidak** memakainya

**Minggu 2 — bikin satu modul kecil sendiri**
- Domain tanpa import eksternal
- Repository sebagai interface di domain
- Dua adapter: in-memory untuk test, Postgres untuk produksi
- Pisahkan command handler vs query handler
- **Ukur sendiri biaya boilerplate-nya** — pengalaman yang tidak bisa didapat dari artikel

**Minggu 3 — refactor kode yang sudah ada**
Ambil satu modul paling berantakan, refactor. Ini yang membuat benar-benar paham bedanya teori dan praktik.

### ❓ Pertanyaan yang layak diajukan ke senior

- *"Untuk modul CRUD murni, apakah tetap full layer atau boleh lebih tipis?"*
- *"CQRS-nya sampai level berapa — pisah handler saja, atau pisah read model fisik?"*
- *"Kalau read model terpisah, konsistensinya ditangani bagaimana di UI — optimistic update atau menunggu?"*
- *"Apakah ada rencana ke event sourcing, atau CQRS saja?"* ← penting, banyak yang tidak sadar bedanya
- *"Transaksi lintas aggregate ditangani di mana — di use case atau di domain service?"*

---

## 2. SAP ECC 6.0

**Definisi:** **SAP ERP Central Component 6.0** — produk ERP inti SAP. Sistem "generasi lama", pendahulu **SAP S/4HANA**.

### Modul utama

| Kode | Modul |
|---|---|
| **FI/CO** | Finance & Controlling (akuntansi, GL, AR/AP, costing) |
| **MM** | Materials Management (purchasing, inventory) |
| **SD** | Sales & Distribution |
| **PP** | Production Planning |
| **QM** | Quality Management |
| **HR/HCM** | Kepegawaian |
| **PM** | Plant Maintenance |

### Istilah teknis

- **ABAP** — bahasa pemrograman internal SAP
- **NetWeaver** — platform dasar
- **EHP (Enhancement Package)** — paket pembaruan fitur. Terakhir: **EHP 8**
- **HANA** — database in-memory (untuk S/4HANA)

### ⏰ Kenapa topik ini "panas" sekarang

SAP menghentikan **mainstream maintenance**:
- **31 Desember 2027** — untuk sebagian besar pelanggan ECC 6.0
- **2030** — batas akhir *extended maintenance* (lebih mahal)

Artinya jutaan perusahaan sedang dipaksa migrasi ke S/4HANA. Itu sebabnya ECC jadi bahan pembicaraan konstan di perusahaan jasa integrasi — **bukan karena teknologinya baru, tapi karena ini pasar kerja besar yang sedang terbuka**.

### Opsi jalur integrasi (kalau menyambung ke ECC)

| Jalur | Tipe | Kapan dipakai |
|---|---|---|
| **IDoc** | Async | Master data & dokumen bisnis. `ORDERS05`, `INVOIC02`, `DESADV01`, `MATMAS` |
| **BAPI / RFC** | Sync | Cek stok, ambil master data, buat dokumen butuh respons langsung |
| **OData** (via Gateway) | Sync, HTTP+JSON | Kalau NetWeaver Gateway terpasang. Cek `/IWFND/MAINT_SERVICE` |
| **SOAP / Enterprise Services** | Sync | Skenario butuh standar ketat |
| **File drop / SFTP** | Async | Paling sering dipakai di dunia nyata. Sederhana, tapi rawan duplikasi |

### ⚠️ Jebakan integrasi SAP

1. **Idempotency mutlak wajib.** Koneksi sering timeout **setelah** transaksi berhasil. Retry tanpa kunci idempotensi = dokumen dobel. **Masalah nomor satu.**
2. **SAP bukan REST API.** Latency ratusan ms sampai beberapa detik. Jangan panggil per-item dalam loop — pakai batch.
3. **Tes di `SE37`/`WE19` dulu.** Engineer SAP bisa tes BAPI/IDoc manual sebelum dibuat kode.
4. **Perubahan di sisi SAP lambat.** Butuh transport request (`SE01`/`SE10`) DEV → QA → PROD. Bisa hitungan minggu.
5. **Jangan pakai user dialog.** Minta *communication user* dengan otorisasi minimal.
6. **Log semua payload.** Satu-satunya cara menyelesaikan debat dengan tim SAP.

### ❓ Yang wajib ditanyakan di hari pertama

- Arah integrasi: tarik dari SAP, kirim ke SAP, atau dua arah?
- **Apakah SAP NetWeaver Gateway terpasang?** (penentu OData tersedia)
- **Ada middleware?** (SAP PI/PO atau Integration Suite) — kalau ada, **jangan** panggil ECC langsung
- **Siapa ABAP resource-nya?** Hampir semua jalur butuh orang SAP

---

## 3. MDM (Microsoft Intune) vs Hubstaff

### ⚠️ MDM punya DUA arti yang tidak berhubungan

| Arti | Bidang | Contoh produk |
|---|---|---|
| **Mobile Device Management** | IT / Security | Intune, Jamf, Workspace ONE |
| **Master Data Management** | Data / Enterprise Architecture | SAP MDG, Informatica MDM, Stibo STEP |

**Di konteks OneByOne: yang dimaksud adalah Mobile Device Management, dan produknya Microsoft Intune.**

---

### Microsoft Intune — mengelola & mengamankan perangkat

**Definisi resmi Microsoft:** *cloud-based endpoint management service* untuk enroll, konfigurasi, mengamankan, dan meng-update perangkat, mendistribusikan aplikasi, serta mengatur siapa yang boleh akses resource perusahaan.

**Platform didukung:** Android, iOS/iPadOS, Linux, macOS, tvOS, visionOS, Windows. Sepenuhnya cloud — tanpa server on-premise.

**Dua mode manajemen (bisa sendiri atau bersamaan):**

- **MDM** — perangkat di-enroll utuh. Intune kelola seluruh device: setting, keamanan, aplikasi. Bisa di-*wipe* kalau hilang/dicuri.
- **MAM** — hanya mengelola aplikasi kerja & data di dalamnya, bukan seluruh perangkat. Khas untuk **BYOD**: HP pribadi tetap milik karyawan, data di Outlook/Teams dilindungi dan bisa dihapus selektif saat karyawan keluar.

**Tiga pilar Intune:** identitas (via **Microsoft Entra ID**), perangkat, aplikasi.
Postur perangkat & aplikasi mengalir balik ke **Conditional Access** — akses ditentukan sinyal nyata: apakah perangkat patuh, OS ter-update, terenkripsi.

**Untuk engineer:** setiap aksi di admin center Intune sebenarnya panggilan **Microsoft Graph API**. Semua yang bisa lewat UI, bisa diotomasi lewat API. Pintu masuk kalau nanti diminta bikin tooling internal.

**Intune tidak menyimpan identitas & tidak melakukan autentikasi** — itu tugas Entra ID.

---

### Hubstaff — mengukur waktu & aktivitas kerja

**Definisi resmi:** *employee time-tracking software with screenshots and activity monitoring, reporting, and automated payments.*

**Cara kerjanya (dari FAQ resmi Hubstaff):**
- Karyawan install aplikasi di mesinnya (kecuali pakai *silent app*), pilih project, waktu terlacak ke project itu
- **Screenshot acak ~tiap 10 menit** (hanya paket berbayar)
- Merekam **URL & aplikasi** yang dibuka, serta **lokasi** (mobile)
- **Activity rate dihitung per detik:** gerakan mouse atau ketikan = active; tidak ada keduanya = inactive. Dijumlahkan jadi persentase per segmen 10 menit
- **5 menit tanpa aktivitas → status idle**; karyawan ditawari menghapus waktu itu dari log

> ⚠️ **Yang diukur adalah gerakan mouse & keyboard, BUKAN output pekerjaan.**
> Backend engineer yang 40 menit berpikir lalu menulis 30 baris yang menyelesaikan masalah besar akan terlihat "kurang aktif" dibanding orang yang scroll dokumen.

**Fitur lain:** timesheet, laporan produktivitas, payroll otomatis, opsi *silent app* (jalan tanpa terlihat di tray).

---

### Perbandingan

| Aspek | **Intune** | **Hubstaff** |
|---|---|---|
| **Tujuan** | Keamanan & kontrol perangkat | Mengukur waktu & aktivitas kerja |
| **Pertanyaan dijawab** | "Apakah perangkat ini aman dan patuh kebijakan?" | "Berapa jam dan seberapa aktif orang ini bekerja?" |
| **Pemilik** | Tim IT / Security | Ops / HR / Management |
| **Objek** | Device & aplikasi | Karyawan |
| **Level** | Infrastruktur | Aplikasi di atasnya |

### 🔗 Hubungan keduanya

Hubstaff punya FAQ khusus *"How does tracking work on company-owned devices?"* dan menyediakan **silent app**. Keduanya ada karena pola umum: **Intune yang mendistribusikan & mengonfigurasi Hubstaff** ke semua laptop karyawan, sehingga:

- Karyawan tidak bisa uninstall sendiri (dikunci lewat kebijakan MDM)
- Setting seragam di semua perangkat
- Kalau perangkat hilang, bisa di-wipe termasuk data Hubstaff-nya

> **Bukan "Intune vs Hubstaff".** Yang benar: **Intune mengatur perangkat, Hubstaff memantau kerja di dalamnya.**

---

### 🔒 Yang perlu diketahui sebagai karyawan

**Legal & wajar:** memantau perangkat & aktivitas **milik perusahaan** pada jam kerja, dengan pemberitahuan. Hampir semua yurisdiksi membolehkan.

**Yang bermasalah:** tracking di perangkat pribadi tanpa persetujuan eksplisit, atau memantau di luar jam kerja. Di Indonesia masuk ranah **UU PDP (No. 27/2022)** — pemantauan harus punya dasar jelas dan proporsional.

**Praktisnya:**
- Kalau laptop kerja bisa di-wipe jarak jauh, **jangan simpan file pribadi di sana**. Ini konsekuensi teknis MDM, bukan soal curiga.
- Kalau ada opsi install di perangkat pribadi, **pakai laptop kantor saja**.
- **Idle time bukan ukuran kinerja.** Kalau ditegur karena activity rate rendah padahal output beres, bawa bukti output — bukan pembelaan soal mouse.
- Deep work (debugging, desain arsitektur, baca dokumentasi) **selalu** terlihat rendah activity rate. Komunikasikan lebih awal ke atasan, bukan setelah jadi masalah.

---

## 4. CargoWise eAdaptor

📄 **Catatan lengkap ada di file terpisah:** [[CargoWise_eAdaptor_Integration_Notes]]

Isi: eAdaptor Legacy vs Next, EDI Client setup, Universal vs Native XML (XUS/XUE), Workflow Template, 5 constraint arsitektur, pola relay/middleware, pertanyaan wajib ke tim CW.

---

## 5. Workshop Kantor

**Definisi:** sesi kolaboratif yang berfokus pada **praktik langsung**, bukan mendengarkan presentasi.

### Bedanya dengan yang lain

| Format | Arah | Isi |
|---|---|---|
| **Seminar/kuliah** | Satu arah | Peserta dengar |
| **Meeting** | Diskusi | Membahas keputusan & status kerjaan |
| **Workshop** | Partisipatif | Peserta **kerjakan sesuatu** — ada latihan, studi kasus, output nyata |

Biasanya 2–4 jam, peserta 10–30 orang.

### Bentuk umum di kantor

- **Skill-based** — training tools baru (Git workflow, Docker, SQL tuning), Excel lanjutan, public speaking
- **Cross-functional** — sesi antar tim supaya Backend paham kebutuhan QA/PM
- **Problem-solving** — bawa satu masalah nyata perusahaan, selesaikan bareng dalam sesi
- **Onboarding / knowledge sharing** — karyawan senior share pengalaman, retrospektif

### Kenapa kantor tertentu rutin mengadakan

- **Timnya campur level** — junior butuh dipandu senior secara terstruktur, bukan dibimbing sambil kerja
- **Tooling berubah cepat** — kalau tidak ada sesi khusus, orang belajar sendiri-sendiri dan hasilnya tidak seragam
- **Sektor jasa/konsultan** — waktu belajar dihitung sebagai kerja, karena output-nya dijamu ke klien

### Yang sebaiknya disiapkan

- Bawa laptop + siapkan environment (workshop hampir selalu *hands-on*)
- Catat istilah domain yang belum familiar — jangan malu bertanya
- **Siapkan satu pertanyaan tajam**, mis: *"Untuk proyek klien baru, standar minimum yang wajib dipenuhi sebelum masuk code review itu apa saja?"*

---

*Terakhir diperbarui: 9 November 2026*
