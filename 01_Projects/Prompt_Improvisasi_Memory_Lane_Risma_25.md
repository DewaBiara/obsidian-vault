# Panduan & Prompt Improvisasi: Memory Lane untuk Ulang Tahun ke-25 Risma

Repositori: **`arpon-kapuria/memory-lane`**  
Target: Risma (25 Tahun, 26 Oktober 2026, Scorpio, Sukra Kliwon Pujut)  
Pembuat: Dewa (Cancer, Buda Wage Menail)

---

## 🚀 Cara Cepat Setup di Laptop Kamu

Jalankan perintah berikut di terminal laptop kamu:

```bash
# 1. Clone repository
git clone https://github.com/arpon-kapuria/memory-lane.git risma-birthday-25
cd risma-birthday-25

# 2. Install dependensi
npm install

# 3. Jalankan Claude Code di dalam folder tersebut dengan prompt di bawah!
claude
```

---

## 📝 Salin Prompt Berikut ke Claude Code

Salin seluruh teks di dalam blok kode di bawah ini:

```markdown
You are an expert React and UI/UX frontend engineer helping me personalize this `memory-lane` project as an unforgettable 25th birthday surprise gift for my girlfriend, Risma.

Here are the details and context you must incorporate:
- Recipient: Risma (Turning 25 on October 26, 2026. Scorpio, born Sukra Keliwon Pujut, thoughtful, loves good vibes and deep talks).
- Sender: Dewa (Her partner, Cancer, born Buda Wage Menail, programmer, caring).
- Key Inside Stories / Touchpoints:
  1. Our zodiac connection: Scorpio ♏ × Cancer ♋ (both water signs, 95% match, deep understanding, "nyambung ngobrolnya").
  2. Her recent trip/mention: Mau ke Peken Badung.
  3. Our upcoming date: Massimo Gelato in Sanur.
  4. Web maaf kucing interaktif yang pernah aku buatkan untuk dia.
  5. Saling melengkapi dan menemani bertumbuh.

### Task 1: Add a Floating Romantic Background Audio Player
In `src/App.jsx`:
- Add a floating audio player button in the top-right corner (`fixed top-4 right-4 z-50`).
- Use an elegant glassmorphism circular button with a music note icon (spinning/pulsing when playing).
- Audio source: Use a reliable royalty-free romantic piano/lo-fi stream or local `/audio/romantic-bgm.mp3`.
- Auto-play on the first user interaction (first button click on Page 1) to respect mobile browser autoplay policies.
- Allow toggle play/pause with volume set to 0.45.

### Task 2: Completely Replace `src/data/content.json` in Indonesian
Rewrite the entire `src/data/content.json` in natural, warm, heartfelt Indonesian with a playful and romantic tone:
- `meta`:
  - `name`: "Risma"
  - `title`: "Risma's 25th Chapter ❤️"
  - `subtitle`: "Sebuah perjalanan kecil tentang perempuan hebat yang hari ini genap berusia 25 tahun."
- `page1`:
  - `loadingLines`: ["Mencari frekuensi...", "Mendeteksi energi Scorpio...", "Menyiapkan kejutan...", "Sistem siap. Selamat datang, Risma."]
  - `buttonText`: "Mulai Perjalanan ✨"
- `page2`:
  - `lines`: ["Halo Risma...", "Hari ini usiamu genap 25 tahun 🎂", "Sebelum kita tiup lilin dan rayakan...", "Ada sedikit cerita yang ingin kutunjukkan padamu."]
  - `buttonText`: "Lanjut ➔"
- `page3`:
  - `line1`: "Bagaimana jika..."
  - `line2`: "KITA TIDAK PERNAH BERTEMU ?"
  - `buttonText`: "Lihat Semesta Lain 🌌"
- `page4` & `page5`:
  - `title`: "Memori Tidak Ditemukan", `subtitle`: "Di semesta lain yang membosankan tanpa kehadiranmu..."
- `page6`:
  - `title`: "Untunglah di dunia nyata...",
  - `caption`: "Ada perempuan berzodiak Scorpio paling manis yang selalu bikin hariku ramai."
  - `buttonText`: "Pulihkan Memori ❤️"
- `page7`:
  - `lines`: ["Dan di semesta inilah kita bertemu...", "Dari obrolan random yang selalu nyambung...", "Sampai akhirnya kita saling menemukan rasa nyaman."]
- `page8`:
  - `title`: "Memulihkan Memori Indah...", `progress`: 35
- `page9` (Quiz Babak 1):
  - `chapter`: "BABAK 1"
  - `chapterTitle`: "Ujian Kejujuran"
  - `question`: "Siapa yang paling sering overthinking tapi gengsi ngaku?"
  - `options`: ["Risma si ratu Scorpio 😌", "Dewa yang sok tenang 🦀", "Sama-sama tipe air jadi imbang 🌊"]
  - `correctResponse`: "Tepat sekali! Scorpio emang jagonya misterius tapi hatinya lembut kok 😆"
  - `wrongResponse`: "Haha ngeles yaa! Tetep aja kalian berdua sama-sama gemesin."
- `page10` (Quiz Babak 2):
  - `chapter`: "BABAK 2"
  - `chapterTitle`: "Pertanyaan Penting"
  - `question`: "Kalau lagi jalan-jalan, destinasi mana yang paling ditunggu?"
  - `options`: ["Makan Gelato di Massimo Sanur 🍨", "Keliling cari jajan ke Peken Badung 🛵", "Nongkrong santai sambil ngobrol deep talk ☕"]
  - `afterText`: "Semuanya valid! Yang paling penting jalan bareng kamunya ❤️"
- `page11`:
  - `title`: "Momen & Kenangan Manis"
  - `description`: "Setiap foto dan tawa yang kita lewati selalu punya tempat istimewa."
- `page12` & `page13`: Pertanyaan santai seputar kebersamaan kalian.
- `page14`:
  - `title`: "Analisis Karakter: Risma at 25"
  - Questions exploring her sweet qualities, intuition, and kindness.
  - Final Result: "Level Kecocokan: 95% (Cancer × Scorpio Water Bond — Sukra Kliwon × Buda Wage)"
- `page16`:
  - Emotional transition toward the birthday celebration.
- `page17` (The Big Celebration):
  - Confetti burst + "Selamat Ulang Tahun ke-25, Risma! 🎂🎉 Semoga di usia baru ini selalu dilimpahi kesehatan, kebahagiaan, dan rezeki yang melimpah."
- `page18` - `page20`:
  - "Memindai Rencana Masa Depan..."
- `page21` (Locked Future Cards):
  - Card 1: "Ngedate Gelato Massimo Sanur (Unlocked Soon!)"
  - Card 2: "Road Trip & Sunset di Pantai"
  - Card 3: "Merayakan Banyak Hal Baik Bersama"
- `page22`:
  - "Karena cerita terbaik kita masih terus berlanjut..."
- `page23` (The Typewriter Letter):
  - Write a deeply moving, respectful, and touching personal letter from Dewa celebrating her 25th birthday, expressing gratitude for her presence, patience, and warmth, and wishing her the brightest chapter ahead.
- `page24`:
  - Final screen with warm summary and button to replay.

### Task 3: Quality & Styling Verification
- Ensure all text wraps cleanly on mobile viewports (375px–430px).
- Verify that `npm run build` succeeds without TypeScript or Vite errors.
```
