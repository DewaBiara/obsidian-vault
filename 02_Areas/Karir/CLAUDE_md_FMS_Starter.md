# CLAUDE.md

## Konteks

Backend untuk operasional freight forwarding. CargoWise (WiseTech Global) adalah
sistem inti FMS; repo ini adalah lapisan layanan dan integrasi di sekitarnya,
bukan pengganti CargoWise.

Stack: TODO — .NET version, database, EF Core/Dapper, Redis, test framework.

## Glosarium

Jangan menerjemahkan istilah ini, jangan mengganti nama class domain yang sudah ada,
jangan mengarang singkatan baru.

- **Shipment / Job** — unit kerja operasional. Di CargoWise disebut *Job*.
- **Consol** — penggabungan beberapa shipment LCL ke satu kontainer.
- **MBL / HBL** — Master B/L (carrier→forwarder) vs House B/L (forwarder→shipper).
  HBL adalah dokumen kepemilikan barang; MAWB/HAWB tidak.
- **FCL / LCL** — kontainer penuh satu shipper / konsolidasi banyak shipper di CFS.
- **POL / POD** — Port of Loading / Port of Discharge.
- **CFS** — Container Freight Station, tempat stuffing/stripping LCL.
- **CBM / chargeable weight** — laut 1 CBM = 1000 kg, udara 1 CBM = 167 kg; yang
  ditagih adalah nilai terbesar antara berat aktual dan berat volumetrik.
- **Incoterms** — FOB, CIF, DDP, EXW. Menentukan pembagian biaya dan risiko.
- **UN/LOCODE** — kode lokasi 5 karakter (IDJKT, SGSIN, USLAX).
- **Milestone** — peristiwa perjalanan kargo: gate in, loaded, departed, discharged.
- **XUS / XUE** — XML Universal Shipment / Event, format pesan CargoWise.
- **eAdaptor** — gateway pertukaran data CargoWise (legacy SOAP; Next = REST+OAuth).

## Aturan Wajib

**Idempotency**
- Endpoint yang menerima event dari luar WAJIB idempotent. Kunci dedupe dari event ID
  milik pengirim — bukan timestamp, bukan hash body.
- Pengecekan dedupe harus ditegakkan constraint unik di database atau satu transaksi.
  "Cek dulu lalu insert" tanpa constraint adalah race condition.
- Pengiriman ulang dari carrier/CargoWise itu normal, bukan anomali.

**State machine**
- Status shipment hanya berubah lewat satu method domain. Jangan set property status
  langsung dari controller, handler, atau repository.
- Transisi ilegal melempar error domain, tidak diabaikan diam-diam.
- Kalau urutan transisi tidak jelas dari kode: tanya, jangan mengarang.

**Uang dan kuantitas**
- Uang selalu `decimal`, tidak pernah `double`/`float`. Selalu sertakan mata uang.
- Bulatkan sekali di batas output, bukan di tengah perhitungan.
- Duplikasi job di CargoWise menimbulkan biaya transaksi nyata.

**Keamanan**
- Jangan membaca atau menulis ulang `.env`, `appsettings.*.json` berisi connection
  string, `.pfx`/`.pem`, atau private key. Kalau butuh nilai konfigurasi, rujuk lewat
  nama environment variable.
- Jangan menulis secret ke kode, test, komentar, atau log.
- Jangan `git add -A`, jangan `git commit`, jangan `git push --force`. Aku yang commit.
- Jangan menambah package NuGet tanpa bertanya.
- Log tidak boleh memuat nama shipper/consignee, alamat, nomor telepon, nilai barang,
  atau nomor dokumen. Log ID dan status, bukan isi payload.
- Jangan mematikan TLS verification, jangan menambah endpoint debug.

**Gaya kode**
- Nullable reference types aktif. Jangan pakai `!` untuk menekan warning.
- Jangan `#pragma warning disable` tanpa alasan tertulis.
- Setiap method `async` menerima dan meneruskan `CancellationToken`.
- Jangan menambah `try/catch` yang hanya melempar ulang atau menelan exception.
- Jangan mereformat file yang isinya tidak kamu ubah — diff harus fokus dan bisa
  dibaca baris per baris.
- Migration database: jangan mengubah migration lama, buat baru.

## Cara Bekerja

- Lebih dari satu file: tunjukkan rencana dulu, tunggu aku setujui, baru menulis kode.
- Setelah mengubah kode, sebutkan file yang berubah, alasannya, dan bagian mana yang
  harus aku periksa manual.
- Istilah domain, nama field, atau aturan bisnis yang tidak jelas dari kode: tanya.
  Jangan menyajikan tebakan sebagai fakta.
- Kalau tidak yakin sesuatu ada di CargoWise atau tidak: bilang tidak yakin.
  Dokumentasi CargoWise tidak publik — lebih baik mengaku daripada mengarang.
- Jangan menamai ulang hal yang sudah ada hanya karena menurutmu kurang tepat.
  Sebutkan sebagai saran.
- Build atau test gagal: tunjukkan output aslinya, jangan diringkas jadi "sudah diperbaiki".
