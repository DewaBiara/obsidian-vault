# AI Admin Integration Spec — Villa Lateng Backend ("guest-api")

Untuk: **Thena** (Autonomous AI Agent, Hermes Agent) sebagai Operations & Admin Manager.
Dasar: pembacaan langsung kode repositori ini (commit `54304b0`, branch `feat/backoffice-expenses`).
Sumber kebenaran adalah kode Go di `internal/http`, `internal/db`, dan `migrations/`.

---

## 0. Temuan Kunci & Boundary Operasional Thena

1. **Tanpa Payment Gateway:** Pembayaran dicatat manual oleh staf via `PATCH /admin/bookings/:id`. Thena **tidak boleh** memverifikasi uang masuk secara sepihak; hanya mencatat setelah ada konfirmasi bukti transfer manusia.
2. **Tanpa Sinkronisasi OTA Dua Arah:** Airbnb berbasis impor CSV (`POST /admin/airbnb/import`). Risiko overbooking di OTA harus dimitigasi manual.
3. **Status Booking:** Hanya `confirmed | cancelled | no_show`. Tidak ada status `pending` atau `checked_in` di tabel bookings.
4. **Kebijakan Pajak:** Jangan menampilkan atau menghitung pajak pada kuotasi/pesan ke tamu (abaikan `tax_rate` dan `tax_idr` dari `/quote`).
5. **Autentikasi & Akun:** Jangan pakai `ADMIN_TOKEN` (terlalu berisiko/superadmin). Gunakan akun khusus `thena` dengan role `staff`, login via `POST /admin/login` dan cache JWT (12 jam).
6. **Privasi PII:** Thena tidak boleh mengakses file dokumen ID/paspor mentah tamu (`GET /admin/checkins/:id/file`).

---

## 1. Peta Endpoint Utama

- **Base URL Produksi:** `https://api-guest.villalatengubud.com` (atau loopback `http://127.0.0.1:4000` di VPS)
- **Ketersediaan & Kalender:**
  - `GET /availability` (Publik)
  - `GET /admin/calendar?from=YYYY-MM-DD&to=YYYY-MM-DD` (Staff)
  - `POST /admin/bookings/availability` (Staff dry-run)
  - `POST /admin/blocks` & `DELETE /admin/blocks/:id` (Staff)
- **Harga & Kuotasi:**
  - `POST /quote` (Publik, wajib buang field tax)
- **Lead & Inquiry:**
  - `GET /admin/inquiries` & `GET /admin/inquiries/:id`
  - `PATCH /admin/inquiries/:id`
  - `POST /admin/inquiries/:id/convert`
- **Manajemen Booking:**
  - `GET /admin/bookings`
  - `POST /admin/bookings`
  - `PATCH /admin/bookings/:id`
  - `PUT /admin/bookings/:id/villas`
