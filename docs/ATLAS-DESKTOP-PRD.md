# PRD — Atlas Desktop (the hands-free Jarvis)

**Product:** a local desktop application that is the face and voice of the Atlas Hub. You
say **"Hey Atlas"** and it wakes, listens, answers out loud, and acts — pulling your day
together in the morning, answering questions through the day, opening the apps and
gathering the info it needs — without you touching the keyboard or hopping between apps.

**Status:** specification. Builds on the existing hub (this repo). Maps to Roadmap Phases
4–5. **Owner of the build:** Hephaestus (the forge), directed by Atlas.

---

## 1. The one-liner & the problem

> *A Jarvis that's just there — hands-free, ambient, and already knows my whole life.*

Today your intelligence is text-first and scattered across apps. You talk a lot and think
out loud (this is a stream-of-consciousness workflow), so **holding a key to talk is a
non-starter** — your fingers get tired and it breaks your flow. You want to speak
naturally, get spoken answers, and never app-hop to assemble context. You believe you
already have some wake-word wiring; we build on that rather than replacing it.

## 2. Goals / non-goals

**Goals**
1. **Truly hands-free.** Wake word "Hey Atlas"; no key required for a full conversation.
2. **A comfortable optional PTT that is a *toggle*, not a hold.** Tap to start talking, tap
   (or auto-stop on silence) to end. Never hold.
3. **Spoken in and out**, low latency, with **barge-in** (you can interrupt Atlas mid-
   sentence and it stops and listens).
4. **A living "Jarvis" HUD** — an ambient visual with motion that reflects state (idle /
   listening / thinking / speaking / acting).
5. **Morning launch ritual** — "Hey Atlas, what's on today?" pulls calendar, mail, to-dos,
   pipeline, and opens the apps you'll need, then briefs you out loud.
6. **Ad-hoc anything** — "how do I fix this", "build me a Commander deck around X", "how's
   NVDA — hold or fold?" answered in-place using the hub's agents and connectors.
7. **One surface.** It orchestrates the other apps so you don't have to open them.

**Non-goals (v1)**
- Not a phone app yet (phone is a fast-follow that hits the same hub — see §10).
- Not autonomous with money or outbound sends — the hub's consent line still holds (§8).
- Not a general OS assistant that controls *everything* — it drives a curated allow-list of
  apps/actions, expanded over time via the forge.

## 3. Users & signature moments

You (Matt), at your desk, hands on other things. The moments that define success:

- **Morning:** *"Hey Atlas, what's on the schedule and my to-dos?"* → HUD blooms, Atlas
  opens the workspace (Slack, mail, Notion, the day's docs), and speaks a tight briefing:
  what needs you, today's calendar, hot pipeline, anything overdue. Notes captured to the
  brain as it goes.
- **Mid-task:** *"Hey Atlas, how do I fix this error?"* → answers from context, no app
  switch.
- **Hobby:** *"Hey Atlas, cool commander — what can I build around Prosper, Tome-Bound?"* →
  Bard drafts a deck direction.
- **Markets:** *"Hey Atlas, what's the stock look like today — stay in my positions?"* →
  reads quotes/portfolio, gives a read (analysis, not auto-trading).
- **Capture:** *"Hey Atlas, remember that Jordan wants the revised quote Friday."* → Hermes
  updates the people-graph + a follow-up.

## 4. Experience & interaction model

### 4.1 Conversation states (drive the visuals + the mic)
```
IDLE ──"Hey Atlas"──► LISTENING ──speech ends (VAD)──► THINKING ──► SPEAKING
  ▲                        │  ▲                                        │
  │                        │  └───────── barge-in ("Hey Atlas"/voice)──┘
  └───────── conversation timeout / "that's all" ◄── ACTING (tools/apps) ◄┘
```
- **Wake:** local wake-word spotter listens continuously on-device (privacy: only the
  wake word is matched locally; audio isn't streamed until wake).
- **Continuous mode:** after a wake, stay in an open conversational window (configurable,
  e.g. 45s of silence, or until "that's all / thanks Atlas") so follow-ups need no
  re-wake. This is the key to hands-free stream-of-consciousness.
- **Barge-in:** while SPEAKING, keep the mic hot; detected speech instantly ducks/stops
  TTS and returns to LISTENING.
- **Endpointing:** VAD (voice-activity detection) decides when you've finished a thought —
  no button. Tune silence threshold to your pace (you pause a lot mid-thought → generous
  threshold so it doesn't cut you off).

### 4.2 Input modes (you pick per moment, in Settings)
| Mode | How | When |
|------|-----|------|
| **Hands-free (default)** | Wake word + continuous window + barge-in | Normal use |
| **Toggle PTT** | Tap a hotkey (or the HUD orb) to start; tap or auto-VAD to stop | Loud rooms, privacy, dictation bursts — **tap, never hold** |
| **Type** | Click the HUD, type | Quiet office / precise input |
| **Sleep** | Wake word disabled | Focus / calls |

### 4.3 The HUD (Jarvis visuals)
- A frameless, always-available **orb/arc-reactor**: a small floating widget that can
  expand to a panel. Lives in a corner or on a second monitor; global hotkey to summon.
- **Motion maps to state:** slow breathing (idle) → rippling/reactive to your voice
  amplitude (listening) → swirling particles (thinking) → waveform pulse synced to TTS
  (speaking) → tool/app icons orbiting with a progress arc (acting).
- **Live transcript + action log:** what it heard, what it's doing ("opening Slack…",
  "reading 3 unread from customers…"), and cited results — so you can glance, not read.
- **Design language:** dark, translucent, neon-accent, subtle depth/glow. 60fps. Reduced-
  motion and "quiet" (no audio, minimal glow) options.

## 5. System architecture

```
┌──────────────────────── Atlas Desktop (local app) ─────────────────────────┐
│                                                                             │
│  Wake-word spotter (on-device)  ──►  Audio capture + VAD/endpointing        │
│         │                                     │                             │
│         ▼                                     ▼                             │
│  Conversation state machine  ◄──────►  STT (speech→text)                    │
│         │                                     ▲                             │
│         ▼                                     │ barge-in ducking            │
│  HUD renderer (orb/panel, 60fps)      TTS (text→speech, streaming)          │
│         │                                     ▲                             │
│         ▼                                     │                             │
│  ── Hub client ────────────────────────────────────────────────────────    │
│         │  (local IPC / localhost)                                          │
└─────────┼───────────────────────────────────────────────────────────────────┘
          ▼
┌──────────────────────── Atlas Hub service (Agent SDK) ─────────────────────┐
│  Atlas orchestrator → Hermes · Vantage · Hephaestus · Chronos · Bard        │
│  brain/ (Obsidian vault + open-brain)   ·   MCP connectors                   │
│  OS/App control adapter (open apps, focus windows, run allow-listed actions)│
└─────────────────────────────────────────────────────────────────────────────┘
```

The desktop app is a **thin, rich client**: it owns audio + visuals; all reasoning,
memory, and tools live in the hub service you already have. That separation is why phone
and desktop can later be the *same* Atlas.

## 6. Voice pipeline (the make-or-break)

Latency target: **< 800ms** wake→listening, **< 1.2s** end-of-speech→first spoken word.
This is what makes it feel alive vs. clunky.

| Stage | Recommended (v1) | Private/on-device alt | Notes |
|-------|------------------|-----------------------|-------|
| **Wake word** | **openWakeWord** or **Picovoice Porcupine** ("Hey Atlas" custom keyword) | same (both run local) | Reuse whatever you already have wired if it exposes an event |
| **VAD/endpoint** | **Silero VAD** | same | Tunable silence window for your pacing |
| **STT** | **Deepgram** or **OpenAI Realtime** (streaming) | **whisper.cpp** / faster-whisper local | Streaming partials feed the HUD transcript |
| **Reasoning** | **Atlas Hub** (Claude via Agent SDK) | — | The brain you already built |
| **TTS** | **ElevenLabs** (low-latency streaming) or **OpenAI TTS** | **Piper** local | Pick an "Atlas" voice; stream so speech starts fast |
| **Barge-in** | mic stays hot during TTS; VAD triggers duck+cancel | same | Critical for stream-of-consciousness |

The cleanest single-vendor path for v1 speed is **OpenAI Realtime API** (STT+turn-taking+
TTS in one low-latency socket) with the hub in the loop for reasoning/tools; swap to
local Whisper+Piper for a fully private mode later. Design the pipeline as **pluggable
adapters** so wake/STT/TTS are swappable without touching the app.

## 7. OS & application control (the "opens Slack and gathers info" part)

An **App Control adapter** in the hub exposes safe, allow-listed capabilities:
- **Launch / focus** an app (Slack, mail, browser, Notion, Obsidian, your Vantage app).
- **Open a URL / doc / Notion page.**
- **Gather** via the real connectors first (Gmail, Calendar, Notion MCP) — prefer API over
  screen-scraping; launch the GUI app only when you actually want to *see/use* it.
- **Capture** notes/screenshots into `brain/00-inbox/`.
- **(Later, opt-in) UI automation** for apps without an API, via an accessibility/automation
  layer — gated behind explicit per-action approval.

Implementation notes: macOS uses AppleScript/URL-schemes/Shortcuts + Accessibility API;
Windows uses UIAutomation/`start`/PowerShell. Every action is on an allow-list you can
see and edit; new actions are added through the forge with your ok. The morning ritual is
just a saved **routine**: `open workspace apps → pull calendar+mail+pipeline → speak
briefing → log to brain`.

## 8. Consent & privacy (unchanged spine, new surface)

- The hub's consent line still rules: **ask once** for spend / outbound send / irreversible
  / new reach; **just do** everything reversible and internal. Voice doesn't loosen this.
- **Verbal confirmations** for gated actions: "That'll email Jordan — want me to send it?"
  → "yes." A whitelist of low-risk actions ("open Slack", "read my mail") never prompts.
- **Wake-word audio never leaves the device**; streaming to STT begins only after wake and
  can be forced fully-local (Whisper+Piper) for sensitive contexts.
- **Visible mic state** always (HUD color + a hard "Sleep" hotkey). A kill-switch mutes
  everything instantly.
- Trades, purchases, and sending remain hard-gated regardless of mode.

## 9. Tech stack recommendation

- **Shell:** **Tauri** (Rust core + web UI) — lightweight, low RAM for an always-on widget,
  great for a frameless translucent HUD; or **Electron** if you want the richer ecosystem
  and don't mind the footprint. *Recommendation: Tauri for an always-on ambient app.*
- **HUD/visuals:** web canvas — **WebGL/Three.js** or shader-based particles for the orb;
  React for the panel/transcript. Target 60fps, GPU-accelerated.
- **Audio:** native mic capture in the Rust/Node layer; WebAudio for visualizer amplitude.
- **Hub service:** **Claude Agent SDK** hosting the existing `.claude/agents`, skills, and
  `brain/`; local IPC or `localhost` socket to the app.
- **Voice adapters:** pluggable (openWakeWord/Porcupine · Silero · Deepgram/OpenAI/Whisper ·
  ElevenLabs/OpenAI/Piper).
- **Packaging:** auto-launch on login, lives in the tray/menubar.

## 10. Phasing (each stage usable on its own)

- **v0 — Push-to-talk toggle + text HUD.** Hub-as-service on the Agent SDK; a floating orb;
  **tap-to-talk toggle** (proves the loop without wake-word/barge-in). Speaks answers via
  streaming TTS. *You can already talk to Atlas hands-mostly-free.*
- **v1 — Hands-free.** Wake word "Hey Atlas", VAD endpointing, continuous conversation
  window, barge-in. The full no-keys experience.
- **v2 — Rituals + app control.** Morning/evening routines, the App Control adapter (open
  apps, gather, capture), saved voice routines.
- **v3 — The living HUD.** Full reactive particle visuals, action log, second-monitor mode,
  themes, reduced-motion/quiet modes.
- **v4 — Phone parity.** A mobile front-end (PWA or native) pointing at the *same* hub, so
  Atlas on your phone shares the same memory and agents. Proactive spoken briefings from
  Chronos.

## 11. Success metrics

- Time-to-first-word after you stop speaking (target < 1.2s).
- % of a morning handled without touching keyboard/mouse (target: the whole briefing).
- False-wake rate (target: < ~1/hour) and missed-wake rate (target: near zero at desk).
- Barge-in stop latency (target: < 200ms).
- "It's just there" — you reach for Atlas by voice before opening the app it fronts.

## 12. Open questions (won't block v0)

- Which wake-word engine is already wired on your machine, and does it emit an event we can
  subscribe to? (We'll adopt it if so.)
- Fully-local vs. cloud voice as the *default* (privacy vs. lowest latency) — the pluggable
  design lets us defer; pick per your comfort.
- One "Atlas" TTS voice — pick/clone a voice you like (ElevenLabs) or go neutral local.

---
*See `docs/VOICE.md` for the higher-level rationale and `docs/ROADMAP.md` for how this
slots into the overall build. This app is the body; the hub in this repo is already the
brain.*
