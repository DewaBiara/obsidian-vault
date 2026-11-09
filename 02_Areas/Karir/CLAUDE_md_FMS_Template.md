# CLAUDE.md — FMS Backend

<!--
CARA PAKAI
1. Copy isi file ini ke `CLAUDE.md` di root repo kerja. Kalau monorepo,
   taruh satu per service.
2. Isi semua penanda TODO dari kode/repo yang asli. Hapus komentarnya setelah diisi.
3. Untuk aturan yang hanya untukmu dan tidak layak dibagi ke tim, pakai
   `.claude/CLAUDE.local.md` (gitignored) — jangan CLAUDE.md.
4. Jaga file ini di bawah ~150 baris. Aturan yang tidak bisa dicek mesin, atau
   yang sudah ketebak dari kode, tidak perlu ditulis — malah bikin diabaikan.
5. Kalau file ini akan di-commit untuk tim, terjemahkan dulu ke Inggris.
   Kantor pusat OneByOne di Melbourne; repo bersama sebaiknya berbahasa Inggris.
-->

## Konteks

Repo ini adalah layanan backend untuk operasional freight forwarding.
CargoWise (WiseTech Global) adalah sistem inti FMS — repo ini adalah lapisan
integrasi dan layanan di sekitarnya, **bukan** pengganti CargoWise.

TODO — satu paragraf: tanggung jawab utama repo ini, dan hal yang secara eksplisit
TIDAK dikerjakan di sini. Contoh: "Repo ini menangani ingestion milestone dari
carrier, transformasi ke format internal, dan penyajian API ke klien. Repo ini
tidak menyimpan master data tarif dan tidak melakukan invoicing."

## Stack

- Runtime: TODO — versi .NET persis (`dotnet --version`)
- Bahasa: C# TODO
- Database: TODO — engine + versi
- Akses data: TODO — EF Core / Dapper / campuran; kalau campuran, sebutkan pembagiannya
- Cache / broker: TODO
- Arsitektur: TODO — Clean Architecture / vertical slice / CQRS+MediatR / lain
- Testing: TODO — framework + integration test pakai apa (Testcontainers? in-memory?)
- Deploy: TODO

## Perintah

```bash
dotnet build
dotnet test
dotnet run --project TODO
dotnet format
docker compose up -d
```

TODO — ganti dengan perintah yang benar-benar dipakai tim. Perintah yang salah di
sini lebih berbahaya daripada tidak ada sama sekali.

## Struktur

TODO — isi setelah melihat repo. 5–10 baris saja, tunjukkan folder penting + aturannya.
Hapus folder yang tidak ada di repo ini.

```
src/Api/            controller, middleware, DI wiring — tanpa logika bisnis
src/Application/    use case / handler, port interface
src/Domain/         entity, value object, aturan bisnis — tanpa dependency luar
src/Infrastructure/ EF Core, Redis, adapter eksternal, klien HTTP
tests/              unit + integration
```

## Glosarium Domain

Pakai istilah ini apa adanya. Jangan menerjemahkan, jangan mengganti nama class
domain yang sudah ada, jangan mengarang singkatan baru.

- **Shipment / Job** — unit kerja operasional. Di CargoWise disebut *Job*. Satu job
  biasanya satu shipment, tapi bisa punya beberapa leg.
- **Consol / Consolidation** — penggabungan beberapa shipment LCL ke satu kontainer.
- **MBL / HBL** — Master Bill of Lading (dari carrier ke forwarder) vs House Bill of
  Lading (dari forwarder ke shipper). HBL adalah dokumen kepemilikan barang.
- **MAWB / HAWB** — padanan MBL/HBL untuk angkutan udara; bersifat non-negotiable.
- **FCL / LCL** — kontainer penuh satu shipper / konsolidasi banyak shipper di CFS.
- **POL / POD** — Port of Loading / Port of Discharge.
- **CFS** — Container Freight Station, tempat stuffing/stripping LCL.
- **CBM** — meter kubik; dasar tarif. Laut 1 CBM = 1000 kg; udara 1 CBM = 167 kg.
  Yang ditagih adalah *chargeable weight* = nilai terbesar antara berat aktual dan
  berat volumetrik.
- **Incoterms** — FOB, CIF, DDP, EXW, dst. Menentukan pembagian biaya dan risiko.
- **UN/LOCODE** — kode lokasi 5 karakter (IDJKT, SGSIN, USLAX).
- **Demurrage / Detention** — biaya keterlambatan di pelabuhan / di luar pelabuhan.
- **Milestone** — peristiwa perjalanan kargo (gate in, loaded, departed, discharged…).
- **Consignee / Shipper** — penerima barang / pengirim barang.
- **XUS / XUE** — XML Universal Shipment / XML Universal Event, format pesan CargoWise.
- **eAdaptor** — gateway pertukaran data CargoWise (legacy SOAP; Next = REST + OAuth).

## Aturan Wajib

**Idempotency**
- Setiap endpoint yang menerima event/milestone dari luar WAJIB idempotent.
  Kunci dedupe dari event ID milik pengirim, bukan timestamp dan bukan hash body.
- Insert event dan pengecekan dedupe harus dalam satu transaksi atau pakai
  constraint unik di database. Jangan mengandalkan "cek dulu lalu insert" tanpa
  constraint — itu race condition.
- Pengiriman ulang dari carrier/CargoWise adalah hal normal, bukan anomali.

**State machine**
- Status shipment hanya boleh berubah lewat satu method domain (mis. `UpdateStatus`).
  Jangan pernah set property status langsung dari controller, handler, atau repository.
- Transisi ilegal harus melempar error domain, bukan diam-diam diabaikan.
- Kalau transisi valid tidak jelas dari kode, tanya — jangan mengarang urutan status.

**Uang dan kuantitas**
- Uang selalu `decimal`. Jangan pernah `double` atau `float`.
- Jangan bulatkan di tengah perhitungan; bulatkan sekali di batas output.
- Selalu sertakan mata uang eksplisit. Jangan asumsikan satu mata uang.
- Duplikasi job di CargoWise menimbulkan biaya transaksi nyata — perlakuan
  terhadap duplikat adalah keputusan bisnis, bukan sekadar bug teknis.

**Keamanan**
- Jangan pernah membaca, menampilkan, atau menulis ulang isi `.env`,
  `appsettings.*.json` yang berisi connection string, sertifikat `.pfx`/`.pem`,
  atau private key. Kalau butuh nilai konfigurasi, minta aku menaruhnya di
  User Secrets atau environment dan rujuk lewat nama variabel saja.
- Jangan pernah menuliskan nilai secret ke kode, test, komentar, atau log.
- Jangan pernah menjalankan `git add -A` atau `git commit`. Aku yang commit.
- Jangan pernah `git push --force`.
- Jangan menambahkan package NuGet tanpa bertanya lebih dulu.
- Log tidak boleh memuat data pribadi: nama shipper/consignee, alamat, nomor
  telepon, nilai barang, nomor dokumen. Log ID dan status, bukan isi payload.
- Jangan mematikan TLS verification, jangan menurunkan versi package ke yang
  punya CVE, jangan menambahkan endpoint debug.

**Gaya kode**
- Nullable reference types aktif. Jangan pakai `!` (null-forgiving) untuk
  menekan warning — selesaikan akar penyebabnya.
- Jangan pakai `#pragma warning disable` tanpa alasan tertulis di komentar.
- Setiap method `async` menerima `CancellationToken` dan meneruskannya ke bawah.
- Jangan menambah `try/catch` yang hanya melempar ulang atau menelan exception.
- Jangan mereformat file yang isinya tidak kamu ubah. Diff harus fokus pada
  perubahan logis — reviewer harus bisa membaca setiap baris.
- Migration database: jangan pernah mengubah migration yang sudah ada. Buat baru.

## Cara Bekerja

- Untuk tugas lebih dari satu file: **tunjukkan rencana dulu**, tunggu aku setujui,
  baru menulis kode.
- Setelah mengubah kode, sebutkan: file apa yang berubah, kenapa, dan bagian mana
  yang aku harus periksa manual.
- Kalau ada istilah domain, nama field, atau aturan bisnis yang tidak jelas dari
  kode: **tanya**. Jangan menebak lalu menyajikan tebakan sebagai fakta.
- Kalau kamu tidak yakin sesuatu ada di CargoWise atau tidak: bilang tidak yakin.
  Dokumentasi CargoWise tidak publik, jadi lebih baik mengaku daripada mengarang.
- Jangan menamai ulang hal yang sudah ada di kode lama hanya karena menurutmu
  namanya kurang tepat. Sebutkan sebagai saran, jangan langsung ubah.
- Kalau build atau test gagal, tunjukkan output aslinya. Jangan diringkas menjadi
  "sudah diperbaiki" tanpa bukti.
