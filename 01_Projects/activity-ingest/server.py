#!/usr/bin/env python3
"""
Activity Ingest — penerima webhook screen-time dari iOS Shortcuts.

Desain:
- Nol dependensi eksternal (stdlib saja). Ringan untuk VPS 2 vCPU / 2GB.
- SQLite di mode WAL. Tulis append-only, aman untuk satu proses.
- Auth: bearer token statis via header X-Ingest-Token (dibandingkan constant-time).
  Cukup aman karena selalu di belakang TLS.

Endpoint:
  POST /ingest        {"device":"iphone","app":"Instagram","event":"open"|"close"}
  GET  /health        liveness probe
  GET  /summary       ringkasan hari ini (butuh token)

Konvensi pairing:
  event "open"  -> menutup sesi terbuka sebelumnya (kalau ada, dianggap orphan), buka sesi baru
  event "close" -> menutup sesi terbuka terakhir untuk (device, app)
"""

import hmac
import json
import os
import re
import sqlite3
import time
from datetime import datetime, timedelta, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

BASE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.getenv("ACTIVITY_DB", os.path.join(BASE, "activity.db"))
TOKEN = os.getenv("INGEST_TOKEN", "")
PORT = int(os.getenv("ACTIVITY_PORT", "8099"))
WITA = timezone(timedelta(hours=8))

# Sesi lebih panjang dari ini dianggap orphan (mis. app dibiarkan terbuka semalaman)
MAX_SESSION_S = 6 * 3600

APP_RE = re.compile(r"^[\w .\-\+#@/()]{1,80}$")


def db():
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.execute("PRAGMA busy_timeout=5000")
    return conn


def init_db():
    with db() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS sessions (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                device      TEXT NOT NULL,
                app         TEXT NOT NULL,
                started_at  INTEGER NOT NULL,
                ended_at    INTEGER,
                duration_s  INTEGER,
                source      TEXT NOT NULL DEFAULT 'shortcut'
            );
            CREATE INDEX IF NOT EXISTS idx_sessions_app_start
                ON sessions(app, started_at);
            CREATE INDEX IF NOT EXISTS idx_sessions_open
                ON sessions(device, app, ended_at);

            CREATE TABLE IF NOT EXISTS raw_events (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                device      TEXT NOT NULL,
                app         TEXT NOT NULL,
                kind        TEXT NOT NULL,
                ts          INTEGER NOT NULL,
                received_at INTEGER NOT NULL
            );
            """
        )


def now_ts():
    return int(time.time())


def handle_event(device, app, kind, ts):
    """Kembalikan dict hasil yang bisa langsung di-JSON-kan."""
    with db() as conn:
        conn.execute(
            "INSERT INTO raw_events(device, app, kind, ts, received_at) VALUES (?,?,?,?,?)",
            (device, app, kind, ts, now_ts()),
        )

        if kind == "open":
            # tutup sesi terbuka sebelumnya (orphan) bila ada
            prev = conn.execute(
                "SELECT id, started_at FROM sessions "
                "WHERE device=? AND app=? AND ended_at IS NULL "
                "ORDER BY started_at DESC LIMIT 1",
                (device, app),
            ).fetchone()
            if prev:
                dur = min(max(0, ts - prev[1]), MAX_SESSION_S)
                conn.execute(
                    "UPDATE sessions SET ended_at=?, duration_s=? WHERE id=?",
                    (prev[1] + dur, dur, prev[0]),
                )
            conn.execute(
                "INSERT INTO sessions(device, app, started_at, source) VALUES (?,?,?,'shortcut')",
                (device, app, ts),
            )
            return {"ok": True, "action": "opened", "app": app}

        # kind == "close"
        row = conn.execute(
            "SELECT id, started_at FROM sessions "
            "WHERE device=? AND app=? AND ended_at IS NULL "
            "ORDER BY started_at DESC LIMIT 1",
            (device, app),
        ).fetchone()
        if not row:
            return {"ok": True, "action": "noop", "reason": "no open session", "app": app}
        dur = min(max(0, ts - row[1]), MAX_SESSION_S)
        conn.execute(
            "UPDATE sessions SET ended_at=?, duration_s=? WHERE id=?",
            (row[1] + dur, dur, row[0]),
        )
        return {"ok": True, "action": "closed", "app": app, "duration_s": dur}


def summary(date_str=None):
    if date_str:
        day = datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=WITA)
    else:
        day = datetime.now(WITA).replace(hour=0, minute=0, second=0, microsecond=0)
    start = int(day.timestamp())
    end = start + 86400

    with db() as conn:
        rows = conn.execute(
            "SELECT app, SUM(COALESCE(duration_s,0)) AS total, COUNT(*) AS n "
            "FROM sessions WHERE started_at >= ? AND started_at < ? "
            "GROUP BY app ORDER BY total DESC",
            (start, end),
        ).fetchall()
        open_now = conn.execute(
            "SELECT app, started_at FROM sessions WHERE ended_at IS NULL "
            "ORDER BY started_at DESC"
        ).fetchall()

    total = sum(r[1] for r in rows)
    return {
        "date": day.strftime("%Y-%m-%d"),
        "total_s": total,
        "apps": [
            {"app": r[0], "seconds": r[1], "minutes": round(r[1] / 60), "sessions": r[2]}
            for r in rows
        ],
        "open_sessions": [{"app": r[0], "since": r[1]} for r in open_now],
    }


class Handler(BaseHTTPRequestHandler):
    server_version = "activity-ingest/1.0"

    def log_message(self, fmt, *args):
        # log ringkas, hindari noisy default
        print(f"[{datetime.now(WITA).strftime('%H:%M:%S')}] {self.address_string()} {fmt % args}",
              flush=True)

    # ---------- util ----------
    def _send(self, code, payload):
        body = json.dumps(payload, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _authorized(self):
        if not TOKEN:
            return False
        supplied = self.headers.get("X-Ingest-Token", "")
        return hmac.compare_digest(supplied, TOKEN)

    def _read_json(self):
        """Terima JSON dari body; fallback ke query string.

        Shortcuts kadang mengirim body sebagai text/plain, atau pengguna lupa
        mengisi Request Body sehingga semua data jatuh ke URL. Dua-duanya
        ditangani supaya tidak perlu debug berjam-jam.
        """
        data = {}

        n = 0
        try:
            n = int(self.headers.get("Content-Length", "0") or "0")
        except ValueError:
            n = 0

        if 0 < n <= 64_000:
            raw = self.rfile.read(n)
            try:
                parsed = json.loads(raw)
                if isinstance(parsed, dict):
                    data.update(parsed)
            except Exception:
                # coba form-encoded (app=Instagram&event=open)
                try:
                    txt = raw.decode("utf-8", "ignore")
                    for k, v in parse_qs(txt).items():
                        data[k] = v[0]
                except Exception:
                    pass

        # query string selalu boleh menimpa (memudahkan tes via browser)
        qs = parse_qs(urlparse(self.path).query)
        for k, v in qs.items():
            data.setdefault(k, v[0])

        return data if data else None

    # ---------- routes ----------
    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/health":
            return self._send(200, {"ok": True, "service": "activity-ingest"})
        if path == "/summary":
            if not self._authorized():
                return self._send(401, {"ok": False, "error": "unauthorized"})
            qs = parse_qs(urlparse(self.path).query)
            date_str = qs.get("date", [None])[0]
            try:
                return self._send(200, {"ok": True, **summary(date_str)})
            except ValueError:
                return self._send(400, {"ok": False, "error": "bad date, use YYYY-MM-DD"})
        return self._send(404, {"ok": False, "error": "not found"})

    def do_POST(self):
        path = urlparse(self.path).path
        if path != "/ingest":
            return self._send(404, {"ok": False, "error": "not found"})
        if not self._authorized():
            return self._send(401, {"ok": False, "error": "unauthorized"})

        data = self._read_json()
        if not isinstance(data, dict):
            return self._send(400, {"ok": False, "error": "invalid json"})

        device = str(data.get("device", "iphone"))[:32]
        app = str(data.get("app", "")).strip()
        kind = str(data.get("event", "")).lower()

        if not APP_RE.match(app):
            return self._send(400, {"ok": False, "error": "invalid app name"})
        if kind not in ("open", "close"):
            return self._send(400, {"ok": False, "error": "event must be open|close"})

        try:
            ts = int(data.get("ts") or now_ts())
        except (TypeError, ValueError):
            ts = now_ts()

        try:
            result = handle_event(device, app, kind, ts)
        except Exception as e:  # noqa: BLE001
            return self._send(500, {"ok": False, "error": str(e)})
        return self._send(200, result)


def main():
    init_db()
    srv = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    print(f"activity-ingest listening on 127.0.0.1:{PORT} db={DB_PATH}", flush=True)
    srv.serve_forever()


if __name__ == "__main__":
    main()
