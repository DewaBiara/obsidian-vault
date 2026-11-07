#!/usr/bin/env python3
"""
Laporan harian Activity Tracker (iOS Shortcuts) untuk Discord.

Dijalankan oleh cron Hermes. Membaca SQLite langsung (read-only),
mengklasifikasikan app ke kategori, lalu mencetak laporan markdown.

Kalau tidak ada data sama sekali untuk hari ini -> cetak string kosong
supaya cron tidak mengirim apa-apa (mode watchdog).
"""

import os
import sqlite3
import sys
from datetime import datetime, timedelta, timezone

DB = os.getenv("ACTIVITY_DB", "/opt/activity-ingest/activity.db")
WITA = timezone(timedelta(hours=8))

# --- klasifikasi ------------------------------------------------------------
# Urutan penting: pola pertama yang cocok menang.
CATEGORIES = [
    ("Sosmed", r"instagram|tiktok|twitter|^x$|facebook|threads|snapchat|reddit|9gag|pinterest|linkedin|weibo|line|telegram"),
    ("Game", r"game|pubg|mobile legends|mlbb|free fire|codm|genshin|honkai|minecraft|roblox|clash|steam|valorant|dota|candy crush|among us"),
    ("Video/Hiburan", r"youtube|netflix|disney|spotify|vidio|viu|iqiyi|bilibili|twitch|prime video|apple tv"),
    ("Chat", r"whatsapp|telegram|messenger|discord|signal|wechat|kakaotalk"),
    ("Kerja/Produktif", r"vs ?code|visual studio|terminal|iterm|xcode|intellij|goland|postman|notion|slack|figma|excel|word|powerpoint|obsidian|github|hermes|datagrip|tableplus"),
    ("Belanja/Finansial", r"tokopedia|shopee|lazada|blibli|bukalapak|tiktok shop|gojek|grab|traveloka|bibc|mybca|bca|mandiri|brimo|pluang|ajaib|stockbit|bibit|investing"),
    ("Browser", r"safari|chrome|firefox|edge|brave|arc"),
]

IMPORT_RE = None


def classify(app: str) -> str:
    import re
    a = app.lower()
    for cat, pat in CATEGORIES:
        if re.search(pat, a):
            return cat
    return "Lainnya"


def fmt_dur(seconds: int) -> str:
    if not seconds:
        return "0m"
    h, m = divmod(int(seconds) // 60, 60)
    if h and m:
        return f"{h}j {m}m"
    if h:
        return f"{h}j"
    return f"{m}m"


def main():
    day_str = sys.argv[1] if len(sys.argv) > 1 else None
    if day_str:
        try:
            day = datetime.strptime(day_str, "%Y-%m-%d").replace(tzinfo=WITA)
        except ValueError:
            print(f"format tanggal salah: {day_str} (pakai YYYY-MM-DD)", file=sys.stderr)
            return 2
    else:
        day = datetime.now(WITA).replace(hour=0, minute=0, second=0, microsecond=0)

    start = int(day.timestamp())
    end = start + 86400

    if not os.path.exists(DB):
        print(f"database belum ada: {DB}", file=sys.stderr)
        return 1

    conn = sqlite3.connect(f"file:{DB}?mode=ro", uri=True, timeout=10)
    rows = conn.execute(
        "SELECT app, SUM(COALESCE(duration_s,0)) AS total, COUNT(*) AS n "
        "FROM sessions WHERE started_at >= ? AND started_at < ? "
        "GROUP BY app ORDER BY total DESC",
        (start, end),
    ).fetchall()
    open_now = conn.execute(
        "SELECT app, started_at FROM sessions WHERE ended_at IS NULL ORDER BY started_at DESC"
    ).fetchall()
    conn.close()

    if not rows:
        # watchdog: tidak ada data -> jangan kirim apa pun
        return 0

    total = sum(r[1] for r in rows)
    by_cat = {}
    for app, secs, n in rows:
        by_cat.setdefault(classify(app), 0)
        by_cat[classify(app)] += secs

    lines = [f"**📱 ACTIVITY REPORT — {day.strftime('%a, %d %b %Y')}**", ""]
    lines.append(f"**Total terpakai:** {fmt_dur(total)}")
    lines.append("")

    lines.append("**Per kategori**")
    for cat, secs in sorted(by_cat.items(), key=lambda x: -x[1]):
        pct = (secs / total * 100) if total else 0
        bar = "█" * max(1, round(pct / 10))
        lines.append(f"• {cat}: {fmt_dur(secs)} ({pct:.0f}%) {bar}")
    lines.append("")

    lines.append("**Top 5 app**")
    for app, secs, n in rows[:5]:
        lines.append(f"• {app} — {fmt_dur(secs)} ({n}× buka)")
    lines.append("")

    sosmed = by_cat.get("Sosmed", 0)
    game = by_cat.get("Game", 0)
    if sosmed + game > 0:
        lines.append(f"**Distraksi (sosmed + game):** {fmt_dur(sosmed + game)} "
                     f"({(sosmed + game) / total * 100:.0f}% dari total)")

    if open_now:
        lines.append("")
        lines.append(f"⚠️ {len(open_now)} sesi masih terbuka (belum ada event close):")
        for app, since in open_now[:5]:
            t = datetime.fromtimestamp(since, WITA).strftime("%H:%M")
            lines.append(f"• {app} sejak {t}")

    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
