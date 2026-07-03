# Voice — the path to a Jarvis you talk to

Your endgame: physically speak to Atlas throughout the day and have it speak back — on
your computer and your phone. This is real and buildable; it's Stage B, and it sits *on
top of* everything already in this repo. Nothing here needs to change to add voice; you're
adding a microphone and a speaker to a brain that already works.

## The honest state of things
- Claude Code (Stage A, what's in this repo) is **text-first**. You already get "on your
  computer and phone" via the Claude Code **desktop app, web app (claude.ai/code), and
  mobile** — you can type to Atlas from anywhere today.
- **Spoken** in/out is not built into Claude Code. It's a thin front-end you add in Stage
  B. The intelligence — Atlas, the specialists, the brain, the connectors — is already the
  hard part and it's done.

## Architecture for voice (Stage B)

```
🎙️ mic ──► Speech-to-Text ──► ┌──────────────────────────┐ ──► Text-to-Speech ──► 🔊
                              │  Atlas Hub (Agent SDK)    │
📱 phone / 💻 desktop ───────►│  same agents, skills,     │◄──► brain + MCP connectors
   (push-to-talk / wake word) │  brain, connectors        │
                              └──────────────────────────┘
```

Components:
1. **Hub service** — the current `.claude/agents`, `.claude/skills`, `CLAUDE.md`, and
   `brain/` re-hosted as a persistent process on the **Claude Agent SDK**. The files port
   directly; this is a re-host, not a rewrite.
2. **Voice I/O layer** — STT (speech→text) in, TTS (text→speech) out. Options:
   - *Fastest to working:* OpenAI Realtime API or a Whisper (STT) + ElevenLabs/TTS pairing.
   - *On-device / private:* local Whisper + a local TTS for privacy-sensitive moments.
3. **Front-ends:**
   - **Desktop:** a small always-listening app (push-to-talk or wake word "Atlas") that
     streams audio to the hub and plays the reply.
   - **Phone:** a PWA or a Shortcut/Assistant hand-off that hits the same hub endpoint, so
     phone and desktop are the *same* Atlas with the *same* memory — not two assistants.
4. **Persistent session + cadence:** the hub stays running so Chronos's briefings can
   speak to you proactively ("Morning, Matt — here's your day"), not only answer when
   asked.

## Why Stage A first
Voice is a UI. If the brain underneath is shallow, a talking assistant is a gimmick. By
building the collective, memory, and connections first, the moment you bolt on voice you
get a Jarvis that actually *knows your life* — pipeline, people, games, guild — not a
smart speaker. The repo is deliberately ordered so voice is the last, easy mile.

## Concrete next step when you're ready for voice
1. Stand up the hub on the Agent SDK (Roadmap Phase 4).
2. Add a voice loop: STT → hub → TTS, push-to-talk on desktop first.
3. Add the wake word + phone front-end.
4. Turn on Chronos proactive speech for briefings.

Everything above reuses what's already in this repo unchanged.
