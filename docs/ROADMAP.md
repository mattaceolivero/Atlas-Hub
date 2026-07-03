# Roadmap — from this repo to Jarvis

Phased so each step is usable on its own. You are at the end of Phase 0.

## Phase 0 — Foundation ✅ (done in this repo)
- Atlas charter (`CLAUDE.md`), 6 specialists (`.claude/agents/`), 3 core skills, the brain
  vault (`brain/`), permissions (`.claude/settings.json`), and the full design (`docs/`).
- **You can already talk to Atlas** by opening this repo in Claude Code.

## Phase 1 — Consolidate (absorb the scatter)
Goal: everything in one place.
1. Open this repo locally in Claude Code (desktop/CLI).
2. Say: *"Atlas, ingest my Obsidian vault at `<path>` and my AI-Vault drive into the
   brain."* Atlas + Hephaestus map, merge, dedupe, and log provenance to
   `brain/50-system/intake-log.md`.
3. Fill `brain/20-work-pipeline/icp.md` (your ICP) and add your key people to
   `brain/10-people/`, campaigns to `brain/40-games/`.
4. Point Obsidian at the `brain/` folder so you edit the same vault the agents do.
_Exit criteria: no important note lives outside `brain/` anymore._

## Phase 2 — Wire the daily loop
Goal: the hub works for you every day, on request.
1. Confirm connectors (Gmail, Calendar, Notion, ZoomInfo) are authorized.
2. Run each specialist once for real: a Hermes inbox triage, a Vantage lead run to Notion,
   a Bard session recap. Fix any friction in the agent files.
3. Tune `.claude/settings.json` consent tiers to your comfort.
_Exit criteria: each specialist has done one real job end-to-end._

## Phase 3 — Make it proactive
Goal: second set of eyes, unprompted.
1. Register the cadence in `brain/50-system/cadence.md` as scheduled triggers
   (`create_trigger` / `CronCreate`) firing into a persistent hub session.
2. Turn on the morning briefing + evening wrap; adjust timing/verbosity over a week.
3. Let Hermes run its signals digest and start proposing hub improvements — watch the
   self-improvement loop work.
_Exit criteria: you get a useful briefing without asking._

## Phase 4 — Persistent hub (Agent SDK)
Goal: always-on, ready for voice.
1. Re-host the agents/skills/brain on the Claude Agent SDK as a running service (files
   port directly — see `docs/ARCHITECTURE.md` §7).
2. Keep the brain as the shared markdown vault; keep MCP connectors.
_Exit criteria: the hub runs without you launching a session._

## Phase 5 — Voice (the Jarvis mile)  🟡 v1 built
Goal: speak to Atlas, it speaks back, on desktop and phone.
- ✅ **Hands-free desktop app built** — `atlas-desktop/`: "Hey Atlas" wake word, Silero
  endpointing, Google **Chirp** STT + Chirp 3:HD TTS, barge-in, continuous conversation,
  reactive orb HUD, wired to the hub via the Claude Agent SDK. (macOS.)
- ⬜ First real-hardware run + tuning (`config.yaml`: VAD timings, wake sensitivity).
- ⬜ macOS app-control adapter hardening (open/gather across Slack, mail, Notion).
- ⬜ Phone front-end pointing at the same hub; Chronos proactive spoken briefings.
_Exit criteria: "Hey Atlas, what's my day?" — out loud — just works._
See `atlas-desktop/README.md` to run it and `docs/ATLAS-DESKTOP-PRD.md` for the full spec.

## Ongoing — self-improvement
From Phase 2 on, the forge is live: whenever Atlas hits a missing capability, Hermes finds
or Hephaestus builds the skill (one consent check), and the hub gets more capable every
week. That's the flywheel.
