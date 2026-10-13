# 🚀 CLAUDE CODE SPECIFICATION: PANTAU BBM BALI (LIVE QUEUE & TRAFFIC RADAR)

> **Document Type:** Production Architecture Blueprint & Implementation Handover  
> **Brand & Identity:** **PantauBBM Bali** (*"Radar Antrean & Stok SPBU Real-time Se-Bali"*)  
> **Author:** Thena (Hermes AI) for Dewa Biara  
> **Target Execution Agent:** Claude Code CLI (`claude -p` / interactive)  
> **Project Name:** `pantaubbm-bali`  
> **Primary Stack:** Go (Golang 1.22+ Worker & REST API), Redis (GEO & State Cache), SQLite/PostgreSQL, React + Vite + Tailwind + Leaflet/MapLibre (Mobile-First PWA)  
> **Zero-Cost External APIs:** OpenStreetMap Overpass (Seed Data), HERE Traffic API v7 (Bounding Box Flow, 250k free calls/mo)  

---

## 1. Executive Summary & Problem Framing

Krisis keterlambatan distribusi tanker BBM di Bali menyebabkan antrean kendaraan mengular ratusan meter hingga ke badan jalan raya di puluhan SPBU. Masyarakat membuang waktu 1–2 jam berkeliling tanpa kepastian stok.

Tantangan teknis utama:
1. **Sensor Traffic Murni Memiliki Blind Spot:** Jika SPBU kehabisan bensin, jalanan di depannya akan *sepi (kosong)*. Tanpa verifikasi stok, sistem traffic murni akan keliru mengira SPBU tersebut "Lancar & Siap Isi".
2. **Kemacetan Jalan Reguler vs Antrean SPBU:** Jalan arteri padat (misal Sunset Road / Bypass Ngurah Rai jam 18.00) selalu merah. Perlu algoritma *Delta Anomaly* untuk membedakan macet jalan umum vs antrean dispenser SPBU.

**Solusi:** **Hybrid Radar System** = *Automated Traffic Heuristic (HERE API)* dikombinasikan dengan *Geofenced 1-Tap Crowdsourced Validation* (konsensus warga di radius 300m).

---

## 2. System Architecture & Data Flow

```
[ OpenStreetMap (Overpass) ] 
         │ (One-time Seed / Daily Sync)
         ▼
[ Master SPBU Store (~180 SPBUs Bali) ] ── (Lat, Lon, Road Segment Bounding Box)
         │
         ▼
[ Go Ingestion Worker (Cron: 5 Min) ] ──> [ HERE Traffic API v7: bbox query ]
         │
         ▼
[ Heuristic Engine: JamFactor & Speed Delta Calculation ]
         │
         ▼
[ Redis Core State (GEOSEARCH + Key-Value + Expiring Votes) ]
         ▲
         │ (REST API / SSE)
[ Mobile PWA Frontend (Leaflet / MapLibre) ]
         │
         └── [ 1-Tap Geofenced User Report (Radius <= 300m) ]
```

---

## 3. Directory Structure

```
pantaubbm-bali/
├── cmd/
│   ├── api/
│   │   └── main.go                 # HTTP REST API server
│   └── worker/
│       └── main.go                 # Background traffic poller (HERE API BBox)
├── internal/
│   ├── config/                     # Env parser (HERE_API_KEY, PORT, REDIS_URL)
│   ├── domain/
│   │   ├── spbu.go                 # SPBU struct, TrafficStatus, StockStatus
│   │   └── report.go               # Crowdsource report model
│   ├── heuristic/
│   │   └── traffic_analyzer.go     # Speed ratio, JamFactor delta evaluator
│   ├── repository/
│   │   ├── redis_repo.go           # Redis GEO, status cache, rate limits
│   │   └── seed_repo.go            # Local JSON/SQLite master SPBU store
│   ├── service/
│   │   ├── spbu_service.go         # Query nearby, get overview list
│   │   └── report_service.go       # Validate geofence, submit crowd vote
│   └── traffic/
│       └── here_client.go          # HERE Traffic API v7 bbox client
├── web/                            # Mobile-First PWA (Vite + React + Tailwind)
│   ├── src/
│   │   ├── components/             # MapView, SPBUCard, ReportModal, FilterPills
│   │   ├── hooks/                  # useGeolocation, useSPBUData
│   │   ├── lib/                    # Leaflet map helper, distance formula
│   │   └── App.tsx
│   ├── package.json
│   └── vite.config.ts
├── data/
│   └── spbu_bali_master.json       # Pre-seeded coordinates of Bali SPBUs
├── scripts/
│   └── seed_overpass.py            # Python scraper to fetch Bali SPBUs from OSM
├── docker-compose.yml              # Redis + Go App
├── Dockerfile                      # Multi-stage Go build
├── Makefile
└── README.md
```

---

## 4. Algoritma Heuristik & Logika Status

### A. Algoritma Anomali Traffic (HERE Traffic API v7)
HERE mengembalikan data per segmen:
- `jamFactor`: Float 0.0 (lancar jaya) hingga 10.0 (deadlock/macet total).
- `currentSpeed` (km/h) & `freeFlowSpeed` (km/h).

Formula Indeks Antrean (*Queue Probability Score* $QPS$):
$$QPS = \min\left(10, \; \text{jamFactor} \times \left(1.0 - \frac{\text{currentSpeed}}{\text{freeFlowSpeed}}\right) \times 1.5\right)$$

* Rule Evaluasi:
  - $QPS < 3.0$ $\rightarrow$ **TRAFFIC_CLEAR** (Lancar)
  - $3.0 \le QPS < 6.5$ $\rightarrow$ **TRAFFIC_MODERATE** (Antre Sedang)
  - $QPS \ge 6.5$ $\rightarrow$ **TRAFFIC_JAMMED** (Antrean Meluber ke Jalan)

### B. Konsensus Komunitas (Anti-Troll & Geofence)
1. **Geofence Check:** User wajib share live browser location. Hitung jarak Haversine ke target SPBU. Jika `distance > 300m`, tolak vote (status `403 Geofence Exceeded`).
2. **Device / IP Cooldown:** 1 IP/User hanya bisa vote 1x per SPBU setiap 15 menit (Redis key `vote_lock:{spbu_id}:{client_ip}`).
3. **Status Override State:**
   - 🟢 **TERSEDIA & LANCAR:** Traffic QPS < 3.0 dan tidak ada laporan "Habis".
   - 🟡 **ANTRE SEDANG:** Traffic QPS 3–6.5 atau 2+ laporan antre.
   - 🔴 **ANTREAN PANJANG:** Traffic QPS > 6.5 atau 3+ laporan antre parah.
   - ⚫ **STOK HABIS / TUTUP:** Jika dalam window 20 menit ada $\ge 3$ laporan "BBM Kosong", status **OTOMATIS DI-OVERRIDE MENJADI KOSONG** terlepas apakah lalu lintas jalan di depannya hijau/sepi!

---

## 5. REST API Contract

### `GET /api/v1/spbus?lat=-8.65&lon=115.21&radius=10`
Mengambil SPBU terdekat berbasis lokasi pengguna (`radius` dalam km).

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": "spbu-54-803-08",
      "code": "54.803.08",
      "name": "SPBU Kapal Mengwi",
      "lat": -8.57721,
      "lon": 115.17641,
      "distance_meters": 1240,
      "status": "CROWDED", 
      "stock_status": "AVAILABLE",
      "pertalite": true,
      "pertamax": true,
      "solar": false,
      "jam_factor": 7.4,
      "last_updated": "2026-10-12T20:15:00Z",
      "crowd_reports_last_hour": {
        "lancar": 1,
        "antre": 8,
        "habis": 0
      }
    }
  ]
}
```

### `POST /api/v1/spbus/{id}/reports`
Submit status dari masyarakat.

**Payload:**
```json
{
  "lat": -8.57715,
  "lon": 115.17635,
  "status_vote": "HABIS", 
  "fuel_types_available": ["pertamax"],
  "note": "Pertalite baru saja habis jam 20:00"
}
```

---

## 6. Frontend Mobile PWA UI/UX Specification

- **Framework:** Vite + React + Tailwind CSS + Lucide Icons.
- **Peta:** MapLibre GL / Leaflet dengan OpenStreetMap tiles (CartoDB Positron / DarkMatter).
- **Marker Color System:**
  - 🟢 Hijau: Tersedia & Lancar (< 10 menit antre).
  - 🟡 Kuning: Antre 15–30 menit.
  - 🔴 Merah: Antre Horor (> 45 menit / meluber ke jalan raya).
  - ⚪ Abu-abu Gelap / Hitam: Stok Kosong / SPBU Tutup.
- **Bottom Sheet Drawer:**
  - Klik marker $\rightarrow$ Muncul drawer detail: Nama SPBU, Jarak dari user, JamFactor live, Tombol "Lapor Kondisi Ini", Tombol "Buka di Google Maps" (`geo:lat,lon`).

---

## 7. Phased Implementation Roadmap for Claude Code

### Fase 1: Data Seeding & Core Backend (Target: 3 Jam)
1. Buat script `scripts/seed_overpass.py` untuk mengunduh semua node & way `amenity=fuel` di batas provinsi Bali (-8.9 s/d -8.0 lat, 114.4 s/d 115.7 lon). Simpan ke `data/spbu_bali_master.json`.
2. Setup Go module `pantaubbm-bali` dengan arsitektur domain clean.
3. Implementasi `here_client.go` untuk menarik flow traffic via BBox Bali Selatan:
   - Endpoint: `https://data.traffic.hereapi.com/v7/flow?in=bbox:115.05,-8.85,115.35,-8.50&locationReferencing=shape&apiKey={KEY}`
4. Simpan status ke Redis (`GEOADD` + Hash state per SPBU).

### Fase 2: Crowdsource Engine & API (Target: 2 Jam)
1. Endpoint `GET /api/v1/spbus` dengan filter koordinat `lat`, `lon`, `radius`.
2. Endpoint `POST /api/v1/spbus/{id}/reports` dengan validasi geofence Haversine $\le 300\text{ m}$.
3. Logic aggregasi: 3 suara "HABIS" override traffic indicator.

### Fase 3: Frontend PWA UI (Target: 3 Jam)
1. Setup Vite React TypeScript di `web/`.
2. Pasang Leaflet / MapLibre dengan geolokasi otomatis.
3. Buat UI bottom drawer mobile-friendly, indikator warna real-time, dan modal submit status 1-klik.

---

## 8. Command Handover ke Claude Code CLI

Eksekusi build langsung menggunakan prompt berikut:

```bash
claude -p "Tolong inisialisasi dan bangun project 'pantaubbm-bali' sesuai dengan file blueprint /workspace/CLAUDE_CODE_PANTAU_BBM_BALI_SPEC.md. Mulai dari Fase 1 (scaffold project Go, fetch data SPBU Bali via OpenStreetMap/script, dan setup Redis model), lalu lanjutkan ke REST API dan frontend PWA." --allowedTools "Read,Write,Edit,Bash" --max-turns 25
```
