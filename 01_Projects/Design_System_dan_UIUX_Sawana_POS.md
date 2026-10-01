# 🎨 PANDUAN DESIGN SYSTEM & UI/UX SPESIFIKASI: SAWANA POS & BACKOFFICE

- **Inisiator & Pemilik:** [[Dewa Biara]]
- **Testbed Operasional:** [[02_Areas/Sawana_Coffee_Eatery]]
- **Tujuan:** Desain antarmuka kelas dunia yang memadukan kecepatan kasir (*ergonomic touch-first speed*) dengan elegansi analitik backoffice modern (Linear/Shadcn style).
- **Tautan Terkait:** [[01_Projects/CLAUDE_CODE_SAWANA_POS_SPEC]] | [[01_Projects/SaaS_Multi_Tenant_Architecture_Sawana_POS]]

---

## 1. Prinsip Desain Fundamental: Dua Dunia Berbeda

| Parameter | 1. POS Kasir (Tablet / Touch PWA) | 2. Backoffice Web (Desktop Admin) |
|---|---|---|
| **Konteks Penggunaan** | Kasir berdiri, pelanggan antre, buru-buru, jari berminyak/basah | Duduk santai di depan laptop, menganalisis angka dan laporan |
| **Ergonomi** | Touch-first, target sentuh minimal 48x48px (ideal 80px), zero nested dropdown | Mouse & Keyboard, keyboard shortcuts, dense data tables |
| **Color Scheme** | High-contrast (latar gelap/terang tegas agar terbaca di bawah lampu kafe) | Clean Modern SaaS (Slate/Zinc neutral, subtle border, aksen Emerald) |
| **Latency Feedback** | Instan (< 16ms), feedback haptik/audio saat tap item & kalkulasi | Asinkron dengan skeleton loading & optimistik UI |

---

## 2. Design System Tokens (Tailwind CSS)

- **Typography:**
  - Font Family: `Inter` atau `Geist` (angka tabular `font-mono tabular-nums` untuk nominal rupiah).
  - Cashier Price Display: `text-2xl font-bold tracking-tight`.
- **Palette Warna (Warm Coffee & Emerald Trust):**
  - Primary Accent: `Emerald-600` (`#059669`) untuk tombol BAYAR / Checkout (simbol uang masuk & sukses).
  - Neutral Background: `Zinc-900` / `Zinc-950` (Dark Mode kasir) atau `Zinc-50` / `White` (Light Mode).
  - Danger / Void: `Rose-600` (`#E11D48`) untuk Void, Refund, dan Pembatalan.
  - Warning / Stock Alert: `Amber-500` (`#F59E0B`) untuk stok bahan menipis.
  - Informational: `Blue-500` (`#3B82F6`) untuk Takeaway / Meja aktif.

---

## 3. UI Wireframe & Layout: POS Kasir (`apps/pos`)

Layarnya menggunakan **3-Pane Split (65% Katalog Menu : 35% Keranjang Transaksi)** pada resolusi tablet landscape (1024x768 atau 1280x800):

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ TOP BAR: [🏠 Sawana Coffee] [🟢 Online (Sync OK)] [Meja 04 ▼]        [👤 Dewa (PIN Lock)]│
├───────────────────────────────────────────────┬────────────────────────────────────────┤
│ KATALOG PRODUK (65% LEBAR LAYAR)              │ CART / STRUK TRANSAKSI (35% LEBAR)     │
│                                               │                                        │
│ [ Semua ] [☕ Coffee] [🍵 Non-Coffee] [🥐 Pastry]│ Order #SWN-102  •  Dine In (Meja 04)   │
│ ───────────────────────────────────────────── │ ────────────────────────────────────── │
│ ┌──────────────┐ ┌──────────────┐ ┌─────────┐ │ 1x Caffe Latte (Iced)         28.000   │
│ │ Caffe Latte  │ │ Cappuccino   │ │ American│ │    - Oat Milk (+10.000)                │
│ │ Rp 28.000    │ │ Rp 28.000    │ │ Rp 22.00│ │    - Less Sugar                        │
│ └──────────────┘ └──────────────┘ └─────────┘ │ 2x Butter Croissant           50.000   │
│ ┌──────────────┐ ┌──────────────┐ ┌─────────┐ │ ────────────────────────────────────── │
│ │ Matcha Latte │ │ Cold Brew    │ │ Toast B.│ │ Subtotal:                    88.000    │
│ │ Rp 30.000    │ │ Rp 32.000    │ │ Rp 35.00│ │ PB1 (10%):                    8.800    │
│ └──────────────┘ └──────────────┘ └─────────┘ │ Diskon Promo:                     0    │
│ ┌──────────────┐ ┌──────────────┐ ┌─────────┐ │ TOTAL:                    Rp 96.800    │
│ │ V60 Filter   │ │ Mineral Water│ │ Brownies│ │ (Font 32px Bold Hijau Emerald)        │
│ │ Rp 35.000    │ │ Rp 10.000    │ │ Rp 25.00│ │ ────────────────────────────────────── │
│ └──────────────┘ └──────────────┘ └─────────┘ │ [⏸️ Simpan Meja]  [✂️ Split Bill]      │
│                                               │ ┌────────────────────────────────────┐ │
│                                               │ │ 💰 BAYAR (Rp 96.800)               │ │
│                                               │ └────────────────────────────────────┘ │
└───────────────────────────────────────────────┴────────────────────────────────────────┘
```

### Fitur Interaksi Kasir Cepat:
1. **Modal Modifier Pop-up (Single-Tap):** Saat kasir men-tap "Caffe Latte", langsung muncul *bottom sheet / popover* pilihan varian (Hot / Iced) dan modifier (Oat Milk / Level Gula) dengan tombol radio button besar. Tap "Tambah" langsung masuk ke cart dalam < 0.2 detik.
2. **Numpad Pembayaran Tunai (Quick Cash):**
   - Saat kasir tap "BAYAR", muncul sheet pembayaran:
   - Tombol Uang Cepat: `[Uang Pas]` `[100.000]` `[150.000]` `[200.000]`.
   - Menampilkan nominal kembalian dengan font super besar (`Rp 3.200`) agar kasir tidak salah ambil uang receh di laci.
3. **QRIS Dinamis Full-Screen / CFD:**
   - Jika pilih QRIS, layar tablet menampilkan QR code besar (atau dikirim ke layar hadap pelanggan). Saat webhook status `settlement` diterima via WebSocket, layar otomatis berkedip hijau dan struk langsung tercetak.
4. **Fast Switch PIN Lock:**
   - Kasir cukup tap avatar di pojok kanan atas untuk mengunci layar ke 4-Digit Numpad. Barista lain cukup ketik 4 angka PIN mereka untuk langsung mulai shift atau melayani pesanan berikutnya.

---

## 4. UI Wireframe & Layout: Backoffice Owner (`apps/backoffice`)

Mengadopsi antarmuka modern ala **Linear / Vercel**:
- **Sidebar Navigasi (Kiri):**
  - Ringkasan: Dashboard (KPI Cards & Grafik)
  - Penjualan: Laporan Penjualan, Laporan Transaksi, Laporan Shift Kasir
  - Menu & Resep: Menu Library, Modifier, Kategori, Resep & Bahan Baku (BOM/HPP)
  - Inventaris: Kartu Stok, Purchase Order (PO), Mutasi Bahan, Stock Opname
  - Pegawai: Karyawan, Hak Akses, Matrix PIN Kasir
  - Pengaturan: Outlet, Profil Usaha, Billing SaaS, Printer & Meja
- **Header Atas:**
  - Dropdown Pilihan Outlet: `[Sawana Coffee & Eatery - Ubud ▼]` atau `[Semua Outlet]`.
  - Date Range Picker kalender interaktif.

### Tampilan Dashboard Utama:
- **Baris 1 (KPI Metrics):**
  - `Gross Sales`: Rp 12.450.000 (`+14.2%` vs kemarin)
  - `Net Sales`: Rp 11.200.000
  - `Total Transaksi`: 184 struk
  - `Average Basket Size`: Rp 60.869
  - `Gross Profit (Laba Kotor)`: Rp 7.840.000 (`69.8% Margin`) $\rightarrow$ *Ini fitur killer yang di Moka berbayar!*
- **Baris 2 (Visualisasi Tren):**
  - Line Chart tren penjualan per jam (melihat jam puncak/rush hour barista jam 09.00 - 11.00 dan 15.00 - 17.00).
  - Bar Chart top 5 menu terlaris (Caffe Latte Iced, Butter Croissant, Americano).

---

## 5. Komponen UI Library yang Direkomendasikan

Untuk mempercepat Claude Code membangun kedua web ini tanpa perlu membuat CSS dari nol:
- **Framework CSS:** Tailwind CSS v3 / v4.
- **Component Primitives:** **Shadcn UI** (Radix UI primitives).
- **Icons:** `lucide-react` (icon modern, konsisten, dan sangat ringan).
- **State Management:**
  - POS Tablet: `zustand` (untuk state cart, shift aktif, dan offline queue) + `idb` (IndexedDB wrapper).
  - Backoffice: `tanstack/react-query` (untuk server-state, caching, dan filtering tabel).
- **Charts:** `recharts` (responsif, mudah dikustomisasi tema dark/light).
