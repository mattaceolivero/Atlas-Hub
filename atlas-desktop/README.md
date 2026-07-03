# Atlas Desktop — the hands-free voice Jarvis

Say **"Hey Atlas"** and talk. Atlas wakes, listens, thinks, acts, and answers out
loud — with the whole collective (Hermes, Vantage, Hephaestus, Chronos, Bard) and your
`brain/` behind it. Hands-free by default: a wake word, continuous conversation (no keys
to hold), and barge-in so you can interrupt mid-sentence. A reactive orb HUD shows what
it's doing.

This app is the **body**; the `Atlas-Hub` repo one level up is the **brain**. The app
just gives that brain ears, a voice, and a face.

```
🎙️  "Hey Atlas…"                        ┌─────────────────────────────┐
      │  wake word (on-device)           │  Atlas Hub  (Agent SDK)     │
      ▼                                   │  Atlas → the 5 specialists  │
 mic → VAD endpoint → Chirp STT ─ text ─►│  brain/ + MCP connectors    │
                                          └──────────────┬──────────────┘
 🔊  Chirp 3:HD  ◄─ sentences ◄─ streamed reply ◄────────┘
      │  (barge-in: talk over it to interrupt)
      ▼
 Reactive HUD orb  ·  http://localhost:4173
```

## What it uses
- **Brain:** Claude Agent SDK running the `Atlas-Hub` project (loads `CLAUDE.md`, the
  specialists in `.claude/agents/`, skills, and permissions). Model: Opus 4.8.
  **No Anthropic API key** — it uses your Claude Code login as the backend.
- **Wake word:** Picovoice Porcupine — "Hey Atlas", on-device.
- **Endpointing:** Silero VAD (tuned generously so it never cuts you off mid-thought).
- **Speech-to-text + text-to-speech:** **Gemini** (default; works with just a Gemini API
  key). Switch `stt.provider`/`tts.provider` to `google-chirp` in `config.yaml` if you set
  up a Google Cloud project for true Cloud Chirp.
- **HUD:** a self-contained local web orb, live over websocket.

## Setup (macOS)

```bash
cd atlas-desktop
bash scripts/setup_mac.sh          # PortAudio + venv + deps + .env
```

Then:
1. **Fill in `.env`** (copied from `.env.example`) — only two secrets:
   - `GEMINI_API_KEY` — from https://aistudio.google.com/apikey (powers voice in + out).
   - `PICOVOICE_ACCESS_KEY` — free from https://console.picovoice.ai (wake word).
   - *No Anthropic key* — sign in to Claude Code once instead (next step).
2. **Sign in to Claude Code** (the brain's backend):
   `npm install -g @anthropic-ai/claude-code` then run `claude` once and log in.
3. **Make the wake word** — see `scripts/get_wakeword.md` (or just say **"Jarvis"** to
   start; that's the built-in fallback until you create "Hey Atlas").

## Run

```bash
source .venv/bin/activate
python -m atlas_voice.main
```

The orb opens at `http://localhost:4173`. Then just talk:

- *"Hey Atlas, what's on my schedule today, and anything in my inbox that needs me?"*
- *"Hey Atlas, open Slack and my mail."*  (macOS app control via Atlas.)
- *"Hey Atlas, cool commander — what can I build around Prosper, Tome-Bound?"*
- *"Hey Atlas, how's NVDA today — should I hold my position?"*
- Interrupt any answer just by talking. Say *"that's all"* to send Atlas back to sleep.

## Tuning
Everything lives in **`config.yaml`** — wake sensitivity, how long it keeps listening,
how much silence means "you're done" (bump `silence_end_ms` if it cuts you off), the Chirp
voice, the app allow-list, and the HUD theme.

## Grant macOS permissions
On first run, macOS will ask for **Microphone** access (allow it). For app control
("open Slack"), you may also need to allow the terminal under **System Settings →
Privacy & Security → Automation / Accessibility**.

## Status & honesty
This is **v1 built for your Mac** and is the first run on real audio hardware — I authored
it in a cloud container without a mic, so expect to tune `config.yaml` (VAD timings, wake
sensitivity) in the first session. Every module is small and single-purpose so it's easy
to adjust. Architecture and rationale: `../docs/ATLAS-DESKTOP-PRD.md`.

### Layout
```
atlas-desktop/
  atlas_voice/
    main.py        # the hands-free state machine (ears + speaking task)
    wakeword.py    # "Hey Atlas" (Porcupine)
    vad.py         # Silero endpointing
    stt_google.py  # Chirp 2 speech-to-text
    tts_google.py  # Chirp 3:HD text-to-speech
    brain.py       # Claude Agent SDK → the Atlas Hub
    audio.py       # mic capture + speaker (barge-in)
    state.py       # states + event bus
    hud/           # the reactive orb (served on localhost)
  config.yaml      # all the knobs
  .env.example     # keys
  scripts/         # setup_mac.sh, get_wakeword.md
```
