# 🚢 CargoWise — Materi Lengkap Platform

**Tanggal riset:** 9 November 2026
**Konteks:** Onboarding Backend Engineer di OneByOne Logistical

**Terkait:**
- [[CargoWise_eAdaptor_Integration_Notes]] — sisi teknis integrasi (eAdaptor, EDI, middleware)
- [[Catatan_Onboarding_OneByOne]] — Clean Architecture/CQRS, SAP, MDM
- [[Log_Sesi_Onboarding_2026-11-09]] — log kronologis sesi belajar

> **Cara membaca dokumen ini:** bagian **fakta** bersumber dari laporan resmi WiseTech, halaman produk CargoWise, dan media industri (The Loadstar, Forwarder News). Bagian **opini/penilaian** diberi label. Angka yang berubah cepat (harga, jumlah agen AI) diberi tanggal.

---

## 1. Apa itu CargoWise

**CargoWise = platform logistics execution** untuk freight forwarder, customs broker, dan penyedia logistik — menjalankan forwarding, customs, warehouse, transport, dan finance dalam **satu database global**.

**Perusahaan pembuatnya:** WiseTech Global (ASX: WTC), didirikan di Sydney, Australia.

**Cara memahami posisinya:** ini bukan SaaS kecil. Ini infrastruktur — 24 dari 25 freight forwarder global teratas memakainya (klaim yang beredar luas di industri, dikutip SFL Tech). WiseTech sendiri menyebut melayani **lebih dari 20.000 perusahaan logistik** (laporan tahunan 2026) dan **47 dari 50 penyedia 3PL global teratas**.

---

## 2. Angka Kunci (FY26, tahun buku berakhir 30 Juni 2026)

Semua dari rilis ASX resmi WiseTech:

| Metrik | Nilai | Catatan |
|---|---|---|
| **Total revenue grup** | **$1.395,9 juta** | Naik 79% dari FY25 — termasuk akuisisi **e2open** |
| **Revenue CargoWise (produk)** | **$756,9 juta** | Naik 11% organik |
| **EBITDA yang dilaporkan** | $558,4 juta | Naik 46% |
| **Underlying EBITDA margin** | 46% | |
| **Belanja R&D** | **$340,7 juta** | ~24% dari revenue |
| **Produk enhancement 5 tahun** | **6.500+** | FY22–FY26, investasi >$1,1 miliar |
| **Pelanggan di Value Packs** | **>95%** | Model komersial baru per Desember 2025 |
| **Kenaikan sign-up SME baru** | ~55% | Sejak Value Pack diluncurkan |

> **Konteks penting:** angka revenue "naik 79%" itu **bukan pertumbuhan organik** — sebagian besar dari akuisisi e2open. Pertumbuhan organik CargoWise sendiri **11%**. Dua angka ini sering dikutip keliru di berita.

**Pesaing/mitra:** e2open (diakuisisi), VerifyWise (compliance), FRDM.ai (diakuisisi untuk supply chain compliance), Bolero (electronic Bills of Lading).

---

## 3. Modul Inti — Empat Pilar

CargoWise punya **216+ modul**, dibundel jadi Value Packs (tidak dijual terpisah).

### 3.1 Freight Forwarding

Jantung platform. Mencakup:
- **Export / Import / Domestic Forwarding** — Air, Sea, Rail, Road
- **Gateway / Transit / Transhipment / Cross Trade**
- **Consolidation Planning Board** — perencanaan konsolidasi
- **Forwarder-to-Forwarder eBookings** (Co-Loader/Wholesaler/NVOCC)
- **Detention/Demurrage/Storage Manager**
- **Container Transport Optimization** — optimasi transportasi darat ekspor
- **Electronic Bills of Lading** — integrasi Bolero untuk eMBL & eHBL

### 3.2 Customs & Compliance

- Deklarasi customs otomatis lintas yurisdiksi
- **Bonded Warehouse** — integrasi customs brokerage + operasi gudang
- **Electronic Certificate of Origin** — sertifikat asal digital
- **Global e-invoicing** — kepatuhan per negara (Jerman mulai 1 Jan 2027, Belgia sudah live, Polandia KSeF wajib)
- **VerifyWise** — screening compliance supply chain
- Kontrak pemerintah: **New Zealand Customs Service** dan komunitas dagang NZ

### 3.3 Warehouse — "Global Warehouse Suite"

Lima modalitas gudang (dari whitepaper resmi):
- **Warehouse PR** — berbasis Product/SKU (contract warehousing)
- **Warehouse TR** — transit warehouse (goods-in ke goods-out)
- **Bonded Warehouse**
- **Contract Warehouse**
- **Transit Warehouse**

### 3.4 Land Transport

- **TMS** — transport management, workflow automation, real-time visibility
- **Container Transport Optimization** — kurangi empty movement
- **Parcel** — B2B & B2C final-mile

### Modul pendukung
Finance (job costing, billing, AR/AP, WIP, accrual), Rates, Workflow, Compliance, Visibility, Enterprise.

---

## 4. CargoWise Neo — Portal Customer

**Apa itu:** aplikasi web untuk **customer dari forwarder** (shipper mereka) — bukan untuk operator.

Fitur: tracking shipment real-time, akses dokumen, manajemen booking, alert milestone proaktif, koordinasi quote & booking, customs declaration.

**Kenapa relevan untuk integrasi:** kalau klien minta "portal tracking", Neo sudah menyediakannya. Membangun portal sendiri biasanya keputusan yang salah — kecuali ada kebutuhan yang Neo tidak penuhi.

> ⚠️ **Web Tracker lama dijadwalkan dihapus 1 April 2026**, digantikan Neo sebagai platform utama (sumber: Carguber). Kalau menemukan dokumentasi yang masih menyebut Web Tracker, itu sudah usang.

**CargoWise Next** — versi generasi berikutnya, masih beta per diskusi komunitas. Neo jadi web tracker default di dalamnya.

---

## 5. CargoWise AI — ini yang paling berubah cepat

### Target resmi WiseTech
Dari halaman `cargowise.com/ai`: **"cut our customers' labor costs in half"** — target penghematan biaya tenaga kerja **hingga ~50%**.

### Enam agen yang sudah live (per 4 September 2026, menurut The Loadstar)

| Agen | Fungsi |
|---|---|
| **SARA** (Smart Auto Request Agent) | Baca email & dokumen masuk, identifikasi info yang hilang/tidak terbaca, **menghubungi importer/exporter langsung** minta klarifikasi, kembalikan data lengkap ke operator |
| **Auto Job Creation** | Daftarkan job di CargoWise Next, ingest e-docs & baris commercial invoice, picu klasifikasi & compliance check |
| **Product Research Agent** | Riset produk untuk workflow customs — jam pencarian jadi detik |
| **Document Management Portal** | Capture, validasi, map data dari dokumen dagang |
| **Invoice Processing Portal** | Ekstrak supplier, jumlah, referensi job dari invoice via email |
| **ACE** | Panduan real-time di dalam CargoWise — "seperti ada expert CargoWise di sampingmu" |

### Yang masih "coming soon" (dari cargowise.com/ai)
Automated Job Registration Agent · Operational Intelligence Agent · Document Validation Agent · Rate Ingestion & Validation Agent · Logistics & Trade Document Ingestion Agents · Workflow Execution & Reasoning Agent · Document Readiness Agent · Tracking Automation & Resolution Agent · Receivables Collections Agent

### ⚠️ Yang perlu dicatat soal monetisasi AI

Dari riset Citi (1 Oktober 2026) yang dilaporkan The Loadstar: **WiseTech berencana menagih agen AI secara terpisah dari Value Pack.**

- CEO Zubin Appoo: *"Six powerful agentic capabilities are currently available to customers through CargoWise Value Packs"* — tapi tidak menyebut apa yang akan datang
- WiseTech belum mengumumkan agen mana yang akan berbayar, berapa harganya, atau kapan mulai
- Citi memperkirakan >$30 juta dari tambahan revenue semester kedua harus datang dari agen AI + VerifyWise

**Implikasi praktis:** kalau perusahaan merencanakan ROI berbasis agen AI, **kunci dalam kontrak tertulis** apa yang termasuk dan apa yang akan berbayar. Halaman Value Pack punya daftar produk yang ditagih terpisah — **agen AI belum ada di daftar itu**. Itu celah yang perlu ditutup.

### Penilaian (opini, bukan fakta)
Dari FreightMynd (pesaing, jadi baca dengan sadar bias): *"No forwarder has publicly rated either one"* — belum ada review publik independen untuk agen-agen ini. WiseTech juga menyatakan forwarder/broker tetap menanggung **liabilitas** kalau agen salah.

---

## 6. Model Komersial — Value Packs

### Perubahan besar: Desember 2025

Sebelumnya: bayar per **user seat** + cloud services.
Sekarang: bayar per **transaksi**.

| Komponen | Kisaran | Catatan |
|---|---|---|
| **Per-transaction fee** | **$2,63 – $19,95** per job | Tergantung jenis & permutasi shipment (pernyataan CEO Zubin Appoo) |
| Full import container + inland leg | $19,95 | Forwarding + transport leg |
| Standalone customs entry | $9,95 | Customs saja |
| **Per user** | **$0** | Unlimited users |
| Cloud hosting | Termasuk | |
| Training individual | Termasuk | WiseTech Academy |
| Implementasi (professional services) | **$200K – $2M** | 3–12 bulan |
| Custom integration development | **Tidak termasuk** | Ini kerja kita |

> Angka implementasi & TCO dari `checkthat.ai` — **estimasi pihak ketiga**, bukan daftar harga resmi WiseTech.

### 📌 Kenapa model ini penting untuk kamu sebagai engineer

**Konsekuensi arsitektur langsung:** karena biaya per transaksi, **setiap job yang dibuat adalah uang**. Ini mengubah cara berpikir:

- Bug yang membuat job duplikat = **biaya nyata**, bukan cuma data kotor
- Testing yang membuat job dummy di production = tagihan
- Sistem retry yang agresif tanpa dedupe = tagihan berlipat
- Idempotency bukan "praktik baik" — ini **kontrol biaya**

Ini alasan tambahan kenapa relay dengan dedupe (lihat [[CargoWise_eAdaptor_Integration_Notes]]) bukan kemewahan arsitektur.

Laporan awal 2026 menyebut kenaikan biaya 20–50% bagi sebagian pelanggan setelah transisi (sumber: GoFreight, pesaing — perlakukan sebagai klaim kompetitor).

---

## 7. Reputasi & Kritik — ini yang perlu kamu tahu

### Rating (per 2026)

| Platform | Rating | Jumlah review |
|---|---|---|
| **G2** | **4,3** | 35 |
| **Capterra** | **2,9** | 32 |
| **Software Advice** | 2,9 | 32 |
| **Gartner Peer Insights** | 3,2 | 2 |

**Kenapa berbeda jauh?** G2 cenderung diisi reviewer enterprise; Capterra/Software Advice lebih banyak UKM dan implementasi yang tidak mulus.

### Kritik yang berulang

**1. Kurva belajar sangat curam**
Dari r/CargoWise: *"it is so complex that most people only learn the hard minimum of what they need in order to get by, and rely on cou[rses]"*

**2. Customer service lemah**
Capterra mencatat skor Customer Service **1,9**. Keluhan: *"Support requests tend to get shut down straightaway"*

**3. Biaya naik**
Keluhan paling sering di Reddit: kenaikan harga.

**4. Implementasi panjang & mahal**
3–12 bulan, $200K–$2M (estimasi pihak ketiga).

**5. Dokumentasi developer tidak publik**
Ini yang paling relevan untuk kita — lihat bagian 8.

### ⚖️ Penilaian seimbang

**Yang benar-benar unggul:**
- **Single database global** — setiap shipment, customs entry, invoice ada di satu sistem lintas cabang/negara/entitas
- **Kedalaman compliance** — ini yang paling sulit ditiru pesaing
- **Job costing & margin analysis native** — CFO bisa lihat profitabilitas per klien/lane/cabang secara live
- **Network effect** — 24 dari 25 forwarder teratas memakainya; integrasi antar-CargoWise user lebih mudah

**Yang benar-benar lemah:**
- Pengalaman developer (dokumentasi tertutup, tooling tua)
- Kompleksitas yang membuat adopsi setengah-setengah jadi norma
- Dukungan pelanggan yang tidak sebanding dengan harga

**Kesimpulan jujur:** CargoWise menang karena **kedalaman domain & jaringan**, bukan karena pengalaman pengguna atau developer. Kalau kamu datang dari dunia Stripe/Twilio di mana DX itu produk, ini akan terasa seperti mundur satu dekade. Itu bukan bug — itu konsekuensi model bisnisnya.

---

## 8. Kenapa Integrasi ke CargoWise Terasa Berat

Ini ringkasan sebab-sebab struktural (detail teknis di [[CargoWise_eAdaptor_Integration_Notes]]):

**1. Dokumentasi developer tidak publik.**
`eAdaptor Developers Guide` hanya tersedia **setelah** pelanggan membeli modul eAdaptor. Partner harus tanda NDA. Artinya: **commit dulu, baru boleh belajar.** Tidak ada `docs.cargowise.com` dengan referensi API publik.

**2. Tooling-nya generasi sebelumnya.**
SOAP, XML dengan skema raksasa, autentikasi Basic/Basic-dalam-SOAP, konfigurasi lewat UI registry, tanpa webhook modern. Alternatif open source yang ada semuanya tidak resmi.

**3. Model bisnisnya konsultan, bukan self-serve.**
Implementasi $200K–$2M berarti onboarding bukan lewat baca dokumentasi, tapi lewat orang. Ini desain sengaja, bukan kelalaian.

**4. Setiap instance bisa berbeda.**
Dari dokumentasi Complect: *"Behavior differences can occur between different instances of CargoWise based on a client's system configuration."* Artinya tutorial online tidak selalu berlaku di instance-mu.

**5. Skema raksasa, object tree bercabang.**
Universal XML mencakup forwarding, customs, warehouse, transport, accounting — masing-masing punya object tree sendiri di dalam skema yang sama.

### Implikasi untuk strategi belajarmu

Karena dokumentasi publik tipis, **sumber belajar terbaik justru**:
1. **Instance CargoWise itu sendiri** — minta akses ke test/training environment, eksplorasi transaksinya
2. **`eAdaptor Developers Guide`** — minta dari admin CargoWise perusahaan (mereka punya aksesnya)
3. **EDI Interchange** — lihat pesan nyata yang sudah lewat, itu dokumentasi terbaik yang ada
4. **Library open source** — baca kode `SteeleConsulting/cargowise-eadapter` untuk memahami perilaku SOAP yang tidak terdokumentasi
5. **Komunitas**: r/CargoWise (sparse tapi ada praktisi), docs Complect, ebook CargoMode

---

## 9. Lanskap Kompetitif (ringkas)

| Alternatif | Posisi |
|---|---|
| **GoFreight** | Menyerang harga & model per-user; menyebut CargoWise naik 20–50% pasca-Value Pack |
| **cargo.one** | Booking platform, bukan pengganti penuh |
| **Descartes / e2open** | e2open sudah diakuisisi WiseTech |
| **Magaya, Logitude, Consignly** | Segmen UKM |

> Catatan: sumber perbandingan ini sebagian dari pesaing. Untuk perencanaan nyata, validasi sendiri.

---

## 10. Yang Perlu Kamu Tanyakan / Pelajari Berikutnya

**Tentang instance perusahaan:**
- [ ] CargoWise cloud atau on-premise?
- [ ] Modul mana yang aktif — Forwarding, Customs, Warehouse, Land Transport, Parcel?
- [ ] Sudah eAdaptor Next atau masih legacy?
- [ ] Value Pack apa yang dipakai? Berapa volume transaksi/bulan? (menentukan skala)
- [ ] Ada test/training instance terpisah?
- [ ] Punya akses ke `eAdaptor Developers Guide`?

**Tentang peran:**
- [ ] Integrasi apa yang jadi prioritas pertama?
- [ ] Ada middleware existing (Complect Relay, Chain.io, custom) atau membangun dari nol?
- [ ] Siapa admin CargoWise internal yang bisa generate certificate & set EDI Client?
- [ ] Apakah klien minta portal custom, atau cukup CargoWise Neo?

**Tentang belajar:**
- [ ] WiseTech Academy punya sertifikasi gratis — mana yang relevan untuk backend engineer?
- [ ] Ada akses ke environment untuk eksperimen?

---

## 11. Ringkasan Satu Halaman

> **CargoWise** = platform logistics execution dari **WiseTech Global** (ASX: WTC). Satu database global untuk forwarding, customs, warehouse, transport, finance.
> **Skala:** revenue produk $756,9 juta (FY26, +11% organik); grup $1.395,9 juta (+79%, termasuk akuisisi e2open). R&D $340,7 juta/tahun. 20.000+ perusahaan logistik.
> **Modul:** 216+, dibundel jadi **Value Packs**. Empat pilar: Forwarding, Customs, Warehouse, Land Transport.
> **Harga:** sejak Des 2025 **per transaksi** ($2,63–$19,95/job), **unlimited users**. Implementasi $200K–$2M (estimasi pihak ketiga).
> **⚠️ Biaya per transaksi = duplikasi job itu mahal.** Idempotency & dedupe adalah kontrol biaya, bukan cuma kebersihan data.
> **AI:** 6 agen live (SARA, Auto Job Creation, dll), target penghematan 50% labor. Rencana penagihan terpisah dari Value Pack — belum diumumkan detailnya.
> **Neo:** portal customer (bukan operator). Web Tracker lama dihapus April 2026.
> **Reputasi:** unggul di kedalaman domain & jaringan (24/25 forwarder teratas); lemah di DX, dokumentasi, dan dukungan. Rating G2 4,3 vs Capterra 2,9.
> **Untuk developer:** dokumentasi tidak publik, tooling SOAP/XML generasi lama, tiap instance bisa beda. Belajar terbaik dari instance + `eAdaptor Developers Guide` + EDI Interchange.

---

## Sumber

**Resmi WiseTech:**
- Rilis ASX FY26: `wisetechglobal.com/media/zzhkiu0t/wtc-fy26-asx-release.pdf`
- Laporan tahunan FY26: `wisetechglobal.com/media/4o1lj2yf/wisetech-global-2026-annual-report.pdf`
- Halaman AI: `cargowise.com/ai`
- Mega features: `cargowise.com/cargowise-mega-features`
- Neo: `cargowise.com/solutions/cargowise-neo`
- Value Pack features: `cargowise.com/cargowise-value-pack/...`
- Warehouse suite whitepaper: `cargowise.com/media/ggvljhf0/...`

**Media industri:**
- The Loadstar — liputan agen AI CargoWise (4 Sep 2026)
- Forwarder News — rencana penagihan agen AI (10 Okt 2026), mengutip riset Citi 1 Okt 2026

**Pihak ketiga / analis:**
- `checkthat.ai/brands/cargowise/pricing` — estimasi TCO (bukan harga resmi)
- `rfp.wiki` — agregasi rating lintas platform
- Complect Solutions docs — sumber terbaik untuk detail teknis eAdaptor
- SFL Tech, Carguber, Infologia, FreightMynd — konsultan/kompetitor, ada bias komersial

---

*Dibuat 9 November 2026. Harga dan fitur AI CargoWise berubah cepat — verifikasi ulang sebelum dipakai untuk keputusan anggaran.*
