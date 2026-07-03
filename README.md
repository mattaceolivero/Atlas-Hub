# Atlas Hub

A personal AI collective. You talk to **one** agent — **Atlas** — and he quietly
delegates to a small team of specialists, remembers everything in one place, connects to
your whole life, and improves himself over time. The north star is a Jarvis you can speak
to; this repo is the working foundation and the full plan to get there.

> **Talk to Atlas today:** open this repo in Claude Code (desktop, CLI, or
> [claude.ai/code](https://claude.ai/code)). `CLAUDE.md` boots him up. Start with:
> *"Atlas, what can you do?"* or *"Atlas, triage my inbox."*

## The team

| Agent | Job |
|-------|-----|
| **Atlas** | The one you talk to. Orchestrates, remembers, synthesizes. |
| **Hermes** | The messenger — inbox, customer needs, friends & family, + AI/tech news & hub-improvement ideas. |
| **Vantage** | Your proprietary lead-gen engine — finds & scores leads → Notion. |
| **Hephaestus** | The forge — finds or builds missing skills. |
| **Chronos** | Briefings, reminders, the daily rhythm. |
| **Bard** | D&D, Magic: The Gathering, the Discord guild. |

## How it's built

```
CLAUDE.md            → Atlas's operating charter (loaded every session)
.claude/agents/      → the 6 specialists (real Claude Code subagents)
.claude/skills/      → reusable capabilities incl. skill-forge (self-improvement)
.claude/settings.json→ consent tiers (auto / ask-once / never-auto)
brain/               → Obsidian-compatible memory vault = the one place
docs/                → the full architecture, roadmap, decisions, voice plan
```

## Read next

- **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)** — the full design + the reasoning.
- **[docs/ROADMAP.md](docs/ROADMAP.md)** — the phased path from here to voice-Jarvis.
- **[docs/DECISIONS.md](docs/DECISIONS.md)** — every trade-off and why.
- **[docs/CONNECTIONS.md](docs/CONNECTIONS.md)** — how it plugs into your life (MCP).
- **[docs/VOICE.md](docs/VOICE.md)** — the path to speaking with Atlas.
- **[docs/ATLAS-DESKTOP-PRD.md](docs/ATLAS-DESKTOP-PRD.md)** — full spec for the hands-free
  "Hey Atlas" desktop Jarvis (wake word, barge-in, HUD visuals, app control).
- **[brain/README.md](brain/README.md)** — the memory vault + how to consolidate your
  scattered notes into it.

## First moves (see the roadmap for the full path)

1. Open the repo in Claude Code and say hi to Atlas.
2. *"Atlas, ingest my Obsidian vault at `<path>` into the brain"* — consolidate your
   scattered work (run locally; the cloud can't see your drive).
3. Fill in `brain/20-work-pipeline/icp.md` and add your key people to `brain/10-people/`.
4. Run each specialist once for real, then turn on Chronos's daily briefing.

## Principles
One front door · consolidate relentlessly · own your data (portable markdown) ·
self-improve with a hard consent line · small single-purpose team.

---
_Note: the `bug-bounty-lab/` folder predates the hub and is unrelated; left in place
untouched. It can be removed or moved to its own repo whenever you like._
