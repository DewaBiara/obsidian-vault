# Activity Tracker — Rencana (Plan Only)

Status: **rencana**, bukan spesifikasi implementasi.
Terakhir diperbarui: 7 November 2026.

Dokumen ini menjawab "apa yang dibangun, dalam urutan apa, dan kapan berhenti" —
bukan "bagaimana kodenya". Detail teknis ada di `Activity_Tracker_iOS_Ingest.md`.

---

## 1. Tujuan

Mengetahui ke mana waktu layar pergi, cukup akurat untuk bisa ditindaklanjuti,
tanpa menyerahkan data perilaku ke pihak ketiga.

**Ukuran keberhasilan (6 minggu):**
- Bisa menjawab "minggu ini berapa jam aku di sosmed vs kerja" tanpa menebak.
- Ada minimal satu keputusan nyata yang diambil berdasarkan data, bukan perasaan.
- Biaya marginal nol (pakai VPS yang sudah ada).

**Bukan tujuan:**
- Memblokir atau membatasi app. Ini tracker, bukan *parental control*.
- Membangun aplikasi native iOS/Android.
- Akurasi tingkat forensik. Cukup arah, bukan presisi detik.

---

## 2. Batasan yang Tidak Bisa Dinegosiasikan

| Batasan | Konsekuensi pada rencana |
|---|---|
| Apple memblokir data Screen Time mentah | Data iPhone hanya dari Shortcuts, **manual per app**. Tidak ada cara pintas. |
| Shortcuts hanya tangkap buka/tutup app | Tidak ada level URL. Tidak ada durasi dalam-app. |
| Sesi bisa putus tanpa event close | Butuh aturan cap durasi + penanda "sesi terbuka". |
| VPS 2 vCPU / ~1.9 GB / sisa disk ~5 GB | Tidak boleh menambah service berat. SQLite, bukan Postgres. |
| Host IPv4-only | Konfigurasi nginx tidak boleh `listen [::]`. |
| Pemilik tunggal | Harus bisa dioperasikan tanpa rasa sakit saat ditinggal berhari-hari. |

---

## 3. Kondisi Awal (sudah berdiri, bukan rencana)

Supaya jelas mana yang sudah ada dan mana yang belum:

- Service ingest aktif di VPS, auth token, penyimpanan SQLite.
- Reverse proxy nginx sudah melayani `/health`, `/ingest`, `/summary` via header Host.
- Laporan harian otomatis terdaftar untuk 21:30 WITA.
- **Belum bisa dipakai dari iPhone** karena DNS `activity.rikala.id` belum ada.
- Belum ada satu pun data nyata. Semua pengujian pakai data sintetis.

Artinya: fondasinya ada, tapi **nol data asli**. Rencana di bawah mengutamakan
mengumpulkan data asli dulu sebelum menambah fitur apa pun.

---

## 4. Fase 0 — Buka Jalan (½ hari)

Prasyarat teknis sebelum ada data.

**Pekerjaan**
- Daftarkan DNS `activity.rikala.id` → VPS.
- Terbitkan sertifikat TLS, aktifkan HTTPS.
- Rotasi token ingest (token lama sudah terekspos di chat).
- Verifikasi end-to-end: kirim satu event dari iPhone via Shortcuts, cek muncul di summary.

**Selesai bila:** satu event dari iPhone tercatat dan bisa dibaca.

**Keputusan yang dibutuhkan darimu:** DNS ditambahkan manual, atau beri akses
Cloudflare API agar saya urus.

---

## 5. Fase 1 — Pilot Data Asli (2 minggu)

Tujuan fase ini **bukan** membangun fitur. Tujuannya mengumpulkan data dan
menemukan apakah asumsinya benar.

**Pekerjaan**
- Daftarkan Shortcuts untuk **4–5 app saja**: Instagram, TikTok, YouTube,
  satu app chat, satu game yang paling sering.
- Jalankan laporan harian apa adanya. Jangan diubah selama pilot.
- Setiap Minggu malam: baca 7 laporan berturut-turut, catat tiga hal —
  1. Angka mana yang ternyata **tidak berguna**?
  2. Pertanyaan apa yang **tidak bisa dijawab** data yang ada?
  3. Berapa banyak event yang hilang (sesi terbuka / durasi 0)?

**Selesai bila:** 14 hari data terkumpul dan tiga pertanyaan di atas punya jawaban tertulis.

**Gerbang keputusan — di sini proyek bisa berhenti:**
Kalau setelah 2 minggu ternyata data terlalu bolong untuk dipercaya, atau kamu
tidak pernah membuka laporannya, **hentikan proyek**. Itu hasil yang sah dan
lebih murah daripada lanjut ke fase 2.

---

## 6. Fase 2 — Satu Tampilan yang Benar (1 minggu)

Baru dikerjakan setelah punya data asli, karena bentuk datanya belum diketahui.

**Pekerjaan**
- Satu halaman web read-only, bukan aplikasi: total per kategori, tren 7/30 hari,
  dan perbandingan minggu ini vs minggu lalu.
- Ditaruh di subdomain yang sama (atau path `/report`), akses berpagar token.
- Laporan Discord dipertahankan; dashboard hanya untuk melihat lebih dalam saat penasaran.

**Sengaja tidak dikerjakan:** filter interaktif, grafik realtime, multi-user, ekspor PDF.

**Selesai bila:** membuka halaman itu menjawab pertanyaan mingguan tanpa perlu bertanya ke bot.

---

## 7. Fase 3 — MacBook (1–2 hari, opsional)

Dikerjakan hanya kalau data iPhone dirasa tidak cukup.

**Pendekatan:** pasang ActivityWatch di Mac, arahkan ke server sendiri.
Tidak menulis tracker baru — ini menyelesaikan bagian Mac hampir gratis,
dan memberi level **judul jendela/URL** yang tidak dimiliki iPhone.

**Keputusan di gerbang fase:** apakah detail tambahan itu sepadan dengan
kompleksitas menjaga dua sumber data tetap konsisten?

---

## 8. Fase 4 — Android (ditunda)

Ditunda sampai ada perangkat Android yang benar-benar dipakai harian.
Android punya API resmi yang jauh lebih baik dari iPhone; kalau saatnya tiba,
ini pekerjaan beberapa hari, bukan berminggu-minggu.

---

## 9. Yang Sengaja TIDAK Dibangun

Daftar ini sama pentingnya dengan daftar pekerjaan.

- **Tracker native untuk iOS.** Tidak mungkin, bukan sulit.
- **Reverse engineering aplikasi pihak ketiga.** Untuk kasus ini terbukti buntu:
  data yang dicari tidak pernah keluar dari perangkat, jadi tidak ada yang bisa diambil.
- **Integrasi kalender, todo, atau habit tracker.** Satu masalah, satu alat.
- **Machine learning untuk klasifikasi.** Aturan berbasis pola cukup, dan bisa dibaca manusia.
- **Aplikasi mobile untuk melihat laporan.** Discord + satu halaman web sudah memadai.
- **Sinkronisasi realtime.** Laporan harian lebih berguna daripada angka live.

---

## 10. Risiko

| Risiko | Dampak | Rencana |
|---|---|---|
| Shortcuts berhenti jalan setelah update iOS | Data hilang diam-diam | Laporan menandai "sesi terbuka"; cek mingguan mendeteksi hari kosong |
| Terlalu banyak app didaftarkan | Capek mengelola, akhirnya ditinggalkan | Batasi 5 app sampai Fase 1 selesai |
| Data terlalu bolong | Kesimpulan salah | Gerbang Fase 1: berhenti kalau tidak dipercaya |
| Disk VPS penuh | Service mati | Retensi: event mentah 90 hari, ringkasan selamanya |
| Token bocor | Orang lain bisa menyuntik data palsu | Rotasi di Fase 0; token hanya di header, tidak di URL |
| Proyek jadi ajang bikin fitur | Waktu habis tanpa manfaat | Batas fase + gerbang berhenti eksplisit |

---

## 11. Ringkasan Urutan

```
Fase 0  DNS + TLS + rotasi token       ½ hari    ← prasyarat, belum ada data
Fase 1  Pilot 5 app, 14 hari           2 minggu  ← GERBANG: lanjut atau hentikan
Fase 2  Dashboard read-only            1 minggu
Fase 3  MacBook via ActivityWatch      1–2 hari  ← opsional
Fase 4  Android                        ditunda
```

**Prinsip yang dipegang:** kumpulkan data asli dulu, baru bangun tampilan.
Membangun dashboard sebelum tahu bentuk datanya adalah cara paling umum
menghabiskan seminggu untuk sesuatu yang tidak menjawab pertanyaan siapa pun.
