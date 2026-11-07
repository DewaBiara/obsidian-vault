---
tipo: trading-journal
modal_awal: 2000000
maks_posisi: 2
risiko_per_trade_persen: 30
mulai: 2026-11-07
---

# Jurnal Trading Saham — Modal Belajar Rp2.000.000

> [!warning] Aturan dasar
> Uang ini **terpisah total** dari kas Sawana dan dari dana cicilan KSP/KUR.
> Kalau habis, hidup tidak berubah. Tidak ada margin, tidak ada leverage, tidak ada day trading.

## Aturan eksekusi (tidak boleh dilanggar)

1. Maksimal **2 posisi** bersamaan × Rp600.000 = Rp1.200.000 (60% eksposur). Sisa Rp800.000 cash.
2. **Maksimal 1 trade baru per minggu** selama 8 minggu pertama.
3. Setiap trade **wajib dicatat sebelum eksekusi** di `trades.csv`. Kalau alasan masuk tidak bisa ditulis dalam satu kalimat, jangan beli.
4. **Trailing stop 12%**, aktif hanya setelah posisi **+10%** (jadi stop di break-even, bukan di −5%).
5. **Hard stop −7%** terpisah, untuk melindungi dari gap-down. Trailing stop tidak melindungi dari lompatan harga.
6. Kalau kena stop → keluar. Tidak ada "tapi prospeknya bagus".
7. Universe: saham **Rp100–600** (Rp600rb = 10–60 lot).

## Target tahun pertama: data, bukan uang

- **Break-even win rate** di R:R 15:7 = **32%**. Di bawah itu rugi, di atas itu ada edge.
- Target: 30 trade nyata, lalu ukur win rate, expectancy, dan R:R rata-rata.
- Expectancy realistis (WR 40%, +15%/−7%): **± +Rp8.200 per trade** → 30 trade ≈ +Rp250rb.
- Round-trip fee 0,4% (beli 0,15% + jual 0,25%) = Rp2.344 per posisi Rp586rb. Jangan overtrade.

## Cara pakai

Catat trade di `trades.csv`, lalu jalankan:

```bash
python3 hitung_jurnal.py
```

Skrip akan memperbarui [[Dashboard_Trading]] otomatis.

## Referensi

- [[Playbook_IPO_2026]] — cara membaca IPO & pipeline yang sedang berjalan
- [[Catatan_Belajar_Saham]] — materi Level 1–4

Lihat juga: [[Ide_Sistem_Early_Warning_Sentimen_Pasar]]
