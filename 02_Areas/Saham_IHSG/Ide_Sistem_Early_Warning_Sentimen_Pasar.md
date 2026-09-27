# 📡 Ide Sistem: Early Warning Sentimen Pasar & Analisis Hot News

Konsep sistem deteksi risiko dini (*market sentiment shock*) dan kalkulasi probabilitas pergerakan pasar saham (IHSG, Big Banks, Makroekonomi) berbasis agregasi berita terkurasi.

---

## 🎯 Tujuan & Konsep
Membangun bot alert ringan yang memantau headline berita global & nasional secara berkala, menghitung skor sentimen, dan mengirimkan sinyal peringatan (*early warning*) ke Discord sebelum atau saat market bereaksi.

---

## 🏗️ Arsitektur & Alur Kerja Ringan

```
[Sumber Terkurasi] ──> [Agregator Teks] ──> [Scoring Engine] ──> [Threshold Filter] ──> [Discord Alert]
  - RSS Finansial       (Python / Cron)     (FinBERT / LLM)       (Skor Sentimen)      (#market-alert)
  - BI / The Fed
  - CNBC / Bloomberg
```

1. **Ingestion (Penyerap Data):**
   - Menarik RSS feed gratis dari sumber finansial utama: CNBC Indonesia, Bisnis.com, Kontan, Reuters Financial, rilis suku bunga BI & Fed.
   - Interval: Tiap 15–30 menit saat jam bursa (09:00 - 16:00 WIB).

2. **Sentiment & Impact Scoring:**
   - Evaluasi headline & summary: Positif (+1), Netral (0), Negatif (-1).
   - Penilaian bobot dampak sektoral (misal: Suku bunga naik -> berdampak langsung ke BBCA, BBRI, BMRI; pelemahan Rupiah -> ekspor/impor).

3. **Trigger Logic (Alert):**
   - Peringatan hanya dikirim jika terjadi **Sentiment Shock** (misal: akumulasi sentimen negatif melebihi batas toleransi dalam 1 jam, atau berita mendadak berdampak sistemik).
   - Menghindari noise atau spam berita harian biasa.

---

## ⚙️ Estimasi Resource & Biaya
- **Server:** Cukup VPS 1 vCPU / 1 GB RAM (atau internal cron job container).
- **Database:** SQLite lokal (sangat hemat disk, < 50 MB).
- **Model Scoring:** FinBERT (open-source Python) atau LLM API tier mini (~$0.50 - $1 / bulan).
- **Output:** Discord Webhook ke channel alert bursa.

---

## 📌 Status
- **Status:** Backlog / Ide tersimpan untuk eksplorasi mendatang.
