# Rencana Arsitektur & Spesifikasi: Kantor AI (Virtual Office AI)

- **Tanggal Dibuat:** 18 Oktober 2026
- **Status:** Siap di-handover ke Claude Code / Diimplementasikan
- **Tech Stack:** Python 3.11+, FastAPI, LangGraph, OpenRouter, OmniRouter, SQLite/PostgreSQL

---

## 1. Ringkasan & Konsep Sistem
Sistem ini memodelkan "Kantor AI" mandiri berbasis arsitektur *Multi-Agent Hierarchical Orchestration*:
- **Manager Agent (Orchestrator):** Didukung OpenRouter (Claude 3.5 Sonnet / GPT-4o) untuk tugas perencanaan, pemecahan tugas (*task breakdown*), penugasan ke spesialis, dan *quality control* akhir.
- **Worker Agents (Spesialis):** Didukung OmniRouter (DeepSeek V3/V4 / model biaya efisien) untuk eksekusi tugas teknis massal:
  1. *Market & Competitor Analyst* (riset pasar, analisis data)
  2. *Copywriter & Content Strategist* (copywriting, strategi konten sosial media)
  3. *Operational SOP & Policy Drafter* (pembuatan SOP operasional bisnis)
- **Executive Interface (Discord Integration):** Thena bertindak sebagai penghubung langsung antara pemilik bisnis (Dewa Biara) di Discord dan backend FastAPI melalui direct HTTP calls (`POST /api/tasks`, `GET /api/tasks/{task_id}`).

---

## 2. Struktur Direktori Proyek (`virtual-office-ai`)

```text
virtual-office-ai/
├── app/
│   ├── __init__.py
│   ├── main.py                     # FastAPI REST API & SSE streaming
│   ├── config.py                   # Pydantic Settings & environment config
│   ├── core/
│   │   ├── llm_factory.py          # Client factory (OpenRouter & OmniRouter)
│   │   └── state.py                # LangGraph State schemas
│   ├── agents/
│   │   ├── manager.py              # Planning & review specialist (OpenRouter)
│   │   ├── analyst.py              # Data/market analysis specialist (OmniRouter)
│   │   ├── copywriter.py           # Marketing copy specialist (OmniRouter)
│   │   └── ops.py                  # SOP/operational specialist (OmniRouter)
│   ├── graph/
│   │   ├── workflow.py             # LangGraph state machine & router
│   │   └── memory.py               # SQLite/PostgreSQL checkpointing
│   └── web/                        # Web Dashboard UI
│       ├── static/
│       │   ├── css/style.css
│       │   └── js/app.js           # Real-time event consumer
│       └── templates/index.html    # Visual office rooms & interactive logs
├── tests/
│   ├── test_agents.py
│   └── test_api.py
├── .env.example
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## 3. Konfigurasi Lingkungan (`.env`)

```env
# Manager LLM (OpenRouter)
OPENROUTER_API_KEY=your_openrouter_key
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_MODEL=anthropic/claude-3.5-sonnet

# Worker LLM (OmniRouter - Deployed on Same VPS)
OMNIROUTER_API_KEY=your_omnirouter_key
OMNIROUTER_BASE_URL=http://127.0.0.1:3000/v1  # Sesuaikan dengan port OmniRouter lokal
OMNIROUTER_MODEL=deepseek-v4-pro

# Server Config
PORT=8000
DEBUG=True
```

---

## 4. Evaluasi Kapasitas Resource VPS (Audit 18 Oktober 2026)

| Parameter | Spesifikasi Saat Ini | Kebutuhan Kantor AI | Status |
| :--- | :--- | :--- | :--- |
| **CPU** | 2 vCPU (Intel Broadwell) | ~0.1 - 0.3 vCPU (I/O bound) | **Sangat Kuat / Aman** |
| **RAM** | 2.0 GB (Available: ~750 MB) | ~150 MB - 300 MB (FastAPI + LangGraph) | **Cukup & Stabil** |
| **Disk** | 19 GB (Sisa: 2.3 GB / 88%) | ~300 MB - 500 MB (Virtualenv & dependensi) | **Waspada Kuota Disk** |
| **Load Avg** | 0.19, 0.13, 0.09 | Rendah | **Optimal** |

### Kesimpulan Kelayakan:
1. **Komputasi & Memori:** Sangat memadai. Komputasi AI dan neural network dilakukan secara remote di server OpenRouter dan OmniRouter, sehingga beban lokal server hanya menjalankan HTTP server asynchronous (FastAPI/Uvicorn) dan state router LangGraph.
2. **Catatan Ruang Disk:** Karena sisa ruang disk adalah **2.3 GB**, disarankan:
   - Menjalankan aplikasi langsung menggunakan `venv` Python lokal daripada membuat image Docker baru yang besar.
   - Rutin membersihkan package cache (`pip cache purge`).
