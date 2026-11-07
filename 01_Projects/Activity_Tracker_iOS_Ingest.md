# Activity Tracker — iOS Screen Time Ingest

Webhook penerima event screen-time dari **iOS Shortcuts**, plus laporan harian otomatis ke Discord.

Dibangun 7 November 2026. In-house, tanpa SaaS, tanpa dependensi eksternal.

---

## Kenapa pendekatan ini

Apple **sengaja memblokir** akses ke data Screen Time mentah. `DeviceActivityReportExtension`
hanya boleh mengembalikan sebuah *view*, bukan angka — sudah dikonfirmasi berulang di
Apple Developer Forums. Ini berlaku untuk semua pihak, termasuk Opal, one sec, Jomo.

Satu-satunya jalur resmi untuk mendapat data per-app di iPhone: **Shortcuts Personal
Automation** dengan trigger `App → is opened` / `is closed`, lalu POST ke endpoint sendiri.

Konsekuensi yang harus diterima:
- Harus didaftarkan **manual per app** yang mau dipantau.
- Hanya menangkap transisi foreground; kalau app dibunuh sistem tanpa event close,
  sesi di-cap maksimal 6 jam (lihat `MAX_SESSION_S`).
- Level data = **nama app**, bukan URL/halaman. Tidak tahu "Instagram 2 jam" itu Reels atau DM.

---

## Arsitektur

```
iPhone (Shortcuts automation)
        │  POST /ingest  (JSON / form / query string)
        ▼
nginx (activity.rikala.id) ──► 127.0.0.1:8099
        │
        ▼
activity-ingest.service  (Python stdlib, systemd)
        │
        ▼
/opt/activity-ingest/activity.db  (SQLite, WAL)
        │
        ▼  read-only
cron Hermes 21:30 WITA ──► activity_report.py ──► Discord
```

---

## Komponen

| Path | Fungsi |
|---|---|
| `/opt/activity-ingest/server.py` | HTTP listener, auth, pairing open/close → sesi |
| `/opt/activity-ingest/activity.db` | SQLite: `sessions`, `raw_events` |
| `/etc/activity-ingest/env` | `INGEST_TOKEN`, `ACTIVITY_PORT`, `ACTIVITY_DB` — mode 600 root |
| `/etc/systemd/system/activity-ingest.service` | unit systemd, hardening + MemoryMax=128M |
| `/home/hermes/.hermes/scripts/activity_report.py` | laporan harian, watchdog mode |
| nginx `sites-available/activity.rikala.id` | reverse proxy, hanya expose /health /ingest /summary |

Sumber di workspace: `/workspace/activity-ingest/`.

---

## Kontrak API

### `POST /ingest`

Header wajib: `X-Ingest-Token: <token>`

Body fleksibel — semua format ini diterima:
```json
{"device":"iphone","app":"Instagram","event":"open","ts":1794064707}
```
```
?app=Instagram&event=open&device=iphone
```
```
app=Instagram&event=open          (form-encoded)
```
`ts` opsional (epoch detik). Default: waktu server.

Respons:
```json
{"ok": true, "action": "opened"|"closed"|"noop", "app": "Instagram", "duration_s": 1200}
```

### `GET /health`
Tanpa auth. Untuk monitoring.

### `GET /summary?date=YYYY-MM-DD`
Header `X-Ingest-Token` wajib. Default: hari ini (WITA).

```json
{"ok":true,"date":"2026-11-07","total_s":8640,
 "apps":[{"app":"Instagram","seconds":8340,"minutes":139,"sessions":3}],
 "open_sessions":[{"app":"TikTok","since":1794064914}]}
```

---

## Logika pairing

- `open` → tutup sesi terbuka sebelumnya untuk (device, app) sebagai orphan, buka sesi baru.
- `close` → tutup sesi terbuka terakhir; kalau tidak ada, kembalikan `noop` (bukan error).
- Durasi di-cap `MAX_SESSION_S` = 6 jam, mencegah satu sesi liar menghapus laporan sehari.
- Semua event mentah tetap disimpan di `raw_events` untuk audit / rebuild.

---

## Setup iPhone (Shortcuts)

Buat **dua automation per app**:

1. Shortcuts → tab **Automation** → **+** → **App**
2. Pilih app (mis. Instagram)
3. Centang **Is Opened** → **Next** → **New Blank Automation**
4. Tambah action **Get Contents of URL**
   - URL: `https://activity.rikala.id/ingest`
   - Method: `POST`
   - Headers: `X-Ingest-Token` = `<token>`
   - Request Body: **JSON**
     - `device` = `iphone` (Text)
     - `app` = `Instagram` (Text)
     - `event` = `open` (Text)
5. **Matikan** "Ask Before Running" supaya jalan otomatis
6. Ulangi untuk **Is Closed** dengan `event` = `close`

**Prioritas app yang dipantau:** Instagram, TikTok, YouTube, X/Twitter, dan game yang
paling sering dimainkan. Mulai dari 4–5 app dulu, jangan langsung semua.

---

## Laporan harian

Cron `a0a87b69078f`, 21:30 WITA, `no_agent` mode.

- Mengklasifikasi app ke: Sosmed, Game, Video/Hiburan, Chat, Kerja/Produktif,
  Belanja/Finansial, Browser, Lainnya.
- Menampilkan total, breakdown kategori + bar, top 5 app, dan **total distraksi**.
- **Watchdog:** kalau tidak ada data sama sekali, stdout kosong → Discord tidak dikirimi apa pun.

Jalankan manual:
```bash
sudo -u hermes python3 /home/hermes/.hermes/scripts/activity_report.py
sudo -u hermes python3 /home/hermes/.hermes/scripts/activity_report.py 2026-11-07
```

---

## Operasional

```bash
sudo systemctl status activity-ingest
sudo journalctl -u activity-ingest -f
sudo systemctl restart activity-ingest

# token
sudo grep INGEST_TOKEN /etc/activity-ingest/env
```

Uji dari VPS:
```bash
TOK=$(sudo grep INGEST_TOKEN /etc/activity-ingest/env | cut -d= -f2)
curl -s -X POST -H "X-Ingest-Token: $TOK" \
  'http://127.0.0.1/ingest?app=Test&event=open'
```

---

## Status per 7 Nov 2026

**Selesai & terverifikasi:**
- Service jalan, RAM ~14 MB, auth constant-time, hardening systemd aktif
- 4 format input teruji (JSON, form, query, text/plain)
- Pairing open/close benar; orphan handling benar; `noop` tidak error
- nginx proxy teruji via `Host:` header untuk /health, /ingest, /summary
- Laporan harian teruji dengan data demo & data kosong
- Cron harian terdaftar (`a0a87b69078f`)

**Menunggu (butuh aksi manual):**
- **DNS record `activity.rikala.id` → 103.179.57.42** belum ada. Zone `rikala.id`
  dikelola Cloudflare (`odin.ns.cloudflare.com`, `sureena.ns.cloudflare.com`), jadi
  tidak bisa ditambah tanpa API token atau dashboard.
- Setelah DNS aktif: jalankan certbot untuk sertifikat TLS, lalu aktifkan blok :443.
  Sampai itu selesai, `https://` belum bisa dipakai dari iPhone.

**Backlog:**
- Retensi: hapus `raw_events` > 90 hari, simpan `sessions` selamanya. Disk VPS tinggal ~5 GB.
- Dashboard web read-only (Next.js) — fase 2.
- Integrasi MacBook via ActivityWatch (`aw-server` di docker) → gabungkan ke laporan yang sama.
- Shortcut "buka tutup cepat": kalau `open` lalu `close` dalam < 3 detik, abaikan (kurangi noise).
