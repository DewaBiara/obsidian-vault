---
title: Analisis Penjualan Villa Lateng 2026
date: 2026-11-14
tags:
  - villa-lateng
  - revenue
  - analisis
  - hospitality
status: final
---

# Analisis Penjualan Villa Lateng 2026

Sumber data: `airbnb_reservations` (Airbnb, di-prorata per malam) + `booking_villas` (direct/PMS).
Database: `villa_guest` @ container `backend-villalateng-postgres-1` (prod `103.139.193.167`).

> **Catatan integritas data:** sinkronisasi Airbnb terakhir **2 & 4 November 2026**. Angka November dan Desember **belum final** — hanya booking yang masuk manual ke PMS yang tercatat (Des: Michelle, Royce, Brian, Auzar = Rp 24 Jt). Tabel `bookings` (PMS) sendiri baru terisi mulai 24 Agustus 2026, jadi Jan–Jul 2026 murni berasal dari Airbnb.

## Ringkasan Setahun

- **Gross revenue** (dibayar tamu): **Rp 363.334.500**
- **Payout bersih** (masuk rekening setelah fee): **Rp 317.606.620**
- **Fee platform**: Rp 45.727.880 (**12,6%**)
- Total malam terjual: 997 malam dari kapasitas 1.825 malam (5 unit × 365)

## Per Bulan

| Bulan | Malam | Okupansi | Payout (Rp) | Gross (Rp) | ADR (Rp) | RevPAR (Rp) |
|---|---|---|---|---|---|---|
| Jan | 45 | 29% | 9.399.169 | 11.352.306 | 208.870 | 60.640 |
| Feb | 41 | 29% | 8.805.159 | 10.634.878 | 214.760 | 62.894 |
| Mar | 69 | 45% | 14.039.244 | 16.956.635 | 203.467 | 90.576 |
| Apr | 90 | 60% | 18.946.288 | 22.883.330 | 210.514 | 126.309 |
| Mei | 109 | 70% | 26.035.621 | 31.445.883 | 238.859 | 167.972 |
| Jun | 108 | 72% | 22.547.336 | 27.118.157 | 208.772 | 150.316 |
| Jul | 109 | 70% | 26.004.620 | 31.408.436 | 238.574 | 167.772 |
| Agu | 126 | 81% | 34.645.444 | 40.753.785 | 274.964 | 223.519 |
| **Sep** | **133** | **89%** | **53.926.743** | 59.314.339 | 405.464 | 359.512 |
| Okt | 107 | 69% | 50.901.356 | 53.997.901 | 475.714 | 328.396 |
| Nov | 46 | 31% | 25.357.174 | 29.847.250 | 551.243 | 169.048 |
| Des | 20 | 13% | 26.998.466 | 27.621.600 | 1.349.923 | 174.184 |

## Per Unit (setahun penuh)

| Villa | Malam | Payout (Rp) | ADR (Rp) | Catatan |
|---|---|---|---|---|
| Emerald | 246 | 117.509.761 | 477.682 | Payout tertinggi |
| Lateng Signature | 291 | 103.302.880 | 354.993 | Volume tertinggi, paling stabil |
| Dolce Vita | 105 | 98.048.755 | 933.798 | **Menipu** — Rp 48 Jt dari Dee (flat 2 bln) |
| Sky Luxe | 176 | 92.660.101 | 526.478 | Pola long-stay sehat |
| Inspiration | 185 | 86.085.123 | 465.325 | — |

**Split kepemilikan:**
- Keluarga (Lateng, Sky, Dolce): **Rp 201.386.198**
- Koperasi (Emerald, Inspiration): **Rp 116.220.422**

## Temuan Utama

### 1. Kurva okupansi naik mulus lalu jatuh bebas
Jan 29% → Sep 89%, lalu Nov 31% dan Des 13%. Lonjakan Sep–Okt **bukan organik**: itu booking Dee dengan flat Rp 20 Jt/bulan (Sep blok 3–12 & 19–30, Okt penuh). Tanpa Dee, Sep–Okt setara Jun–Jul (~Rp 26 Jt/bulan).

### 2. Dolce Vita unit terlemah
Di luar Dee, Dolce hanya menghasilkan ~Rp 50 Jt dalam 10 bulan, dengan bulan kosong total: **Januari, Februari, September, November**. Bandingkan Sky Luxe: 176 malam → Rp 92,7 Jt dengan rate yang jauh lebih rendah per malam. Masalah Dolce bukan harga, tapi **malam kosong**.

### 3. ADR naik tapi volume tidak ikut
Jan–Jul ADR hanya Rp 200–240 rb/malam. Desember Rp 1,35 Jt/malam — tapi itu artefak dari sedikit malam (20 malam), bukan bukti pricing power. Bukti sebenarnya ada di RevPAR: Jan Rp 60.640 vs Sep Rp 359.512.

## Rekomendasi

1. **Dorong long-stay** bermodel Dee (flat bulanan) dan Charlie Collins di Sky (24 malam Airbnb) untuk mengisi **Nov–Feb** — musim dengan okupansi paling parah.
2. **Putuskan nasib Dolce Vita**: reposisi harga, atau jual permanen sebagai paket bulanan. Empat bulan nol dalam 10 bulan tidak bisa dibiarkan.
3. **Perbaiki sinkronisasi Airbnb** — data Nov/Des tidak lengkap, sehingga keputusan pricing musim ramai diambil tanpa angka penuh.
4. **Pantau RevPAR, bukan ADR.** ADR tinggi di bulan sepi hanya menandakan sedikit malam terjual dengan harga mahal.

## Glosarium

- **ADR (Average Daily Rate)** — pendapatan rata-rata per malam terjual = payout ÷ jumlah malam terjual. Mengukur *harga*, bukan *volume*.
- **Okupansi** — malam terjual ÷ malam tersedia.
- **RevPAR (Revenue per Available Room)** — payout ÷ seluruh malam tersedia. Menggabungkan harga × okupansi, jadi ini angka yang paling jujur untuk menilai performa unit.
- **Payout** — uang bersih yang masuk setelah dipotong fee platform.
- **Gross** — total yang dibayar tamu sebelum fee.
