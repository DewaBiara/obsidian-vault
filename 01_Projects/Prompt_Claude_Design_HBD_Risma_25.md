# Prompt Claude Design / Claude Code: Website Ulang Tahun ke-25 Risma

File: `Prompt_Claude_Design_HBD_Risma_25.md`  
Tujuan: Digunakan sebagai instruksi pembuatan website interaktif ulang tahun Risma ke-25 via Claude Code / Claude Design.

---

```markdown
You are acting as an expert interaction and visual designer adhering to high aesthetic standards. Build a complete, production-ready, single-file interactive birthday website (`index.html`) for Risma's 25th Birthday, created by her partner Dewa.

### Context & Persona
- Recipient: Risma (Turns 25 years old on October 26, 2026. Scorpio, born Sukra Keliwon Pujut, deep, intuitive, appreciative of effort and sincere details).
- Sender: Dewa (Cancer, born Buda Wage Menail, programmer, thoughtful, caring).
- Purpose: A deeply touching, interactive, and memorable birthday experience to open at midnight on mobile.

### Design System & Anti-Slop Guidelines
- Surface Archetype: Experience / Storytelling (NOT a SaaS dashboard, NO generic gradient hero, NO three equal-weight cards).
- Visual Mood: Warm, romantic, intimate, and luxurious.
  - Palette: Midnight navy/slate base (`#090D16`), Warm Champagne Gold accents (`#E6B980`), Soft Rose Blush (`#FDF2F8`), and creamy muted white text (`#F8FAFC`).
  - Typography: Serif display for emotional headers ("Cormorant Garamond" or "Playfair Display" via Google Fonts) paired with a clean, modern geometric sans ("Outfit" or "Plus Jakarta Sans").
  - Spacing & Touch: Strictly Mobile-First, all buttons/interactives >= 44px height, smooth scroll, tactile tap feedback with subtle spring micro-animations.

### Required Interactive Features (All inside single file index.html)
1. HERO: Interactive Birthday Cake & Candle (The Gatekeeper)
   - An elegant minimalist CSS-drawn birthday cake with a number "25" candle with a realistic flickering flame.
   - Interactive button: "Tiup Lilin & Make a Wish 🕯️".
   - When tapped: The flame gently puffs out with smoke animation -> triggers a burst of celebration confetti (use `https://cdn.jsdelivr.net/npm/canvas-confetti@1.9.3/dist/confetti.browser.min.js`) -> background romantic music starts playing smoothly (include a muted/unmute toggle floating button) -> unlocks the rest of the page with a gentle smooth scroll.

2. SECTION 2: The Interactive Love Letter (Amplop Digital)
   - A closed digital envelope with wax seal that flaps open when tapped.
   - Pulls out a letter sheet styled like textured parchment paper.
   - Indonesian heartfelt letter copy congratulating her 25th birthday, praying for her happiness, health, and career, expressing gratitude for her presence in Dewa's life.

3. SECTION 3: Memory Lane (Polaroid Wall)
   - 3-4 Polaroid-style photo frames with slight random tilts (-2deg to 3deg), drop shadows, and taped corners.
   - Placeholders with clean image tags with captions in handwriting font style (e.g. "Momen gelato pertama", "Senyum favoritku").

4. SECTION 4: The Cosmic Water Bond (Cancer ♋ × Scorpio ♏)
   - A subtle, beautiful badge/card celebrating their water connection:
     "Dua Jiwa Elemen Air yang Saling Melengkapi — Buda Wage × Sukra Kliwon (95% Cosmic Match)".
   - Warm, grounding text acknowledging their deep understanding and safe emotional space.

5. SECTION 5: Birthday Coupon Book (Kupon Spesial Ulang Tahun)
   - 3 tactile vouchers styled like perforated tickets:
     * Coupon 1: "1x Traktir Bebas Gelato di Massimo Sanur 🍨"
     * Coupon 2: "1x Tiket Nemenin Keliling Seharian Bebas Request 🛵"
     * Coupon 3: "1x Hak Selalu Benar & Bebas Ngambek 👑"
   - When Risma taps a voucher: It stamps an angled badge "CLAIMED ✅" with haptic scale animation and saves state to localStorage so it stays claimed even on refresh.

6. Audio Player Integration:
   - Include background music player with fallback royalty-free soft piano/lo-fi audio URL, plus a floating music icon in the top right corner to play/pause.

Deliver the entire working code in a single standalone `index.html` file with embedded CSS in `<style>` and JavaScript in `<script>`, fully responsive and verified.
```
