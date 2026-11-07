#!/usr/bin/env python3
"""Hitung statistik jurnal trading dan regenerasi Dashboard_Trading.md.

Pakai:  python3 hitung_jurnal.py
Input:  trades.csv  (satu baris per trade)
Output: Dashboard_Trading.md + ringkasan di stdout

Kolom trades.csv:
  tanggal, kode, alasan_masuk, harga_beli, stop, target, lot,
  harga_keluar, tanggal_keluar, ikut_rencana
  - lot = jumlah lot (1 lot = 100 saham)
  - ikut_rencana = ya / tidak
  - trade belum ditutup: biarkan harga_keluar & tanggal_keluar kosong
"""
import csv
import os
import sys
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
TRADES = os.path.join(BASE, "trades.csv")
DASH = os.path.join(BASE, "Dashboard_Trading.md")

FEE_BELI = 0.0015   # 0,15%
FEE_JUAL = 0.0025   # 0,25% (termasuk PPh final 0,1%)
MODAL_AWAL = 2_000_000
TARGET_WR = 0.32    # break-even win rate di R:R 15:7


def num(v, default=None):
    v = (v or "").strip().replace("Rp", "").replace(".", "").replace(",", ".")
    if not v:
        return default
    try:
        return float(v)
    except ValueError:
        return default


def load():
    if not os.path.exists(TRADES):
        sys.exit(f"trades.csv tidak ditemukan di {TRADES}")
    with open(TRADES, newline="", encoding="utf-8") as f:
        return [r for r in csv.DictReader(f) if (r.get("kode") or "").strip()]


def main():
    rows = load()
    closed, open_pos = [], []

    for r in rows:
        beli = num(r.get("harga_beli"))
        lot = num(r.get("lot"))
        keluar = num(r.get("harga_keluar"))
        if not beli or not lot:
            continue
        saham = lot * 100
        modal = beli * saham
        rec = {
            "kode": r["kode"].strip().upper(),
            "tanggal": (r.get("tanggal") or "").strip(),
            "modal": modal,
            "ikut": (r.get("ikut_rencana") or "").strip().lower(),
            "alasan": (r.get("alasan_masuk") or "").strip(),
        }
        if keluar:
            pnl = keluar * saham * (1 - FEE_JUAL) - modal * (1 + FEE_BELI)
            rec.update({
                "keluar": keluar,
                "pnl": pnl,
                "ret": pnl / modal if modal else 0,
                "fee": modal * FEE_BELI + keluar * saham * FEE_JUAL,
            })
            closed.append(rec)
        else:
            open_pos.append(rec)

    # ---- statistik ----
    n = len(closed)
    wins = [t for t in closed if t["pnl"] > 0]
    losses = [t for t in closed if t["pnl"] <= 0]
    total_pnl = sum(t["pnl"] for t in closed)
    wr = len(wins) / n if n else 0
    avg_win = sum(t["pnl"] for t in wins) / len(wins) if wins else 0
    avg_loss = sum(t["pnl"] for t in losses) / len(losses) if losses else 0
    expectancy = (wr * avg_win) + ((1 - wr) * avg_loss) if n else 0
    rr = abs(avg_win / avg_loss) if avg_loss else 0
    be_wr = 1 / (1 + rr) if rr else 0
    total_fee = sum(t["fee"] for t in closed)
    patuh = [t for t in closed if t["ikut"] == "ya"]
    patuh_pct = len(patuh) / n if n else 0
    equity = MODAL_AWAL + total_pnl

    def rp(x):
        return f"Rp{x:,.0f}".replace(",", ".")

    lines = [
        "---",
        "tipo: dashboard-trading",
        f"diperbarui: {datetime.now():%Y-%m-%d %H:%M}",
        "---",
        "",
        "# Dashboard Trading",
        "",
        f"> Digenerate otomatis oleh `hitung_jurnal.py`. Jangan edit manual — ubah `trades.csv` lalu jalankan ulang.",
        "",
        "## Ringkasan",
        "",
        f"- Modal awal: **{rp(MODAL_AWAL)}**",
        f"- Equity sekarang: **{rp(equity)}** ({'+' if total_pnl >= 0 else ''}{total_pnl / MODAL_AWAL * 100:.2f}%)",
        f"- Trade ditutup: **{n}** ({len(open_pos)} posisi masih terbuka)",
        f"- Total P&L bersih (setelah fee): **{rp(total_pnl)}**",
        f"- Total fee terbayar: **{rp(total_fee)}**" + (" ⚠️ overtrade" if total_fee > abs(total_pnl) and n > 3 else ""),
        "",
        "## Metrik utama",
        "",
        f"- **Win rate: {wr * 100:.1f}%** (target break-even {be_wr * 100:.1f}%) "
        + ("✅ di atas break-even" if wr >= be_wr and n >= 10 else
           "⏳ sampel masih kecil" if n < 10 else "❌ di bawah break-even"),
        f"- Rata-rata profit: {rp(avg_win)}",
        f"- Rata-rata loss: {rp(avg_loss)}",
        f"- R:R rata-rata: **1 : {rr:.2f}**",
        f"- **Expectancy: {rp(expectancy)} per trade**",
        f"- Disiplin (ikut rencana): **{patuh_pct * 100:.0f}%** ({len(patuh)}/{n})",
        "",
    ]

    if n >= 10:
        if expectancy > 0:
            lines.append("> ✅ Expectancy positif. Fokus: pertahankan ukuran posisi, jangan naikkan risiko karena sedang menang.")
        else:
            lines.append("> ❌ Expectancy negatif. Jangan tambah modal. Periksa: apakah kerugian datang dari strategi atau dari tidak ikut rencana?")
    else:
        lines.append(f"> ⏳ Butuh {10 - n} trade lagi sebelum statistik bisa dipercaya. Jangan ambil kesimpulan dulu.")

    lines += ["", "## Posisi terbuka", ""]
    if open_pos:
        lines += ["| Kode | Tanggal | Modal | Alasan masuk |", "|---|---|---|---|"]
        for t in open_pos:
            lines.append(f"| {t['kode']} | {t['tanggal']} | {rp(t['modal'])} | {t['alasan']} |")
    else:
        lines.append("_Tidak ada._")

    lines += ["", "## Riwayat trade", ""]
    if closed:
        lines += ["| Kode | Tanggal | Modal | Keluar | P&L bersih | Return | Ikut rencana |",
                  "|---|---|---|---|---|---|---|"]
        for t in closed:
            mark = "✅" if t["ikut"] == "ya" else "❌"
            lines.append(f"| {t['kode']} | {t['tanggal']} | {rp(t['modal'])} | "
                         f"{rp(t['keluar'])} | {rp(t['pnl'])} | {t['ret'] * 100:+.1f}% | {mark} |")
    else:
        lines.append("_Belum ada trade yang ditutup._")

    lines += ["", f"Kembali ke [[Jurnal_Trading]] · [[Playbook_IPO_2026]]", ""]

    with open(DASH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Trade ditutup: {n} | Win rate: {wr * 100:.1f}% | Expectancy: {rp(expectancy)} | "
          f"Equity: {rp(equity)} | Disiplin: {patuh_pct * 100:.0f}%")
    print(f"Dashboard diperbarui: {DASH}")


if __name__ == "__main__":
    main()
