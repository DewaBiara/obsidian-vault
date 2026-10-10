# HANDOVER DOKUMEN: MIGRASI REBRANDING & DOMAIN
## KULA POS (`sawanaubud.com`) ➔ RIKALA POS (`rikala.id`)

> **Versi Dokumen:** 1.0  
> **Tanggal:** 7 Oktober 2026  
> **Target Entitas:** Rikala Tech (`rikala.id`)  
> **Target Produk:** Rikala POS (`pos.rikala.id` / `app.rikala.id`)  

---

## 1. Ringkasan Eksekutif & Tujuan Migrasi

Dokumen ini adalah panduan teknis dan operasional untuk melakukan migrasi menyeluruh dari penamaan dan infrastruktur lama:
* **Brand Lama:** KULA POS / Sawana POS
* **Domain Lama:** `kula.sawanaubud.com` (Landing Page) & `pos.sawanaubud.com` (Backoffice/API)
* **Brand Baru:** **RIKALA POS**
* **Domain Baru:** `rikala.id` (Landing Page/Portal), `app.rikala.id` (Backoffice), `api.rikala.id` (Backend API Engine)

---

## 2. Pemetaan DNS & Routing Cloudflare

Pastikan di Cloudflare (`rikala.id`), record DNS berikut diatur dengan status **Proxied (Orange Cloud)**:

| Type | Name | Content / Target | Proxy Status | Keterangan |
|------|------|------------------|--------------|------------|
| **A** | `@` (`rikala.id`) | `IP_SERVER_PRODUKSI` | Proxied | Landing page utama RIKALA |
| **CNAME** | `www` | `rikala.id` | Proxied | Redirect www ke root |
| **A** | `app` | `IP_SERVER_PRODUKSI` | Proxied | Web Backoffice Dashboard |
| **A** | `pos` | `IP_SERVER_PRODUKSI` | Proxied | Web/PWA POS Client (atau redirect ke `app`) |
| **A** | `api` | `IP_SERVER_PRODUKSI` | Proxied | Go REST API & Sync Gateway |

---

## 3. Checklist Perubahan Kode Sumber (Codebase)

### A. Backend (Go Clean Architecture)
1. **Environment Variables (`.env.production` / `config.yaml`):**
   ```bash
   # SEBELUMNYA:
   APP_ENV=production
   BASE_URL=https://pos.sawanaubud.com
   CORS_ALLOWED_ORIGINS=https://kula.sawanaubud.com,https://pos.sawanaubud.com
   COOKIE_DOMAIN=.sawanaubud.com
   REFRESH_COOKIE_NAME=kula_refresh

   # MENJADI:
   APP_ENV=production
   BASE_URL=https://api.rikala.id
   CORS_ALLOWED_ORIGINS=https://rikala.id,https://app.rikala.id,https://pos.rikala.id,capacitor://localhost,http://localhost:5173
   COOKIE_DOMAIN=.rikala.id
   REFRESH_COOKIE_NAME=rikala_refresh
   EMAIL_FROM_ADDRESS=halo@rikala.id
   EMAIL_FROM_NAME="Rikala POS"
   ```

2. **Cookie Middleware & Auth Handler:**
   * Ganti nama cookie dari `kula_refresh` menjadi `rikala_refresh`.
   * Atur `Domain: ".rikala.id"` agar cookie refresh token dapat diakses lintas subdomain (`app.rikala.id` dan `api.rikala.id`).
   * Tetap pertahankan atribut: `HttpOnly: true`, `Secure: true`, `SameSite: http.SameSiteLaxMode`, `Path: "/api/v1/auth"`.

3. **Format Default Invoice Number:**
   * Di `core/domain/order.go` atau bootstrap invoice sequencer:
   * Ubah format default: `OUTLET/YYYYMMDD/DEVICE-SEQ` (contoh: `RKL/20261007/T1-0001`).

---

### B. Front-End Landing Page (`apps/landing` atau `rikala-web`)
1. **Copywriting & Tagline:**
   * **Title Tag:** `<title>Rikala POS: Kasir Offline-First untuk F&B di Bali</title>`
   * **Headline Utama:**
     ```
     Rikala internet putus?
     Kasir tetap jalan.
     ```
   * **Deskripsi:**
     > *"Rikala POS mencatat pesanan, mencetak struk, dan membuka laci kasir tanpa internet. Semua tersinkron otomatis begitu online kembali. Dibuat untuk F&B di Bali."*
2. **Environment Variables (`.env.production`):**
   ```env
   NEXT_PUBLIC_APP_NAME="Rikala POS"
   NEXT_PUBLIC_LOGIN_URL="https://app.rikala.id/login"
   NEXT_PUBLIC_API_URL="https://api.rikala.id"
   NEXT_PUBLIC_LEADS_URL="https://api.rikala.id/api/v1/leads"
   NEXT_PUBLIC_WHATSAPP_NUMBER="628970087058"
   ```
3. **OpenGraph & Media Sharing (Action Item dari Audit):**
   Tambahkan aset `og-banner.png` (1200x630) yang menampilkan logo RIKALA POS dan mockup tablet:
   ```html
   <meta property="og:title" content="Rikala POS: Internet putus? Kasir tetap jalan." />
   <meta property="og:description" content="POS offline-first untuk kafe dan resto di Bali. Tagihan meja, tiket dapur, PB1 & service charge otomatis." />
   <meta property="og:image" content="https://rikala.id/og-banner.png" />
   <meta name="twitter:image" content="https://rikala.id/og-banner.png" />
   ```
4. **Local Storage Keys:**
   * Ganti `kula-web-theme` ➔ `rikala-web-theme`
   * Ganti `kula-web-lead` ➔ `rikala-web-lead`

---

### C. Front-End Backoffice (`apps/backoffice`)
1. **Branding & Header UI:**
   * Ganti logo KULA menjadi logo RIKALA.
   * Ganti teks judul navbar & tab title menjadi `Rikala POS Backoffice`.
2. **Endpoint Base URL (`lib/api.ts` / Axios / Fetch Wrapper):**
   * Arahkan API requests ke `https://api.rikala.id` (atau relative path `/api/v1` jika di-reverse proxy di domain yang sama).
3. **Default Date Range Fix (Action Item dari Audit):**
   * Pastikan state default halaman laporan `/reports/*` langsung menginisialisasi parameter `from` dan `to` (format `YYYY-MM-DD`, e.g. hari ini atau 7 hari terakhir) agar tidak memicu error `422 VALIDATION_FAILED` saat pertama kali render.

---

### D. Front-End POS Client (`apps/pos` / Android Capacitor Wrapper)
1. **Metadata Aplikasi:**
   * Di `capacitor.config.json` / `manifest.json`:
     ```json
     {
       "appId": "id.rikala.pos",
       "appName": "Rikala POS",
       "webDir": "dist",
       "server": {
         "androidScheme": "https"
       }
     }
     ```
2. **IndexedDB Name:**
   * Migrasi atau gunakan nama database lokal: `rikala_pos_offline_db` (versi skema baru).
3. **Pairing & Bootstrap Endpoint:**
   * Default API base URL terminal: `https://api.rikala.id`.

---

## 4. Konfigurasi Reverse Proxy (Nginx)

File `/etc/nginx/sites-available/rikala.conf`:

```nginx
# 1. Landing Page (rikala.id)
server {
    listen 80;
    server_name rikala.id www.rikala.id;
    return 301 https://rikala.id$request_uri;
}

server {
    listen 443 ssl http2;
    server_name www.rikala.id;
    # SSL Managed by Cloudflare / Certbot
    return 301 https://rikala.id$request_uri;
}

server {
    listen 443 ssl http2;
    server_name rikala.id;

    # Security Headers
    server_tokens off;
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    location / {
        proxy_pass http://127.0.0.1:3000; # Port Landing Next.js
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https;
    }
}

# 2. Backoffice Dashboard (app.rikala.id)
server {
    listen 443 ssl http2;
    server_name app.rikala.id;

    server_tokens off;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Strict-Transport-Security "max-age=31536000" always;

    location / {
        proxy_pass http://127.0.0.1:3001; # Port Backoffice Next.js
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https;
    }
}

# 3. Backend API Gateway (api.rikala.id)
server {
    listen 443 ssl http2;
    server_name api.rikala.id;

    client_max_body_size 5M;
    server_tokens off;

    add_header X-Content-Type-Options "nosniff" always;
    add_header Strict-Transport-Security "max-age=31536000" always;

    location / {
        proxy_pass http://127.0.0.1:8080; # Port Go Backend binary
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https;
    }
}
```

---

## 5. Redirect & Deprecasi Domain Lama (`sawanaubud.com`)

Agar tautan lama dari mitra, kafe, dan tester tidak putus:
* Pasang HTTP 301 Permanent Redirect dari `kula.sawanaubud.com` ke `https://rikala.id`.
* Pasang HTTP 301 Permanent Redirect dari `pos.sawanaubud.com` ke `https://app.rikala.id`.

Konfigurasi redirect di Nginx:
```nginx
server {
    listen 443 ssl;
    server_name kula.sawanaubud.com;
    return 301 https://rikala.id$request_uri;
}

server {
    listen 443 ssl;
    server_name pos.sawanaubud.com;
    return 301 https://app.rikala.id$request_uri;
}
```

---

## 6. Prosedur Uji Verifikasi Pasca-Migrasi

1. **DNS Propagation:** Jalankan `dig +short rikala.id` dan `dig +short app.rikala.id` untuk memastikan resolved ke Cloudflare edge IP.
2. **Auth & Cookie Cross-Origin:** Login ke `https://app.rikala.id`, pastikan cookie `rikala_refresh` tersimpan dengan domain `.rikala.id` dan session refresh berjalan mulus.
3. **Terminal Pairing Test:** Generate pairing code di Backoffice baru, lalu redeem dari terminal test untuk memastikan token device terbit tanpa CORS error.
4. **Lead Form Test:** Submit lead di `https://rikala.id#daftar`, pastikan respon `202 Accepted` dan rate limiter bekerja.
