# Atlas Hub — Architecture

The full design for a personal AI collective: one agent you talk to (**Atlas**) that
delegates to a small team of specialists, remembers everything in one place, connects to
your whole life, and improves itself over time. This is the north-star Jarvis, built in
stages you can actually run.

---

## 1. Design principles (the reasoning behind everything)

Every decision below traces back to five principles drawn straight from what you asked
for:

1. **One front door.** You talk to Atlas and only Atlas. The team exists *behind* him.
   Nothing about the multi-agent machinery should leak into your day. → *single
   orchestrator, specialists as subagents.*

2. **Consolidate relentlessly.** Your stated #1 pain is scatter — half-built projects
   across your laptop, an external "AI Vault" drive, and Obsidian. So the hub has exactly
   one memory (`brain/`) and one repo, and every feature pulls toward it. → *one
   Obsidian-compatible vault as the brain; a documented intake to absorb the scatter.*

3. **Own your data, no lock-in.** Your memory is plain markdown you can open in Obsidian,
   grep, and back up. The system is portable. → *markdown vault + open standards, not a
   proprietary DB you can't leave.*

4. **Self-improving with a hard consent line.** Missing a skill isn't a dead end — the
   hub finds or builds it. But it asks once for anything that spends money, sends
   outward, or adds new reach; on "yes" it runs to completion without re-asking. →
   *`skill-forge` + the permission protocol.*

5. **Small team, single-purpose agents.** You explicitly want few agents, each doing one
   job. More agents = more sprawl = the thing you hate. → *Atlas + 6 specialists, and a
   bias toward adding a skill rather than an agent.*

## 2. The collective

```
                              ┌──────────────┐
              You  ⇄  speak   │    ATLAS     │   orchestrator · holds context · one voice
                              └──────┬───────┘
              delegates ┌───────────┼───────────┬───────────┬───────────┐
                        ▼           ▼           ▼           ▼           ▼
                   ┌────────┐  ┌────────┐  ┌────────┐  ┌──────────┐ ┌────────┐
                   │ Hermes │  │ Athena │  │ Hestia │  │Hephaestus│ │  Bard  │
                   │signals │  │ growth │  │relations│ │ the forge│ │ worlds │
                   └────┬───┘  └────┬───┘  └────┬───┘  └────┬─────┘ └────┬───┘
                        │           │           │           │           │
                        └───────────┴─────┬─────┴───────────┴───────────┘
                                          ▼
                          ┌──────────────────────────────┐
                          │   BRAIN  (Obsidian md vault)  │  + open-brain index
                          │  people · pipeline · projects │
                          │  games · system · inbox       │
                          └──────────────────────────────┘
                                          ▲
              ┌───────────────────────────┴────────────────────────────┐
              │  CONNECTIONS (MCP): Gmail · Calendar · Drive · Notion ·  │
              │  ZoomInfo · Granola · GitHub · open-brain · …            │
              └─────────────────────────────────────────────────────────┘
       Chronos (cadence) fires the whole thing on a schedule ── briefings, reviews, nudges
```

| Agent | One job | Why it's separate |
|-------|---------|-------------------|
| **Atlas** | Orchestrate, hold context, be the single voice | You wanted one interface; someone must own the plan and synthesis |
| **Hermes** | AI/tech news + hub improvement proposals | Keeping current is a distinct, continuous scanning job |
| **Athena** | Lead-gen + research → Notion | Prospecting has its own tools (ZoomInfo) and output surface (Notion) |
| **Hestia** | Inbox, customer needs, relationships | Email + people is a full-time steward role; different tools, different care |
| **Hephaestus** | Find/build missing skills | Self-improvement must be an explicit, guard-railed capability, not a side effect |
| **Chronos** | Scheduling + briefings | Proactivity ("throughout the day") needs an owner of time |
| **Bard** | D&D, MTG, Discord guild | Your hobby worlds need continuity; keeps personal life from bleeding into work agents |

Design note on naming: you named Atlas and Hermes and described three more roles (a
marketing/outreach researcher, an email/customer-needs watcher, and a lead-finder that
outputs to Notion). I split those cleanly — **Athena** (leads), **Hestia** (email +
customer needs + relationships) — and added **Hephaestus** (the self-improvement engine
you described but didn't name), **Chronos** (the "throughout the day" proactivity), and
**Bard** (your D&D/MTG/Discord life). Greek pantheon so the team reads as one family
under the Titan.

## 3. Memory — the brain

**Decision: a single Obsidian-compatible markdown vault (`brain/`) is the source of
truth, with `open-brain` MCP as a fast cross-session search index.**

- Markdown + `[[wikilinks]]` + `#tags` → opens natively in your existing Obsidian, greps
  from the terminal, versions in git, backs up trivially. No lock-in, no database to run.
- Structure: `00-inbox / 10-people / 20-work-pipeline / 30-projects / 40-games /
  50-system`. (See `brain/README.md`.)
- Two-tier memory: the vault is the **durable, full record**; `open-brain` holds the
  **searchable gist** so any agent in any session can recall "what do we know about X"
  without loading the whole vault.
- Consolidation: this vault *is* the destination for your scattered notes and the AI
  Vault drive. Intake is a documented Atlas+Hephaestus routine (see §7 and
  `brain/README.md`) because I can't reach your drive from the cloud — you run it locally
  and point it at your existing vault.

Why not Notion or a vector DB as the primary brain? Notion is great for **shareable,
structured output** (leads, dashboards) and is used exactly there — Athena writes to it.
But it's a poor *primary* memory: not greppable, not local, not Obsidian. A vector DB
adds infra you'd have to run and locks your memory behind an index. Markdown-first keeps
principle #3 (own your data) intact; `open-brain` gives the vector-like recall without
owning the truth.

## 4. Connections — the surface to your life

MCP connectors are the hub's senses and hands. Each is owned by the agent whose job it
serves (full map in `docs/CONNECTIONS.md`):

- **Gmail** → Hestia. Reads threads, drafts replies (never sends unprompted).
- **Google Calendar** → Chronos. Your day, scheduling, briefing input.
- **Google Drive + Granola** → shared. Documents and meeting transcripts for context.
- **Notion** → Athena's output; also where dashboards/views you share with others live.
- **ZoomInfo** → Athena. Company/contact/intent data for leads.
- **GitHub** → Hephaestus. The hub's own code and evolution.
- **open-brain** → shared memory index.
- **Spotify / Robinhood / Stocks / Higgsfield** → on-demand, only when you ask.

Gaps become work, not walls: if a capability needs a connector that isn't wired,
Hephaestus proposes adding it (that's a consent-gated action), rather than the hub
pretending it can.

## 5. Self-improvement & consent — the Jarvis clause

The loop (defined operationally in `CLAUDE.md` §5, implemented by `skill-forge` +
Hephaestus):

```
task needs a capability
        │
        ▼
skill exists locally? ──yes──► use it
        │no
        ▼
Hermes finds a prebuilt skill/plugin/MCP? ──yes──► "add X? (y/n)" ─y─► install → finish
        │no
        ▼
"no prebuilt exists; build one? (y/n)" ─y─► skill-forge builds → tests → wires → finish
        │n
        ▼
note the decline in brain (don't re-ask)
```

The consent line is deliberately narrow so the hub feels autonomous but safe. **Ask once**
for: spending money, anything outward-facing (email/DM/post), irreversible changes, new
capabilities/connectors. **Just do** everything reversible and internal. On "yes," run to
completion — no re-asking mid-job. This is exactly the behavior you described: "if I say
yes, it does it without question and into completion."

## 6. Proactivity & cadence

Chronos + scheduled triggers turn the hub from a thing-you-poke into a second set of
eyes:
- **Morning briefing**, **evening wrap**, **weekly review**, **signals digest**, **lead
  run** — defined in `brain/50-system/cadence.md`, fired via `create_trigger` /
  `CronCreate` into a persistent hub session.
- Briefings are single, skimmable messages that lead with what needs you.

## 7. Runtime — how it actually runs, in two stages

**Stage A — today, zero-infra (this repo).** The hub *is* a Claude Code project:
- Atlas = the main session (driven by `CLAUDE.md`).
- Specialists = subagents in `.claude/agents/` invoked via the Agent tool.
- Skills = `.claude/skills/` (self-improvement lives here).
- Brain = the `brain/` markdown vault + `open-brain`.
- Connections = the MCP servers already attached to this environment.
- Proactivity = scheduled triggers.
- Consolidation intake = run locally, point Atlas at your Obsidian vault, it merges into
  `brain/` and logs provenance in `50-system/intake-log.md`.

This works now. Clone the repo, open it in Claude Code (desktop or web), and talk to
Atlas.

**Stage B — the Jarvis endgame (voice, always-on).** A persistent hub service built on
the **Claude Agent SDK** with a **voice front-end** (see `docs/VOICE.md`). The migration
is clean because the artifacts port directly: every `.claude/agents/*.md` becomes an SDK
subagent definition, every skill carries over, the brain and MCP wiring are unchanged.
Stage A is not a throwaway prototype — it's Stage B minus the always-on process and the
microphone. See `docs/ROADMAP.md` for the phased path.

## 8. What this explicitly is NOT (scope discipline)

- Not a swarm. Six specialists, single-purpose, biased toward skills over new agents.
- Not a new data silo. It absorbs your scatter; it doesn't add to it.
- Not autonomous with your money or your outbound reputation. Those stay consent-gated.
- Not dependent on any one vendor for its memory. Markdown-first, portable.

See `docs/DECISIONS.md` for the record of trade-offs and `docs/ROADMAP.md` for how to
stand it up.
