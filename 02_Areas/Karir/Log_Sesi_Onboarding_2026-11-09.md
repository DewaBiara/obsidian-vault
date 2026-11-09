# 📝 Log Sesi Belajar — 9 November 2026

**Konteks:** Sesi tanya-jawab teknis selama onboarding di OneByOne Logistical.
**Format:** kronologis — pertanyaan asli, ringkasan jawaban, dan keputusan/tindakan.

Catatan materi lengkap ada di:
- [[Catatan_Onboarding_OneByOne]] — Clean Architecture/CQRS, SAP ECC, MDM/Hubstaff, Workshop
- [[CargoWise_eAdaptor_Integration_Notes]] — riset CargoWise lengkap

---

## 1. Koreksi: jangan mengarang jawaban

**Pertanyaan:** *"Brarti kamu berbohong tadi :v"* → lalu *"Nah gitu dong, jangan mengarang untuk menyenangkanku. Jawab sejujurnya kalau perlu lakuin research sebelum memberi jawaban"*

**Konteks kesalahan:** Sebelumnya saya mengklaim kata "mixiww" (plesetan "miss you") adalah **tren Gen Z** dengan jalur turunan tertentu. Setelah dicek lewat pencarian, tidak ada entri/dokumentasi resmi apa pun. Itu murni rekonstruksi logis yang saya sampaikan seolah fakta.

**Aturan yang ditetapkan:**
- Kalau tidak tahu → bilang tidak tahu
- Kalau menebak → sebut itu tebakan
- Riset dulu sebelum menyatakan sesuatu sebagai fakta, terutama soal **asal-usul kata, tren, angka, dan klaim teknis**

**Status:** ✅ Diterima sebagai aturan tetap.

---

## 2. Workshop kantor

**Pertanyaan:** *"Workshop di kantor adalah"* (kalimat terpotong) → *"Oke aku cuma pengen tau karena di kantor lamaku itu gaada"*

**Jawaban ringkas:**
- Workshop = sesi kolaboratif berfokus **praktik langsung**, bukan mendengarkan presentasi
- Beda dengan **seminar** (satu arah), **meeting** (bahas keputusan/status)
- Biasanya 2–4 jam, 10–30 peserta, ada output nyata di akhir sesi

**Bentuk umum:** skill-based (tools baru), cross-functional, problem-solving (bawa masalah nyata), onboarding/knowledge sharing.

**Kenapa kantor tertentu rutin mengadakan:**
1. Tim campur level — junior butuh dipandu terstruktur
2. Tooling berubah cepat — kalau tidak ada sesi, hasil belajar tidak seragam
3. Sektor jasa/konsultan — waktu belajar dihitung kerja karena output dijamu ke klien

**Observasi pribadi:** kantor lama tidak ada workshop = pola umum di Indonesia. Kantor baru ada = sinyal manajemen melihat *skill gap* layak diinvestasikan waktu.

---

## 3. Workshop OneByOne — prediksi

**Pertanyaan:** *"Nah di onebyone ini bakal ngadain workshop hari ini, kira kira gimana nanti? dan kemungkinan apa yang bakalan dibahas?"*

**Yang bisa dipastikan:** agenda internal tidak dipublikasi. Bagian prediksi di bawah adalah **inferensi dari profil bisnis publik**, bukan bocoran.

**Profil OneByOne (dari sumber publik):**
- Managed services & systems integrator untuk **logistik, supply chain, transportasi**
- HQ Melbourne; kantor Bali (Sunset Road, Seminyak), Batam, Singapura, Ho Chi Minh, Tokyo, Seoul
- Klien enterprise — integrasi CargoWise, Microlistics, NetSuite, SAP, Shopify, AWS/Azure
- Stack: Java, C#, Node/TypeScript, Python, PHP, React, Flutter

**Karakter workshop di perusahaan model begini:**
- **Output-oriented** — ada deliverable nyata (repo contoh, dokumen standar, checklist)
- **Cross-office** — sering gabung Bali–Batam–Melbourne, format hybrid
- **Platform-specific** — transfer pengetahuan platform partner (CargoWise, Microlistics)

**Prediksi topik (urut kemungkinan):**
1. AI-assisted development (mereka mencantumkan Anthropic di stack)
2. Standar engineering & code quality
3. Integrasi platform logistik (CargoWise/Microlistics/NetSuite)
4. Security & compliance
5. Domain knowledge logistik (shipment lifecycle, incoterms, WMS/TMS)
6. QA & testing standard

**Persiapan yang disarankan:** bawa laptop + environment siap, catat istilah domain yang belum familiar, siapkan satu pertanyaan tajam.

---

## 4. SAP ECC 6.0

**Pertanyaan:** *"SAP ECC 6.0 — Apa yang dimaksud ini?"*

**Definisi:** **SAP ERP Central Component 6.0** — produk ERP inti SAP, pendahulu **SAP S/4HANA**.

**Modul utama:** FI/CO (finance), MM (materials), SD (sales), PP (production), QM (quality), HR/HCM, PM (plant maintenance).

**Istilah teknis:** ABAP (bahasa internal), NetWeaver (platform), EHP (Enhancement Package — terakhir EHP 8), HANA (database in-memory).

**Kenapa "panas" sekarang:** SAP menghentikan mainstream maintenance:
- **31 Desember 2027** — sebagian besar pelanggan ECC 6.0
- **2030** — batas akhir extended maintenance (lebih mahal)

→ Jutaan perusahaan dipaksa migrasi ke S/4HANA. Ini pasar kerja besar yang sedang terbuka.

**Relevansi dengan OneByOne:** mereka menjual jasa integrasi SAP. Konteks workshop kemungkinan: klien masih pakai ECC dan butuh integrasi, pembahasan migrasi ECC → S/4HANA, atau penjelasan kompleksitas integrasi sistem enterprise.

---

## 5. Rencana integrasi ke SAP

**Pertanyaan:** *"Aku di perusahaan baru ingin melakukan integrasi kesana"*

**4 hal yang wajib dipastikan dulu:**
1. **Arah integrasi** — tarik dari SAP, kirim ke SAP, atau dua arah?
2. **Apakah SAP NetWeaver Gateway terpasang?** Penentu apakah OData tersedia. Cek transaksi `/IWFND/MAINT_SERVICE`. Di ECC 6.0, Gateway komponen tambahan `SAP_GWFND` — sering tidak diinstal.
3. **Ada middleware?** (SAP PI/PO atau Integration Suite) — kalau ada, **jangan** panggil ECC langsung.
4. **Siapa ABAP resource-nya?** Hampir semua jalur butuh orang SAP mendaftarkan service/BAPI/partner profile.

**Opsi jalur integrasi:**

| Jalur | Tipe | Kapan dipakai |
|---|---|---|
| **IDoc** | Async | Master data & dokumen bisnis. `ORDERS05`, `INVOIC02`, `DESADV01`, `MATMAS`. Config: `WE20`, monitor `WE02`/`WE05`, reprocess `BD87` |
| **BAPI / RFC** | Sync | Cek stok, ambil master data. Tes di `SE37`. Risiko: thread menggantung kalau SAP lambat |
| **OData** (Gateway) | Sync HTTP+JSON | Kalau Gateway terpasang. Auth bukan JWT biasa — biasanya Basic/OAuth2 SAML Bearer/X.509 |
| **SOAP / Enterprise Services** | Sync | Skenario butuh standar ketat. Lebih tersedia di instalasi ECC lama |
| **File drop / SFTP** | Async | Paling sering dipakai nyata. Sederhana, rawan duplikasi |

**Jebakan yang bikin proyek SAP gagal:**
1. **Idempotency mutlak wajib** — koneksi sering timeout SETELAH transaksi berhasil. Retry tanpa kunci idempotensi = dokumen dobel. **Masalah nomor satu.**
2. **SAP bukan REST API** — latency ratusan ms sampai detik. Jangan panggil per-item dalam loop.
3. **Tes di `SE37`/`WE19` dulu** sebelum koding.
4. **Perubahan di sisi SAP lambat** — transport request (`SE01`/`SE10`) DEV → QA → PROD, bisa hitungan minggu.
5. **Jangan pakai user dialog** — minta *communication user* dengan otorisasi minimal.
6. **Log semua payload** — satu-satunya cara menyelesaikan debat dengan tim SAP.

---

## 6. Onion/Clean Architecture + CQRS

**Pertanyaan:** *"onion clean architecture, dan CQRS pattern, seniorku meminta belajar tentang ini"*

**Inti Clean Architecture — The Dependency Rule:**
> Panah dependensi hanya boleh mengarah ke dalam. Lapisan dalam tidak boleh mengimpor apa pun dari lapisan luar.

**Layer:** Domain (Entities) → Use Cases → Interface Adapters → Infrastructure.

**Sejarah (konsep sama, penekanan beda):** Hexagonal/Ports & Adapters (Cockburn, 2005) → Onion (Palermo, 2008) → Clean (Martin, 2012).

**Kunci Ports & Adapters:** interface didefinisikan di sisi **domain**, bukan di sisi database. Itu yang bikin domain bisa dites tanpa Postgres dan adapter bisa diganti tanpa menyentuh logika bisnis.

**CQRS — tiga level (yang paling sering disalahpahami):**
- **Level 1** — pisah handler, database satu. **90% kasus cukup ini.**
- **Level 2** — pisah read model fisik (DB/view lain, materialized view, Redis, ES)
- **Level 3** — Event Sourcing. **Opsional, BUKAN syarat CQRS.**

**Trade-off CQRS:** eventual consistency (harus ditangani di UI), duplikasi kode, debugging lebih sulit, biaya infrastruktur.

**Yang TIDAK benar:**
- ❌ "CQRS berarti harus microservices"
- ❌ "CQRS berarti harus Kafka / event sourcing"

**Hubungan keduanya:** Clean = soal arah dependensi; CQRS = soal pemisahan tanggung jawab baca/tulis. **Bisa pakai satu tanpa yang lain.** Tapi CQRS Level 1 sangat cocok dengan Clean karena Command/Query Handler memang "Use Case" versi Clean.

**Kenapa senior minta ini (inferensi konteks):**
1. Integrasi CargoWise/SAP — memisahkan aturan integrasi dari cara memanggil pihak ketiga, jadi saat jalur berubah logika tidak dirombak
2. Kalau ada ledger/finansial — write model ketat, read model cepat
3. Standar kode tim — engineer pindah proyek tanpa belajar ulang

**Rencana belajar 3 minggu:**
- Minggu 1: baca artikel asli (Palermo, Uncle Bob, Fowler, Greg Young) — pahami, jangan bikin dulu
- Minggu 2: bikin satu modul kecil sendiri, **ukur sendiri biaya boilerplate-nya**
- Minggu 3: refactor satu modul berantakan di kode kerja

**5 pertanyaan untuk senior:**
1. Untuk modul CRUD murni, tetap full layer atau boleh lebih tipis?
2. CQRS sampai level berapa — pisah handler atau pisah read model fisik?
3. Kalau read model terpisah, konsistensi di UI ditangani bagaimana?
4. Ada rencana ke event sourcing, atau CQRS saja?
5. Transaksi lintas aggregate ditangani di mana?

---

## 7. MDM vs Hubstaff

**Pertanyaan:** *"Apa bedanya MDM dan Hubstaff?"* → lalu *"Microsoft intune, itu yang dipakai"*

**Temuan penting: MDM punya DUA arti yang tidak berhubungan.**

| Arti | Bidang | Produk |
|---|---|---|
| **Mobile Device Management** | IT/Security | Intune, Jamf, Workspace ONE |
| **Master Data Management** | Data/Enterprise Arch | SAP MDG, Informatica MDM, Stibo STEP |

Karena yang dipakai **Intune**, berarti arti pertama.

**Intune (dari dokumentasi resmi Microsoft):**
- Cloud-based endpoint management — enroll, konfigurasi, amankan, update perangkat, distribusi aplikasi
- Platform: Android, iOS/iPadOS, Linux, macOS, tvOS, visionOS, Windows
- **Dua mode:** MDM (seluruh device, bisa di-wipe) dan MAM (hanya aplikasi kerja, khas BYOD)
- **Tiga pilar:** identitas (Entra ID), perangkat, aplikasi
- Postur perangkat mengalir balik ke **Conditional Access**
- **Setiap aksi admin center = panggilan Microsoft Graph API** → semua bisa diotomasi
- Intune **tidak** menyimpan identitas & tidak melakukan autentikasi

**Hubstaff (dari FAQ resmi):**
- Employee time-tracking + screenshots + activity monitoring + reporting + automated payments
- Screenshot acak **~tiap 10 menit** (paket berbayar)
- Merekam URL & aplikasi, lokasi (mobile)
- **Activity rate per detik:** gerakan mouse/ketikan = active; tidak ada keduanya = inactive
- 5 menit tanpa aktivitas → status idle
- Ada opsi **silent app**

**Kritik penting:** yang diukur adalah **gerakan mouse & keyboard, BUKAN output pekerjaan**. Backend engineer yang 40 menit berpikir lalu menulis 30 baris yang menyelesaikan masalah besar akan terlihat "kurang aktif".

**Perbandingan:**

| Aspek | Intune | Hubstaff |
|---|---|---|
| Tujuan | Keamanan & kontrol perangkat | Mengukur waktu & aktivitas kerja |
| Pemilik | IT/Security | Ops/HR/Management |
| Objek | Device & aplikasi | Karyawan |
| Level | Infrastruktur | Aplikasi di atasnya |

**Hubungan keduanya:** Hubstaff punya FAQ khusus soal company-owned devices + opsi silent app. Pola umum: **Intune mendistribusikan & mengonfigurasi Hubstaff** ke semua laptop — karyawan tidak bisa uninstall, setting seragam, bisa di-wipe kalau hilang.

> Bukan "Intune vs Hubstaff". Yang benar: **Intune mengatur perangkat, Hubstaff memantau kerja di dalamnya.**

**Catatan privasi:** memantau perangkat milik perusahaan pada jam kerja = legal & wajar. Tracking di perangkat pribadi tanpa persetujuan = masalah. Di Indonesia masuk **UU PDP No. 27/2022**.

**Praktis:** jangan simpan file pribadi di laptop kerja (bisa di-wipe remote); pakai laptop kantor kalau ada opsi BYOD; kalau ditegur karena activity rate rendah padahal output beres, bawa bukti output; komunikasikan lebih awal soal deep work ke atasan.

---

## 8. CargoWise eAdaptor — riset lengkap

**Pertanyaan:** *"Research tentang cargowise eadaptor next dan edi mapping edi client dan middleware"*

Materi lengkap ada di file terpisah: [[CargoWise_eAdaptor_Integration_Notes]]

**Temuan kunci yang tidak obvious:**
1. eAdaptor **tidak aktif by default** — harus support request ke WiseTech
2. Dokumentasi developer **tidak publik** — hanya untuk pelanggan yang beli modul + NDA
3. Outbound cuma boleh **satu URL** untuk seluruh instance
4. Kirim pesan → dapat **tracking UUID**, bukan hasil. Status dicari manual di EDI Interchange
5. XUS mengandung **job costing & internal notes** → jangan pernah kirim mentah ke pihak ketiga
6. Modul Forwarding/Customs/Warehouse/Transport punya **object tree berbeda di skema XUS yang sama**
7. Legacy → Next = SOAP → REST + OAuth 2.0 client certificate (expire ~1 tahun)

---

## 9. eAdaptor vs eAdaptor Next

**Pertanyaan:** *"Apa perbedaan antara eAdaptor dan eAdaptor Next?"*

**4 perbedaan inti:**

| Aspek | Legacy | Next |
|---|---|---|
| **Transport** | SOAP + WSDL + kompresi | REST over HTTP, XML tanpa SOAP envelope |
| **Auth inbound** | Basic Auth (user/pass + clientId) | OAuth 2.0 + client certificate (CSR flow) |
| **Auth outbound** | Basic Auth | Basic Authentication |
| **Token** | — | JWT |
| **Multi-system** | Terbatas | Tiap sistem kredensial sendiri |
| **Sertifikat** | — | Ada, expire ~1 tahun |

**Pengecualian:** Basic Auth masih tersedia di Next **khusus instance on-premise**.

**Yang TIDAK berubah (sering disalahpahami):**
- ❌ Tetap async — tracking UUID, bukan hasil
- ❌ Tetap single outbound endpoint → relay tetap wajib kalau >1 konsumen
- ❌ Tetap XML — XUS/XUE & Native XML sama, mapping tetap berat
- ❌ Tetap butuh EDI Client + Workflow Template
- ❌ Tetap tidak aktif default

> Yang berubah = **cara konek & autentikasi**. Yang tidak berubah = **model pesan & keterbatasan operasional**. Dua hal berbeda.

**Implikasi praktis:** kalau bangun baru → langsung Next. Kalau migrasi → ubah transport layer, auth flow, **tambah monitoring expiry sertifikat** (paling sering dilupakan). XML mapping tidak perlu diubah.

**Catatan tenggat 2027:** konsultan menyebut legacy pensiun **Januari 2027**, tapi **tidak ada pengumuman resmi WiseTech** yang saya temukan. Yang resmi hanya pernyataan arah di halaman fitur: eAdaptor Next *"fully replaces SOAP for both inbound and outbound communication"*. Konfirmasi ke Account Manager sebelum dipakai untuk perencanaan.

---

## 10. Kenapa bukan webhook saja?

**Pertanyaan:** *"Humm, kenapa gak pke webhooks aja? apa kekurangan jika pke webhooks?"*

**Jawaban singkat:** CargoWise punya padanan webhook, tapi bukan webhook modern.

Kalimat persis dokumentasi Complect:
> *"The eAdaptor Outbound Service provides an equivalent to webhooks, sending messages out to a listening SOAP based service."*

**5 hambatan:**
1. **Body SOAP envelope berisi XML ter-gzip** — penerima harus parse SOAP → decompress → baru dapat XML
2. **Tidak bisa set Authorization header** — auth lewat SOAP body, bukan header. Config hanya 2 field: `eAdaptor Outbound Password` + `Outbound eAdaptor Service URL`
3. **Hanya SATU URL** untuk seluruh instance (`Maintain > System > Registry > eServices > eAdaptor > Outbound Service URL`) — tidak ada fan-out
4. **Tidak ada delivery guarantee per-konsumen** — tidak ada DLQ bawaan
5. **Tidak ada replay** — error di penerima = pesan hilang dari sisi kita

**Kelemahan webhook secara umum (berlaku bahkan untuk webhook modern):** fire-and-forget, penerima mati = pesan hilang, tidak ada backpressure, sulit di-debug, butuh signature verification, ordering tidak dijamin.

> Webhook bagus untuk notifikasi ringan. Bukan pengganti message queue yang andal.

**Apa yang berubah di Next:** klaim konsultan menyebut per-system channels menggantikan single endpoint (SFL Tech, Infologia). **Belum terverifikasi** — halaman outbound Complect masih menulis *"eAdaptor Next guidance is coming soon"*.

**Yang tetap tidak berubah meski Next:** payload tetap XML (bukan JSON), CargoWise tetap menentukan format, tetap butuh Workflow Template, tetap tanpa jaminan delivery setara message queue.

**Pola yang harus dibangun — relay milik sendiri:**
1. Terima & ACK cepat (<1 detik) — unwrap SOAP, simpan XML mentah
2. Klasifikasi — `UniversalShipment` / `UniversalEvent`
3. Antrikan per konsumen — message queue sungguhan (RabbitMQ/SQS/Azure Service Bus), **bukan cron + tabel DB**
4. Kirim dengan retry — budget independen per konsumen (3–5x, exponential backoff) + DLQ sendiri
5. **Routing rules di tabel subscription, bukan `if` statement** — konsumen baru = `INSERT`, bukan deploy

---

## 📌 Tindakan Lanjutan (belum dikerjakan)

- [ ] Konfirmasi ke akun manager WiseTech: apakah legacy eAdaptor benar pensiun Januari 2027
- [ ] Konfirmasi ke tim CW: instance cloud atau on-premise
- [ ] Konfirmasi ke tim CW: modul mana yang dipakai (Forwarding/Customs/Warehouse/Transport)
- [ ] Konfirmasi apakah ada akses read ke database CW (untuk tracking status)
- [ ] Konfirmasi apakah ada test/training instance
- [ ] Tanyakan ke senior: CQRS sampai level berapa yang diharapkan
- [ ] Mulai minggu 1 rencana belajar Clean Architecture + CQRS
- [ ] Kalau ada workshop lanjutan, catat topik & output-nya di sini

---

*Log dibuat 9 November 2026. Materi teknis lengkap dipisah ke dua file yang ditautkan di atas supaya tidak duplikatif.*
