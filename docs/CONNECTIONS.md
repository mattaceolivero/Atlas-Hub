# Connections — MCP → Life Domains

How the hub touches your world. Each connector is owned by the agent whose job it serves,
so there's one responsible party per surface. "Status" reflects what's wired in *this*
environment today.

| Connector | Owner | What it's for | Send/spend risk | Status |
|-----------|-------|---------------|-----------------|--------|
| **Gmail** | Hermes | Read threads, extract customer needs, draft replies | Sending = manual only | Live |
| **Google Calendar** | Chronos | Your day, scheduling, briefing input | Create/edit = ask | Live |
| **Google Drive** | shared | Documents, files for context | Read-only by default | Live |
| **Granola** | Hermes / Bard | Meeting transcripts | Read-only | Live |
| **Notion** | Vantage | Leads DB, research output, shareable dashboards | Create/update = ask | Live |
| **ZoomInfo** | Vantage | Company/contact/intent data for leads | Enrich costs credits = ask | Live |
| **GitHub** | Hephaestus | The hub's own code + skill building | Push = ask | Live |
| **open-brain** | all | Cross-session memory index | Internal | Live |
| **Google Calendar suggest_time** | Chronos | Find meeting slots | Read-only | Live |
| **Spotify** | on-demand | Now playing, playlists | Low | Live, unused until asked |
| **Robinhood / Stocks** | on-demand | Markets, portfolio | Trades = hard-gated | Live, unused until asked |
| **Higgsfield** | on-demand | Image/video/audio generation | Costs credits = ask | Live, unused until asked |
| **Supabase** | future | If the hub ever needs a real DB (Stage B) | — | Available, not adopted |

## Consent tiers (mirrors `.claude/settings.json`)

- **Auto (just do):** all reads, brain writes, Gmail drafts, calendar reads, Notion reads,
  ZoomInfo searches, git status/commit.
- **Ask once:** anything that writes to Notion, edits your calendar, enriches via ZoomInfo
  (credits), or pushes to GitHub.
- **Never auto:** sending email/DMs, placing trades, spending money, adding a new
  connector. Gmail *send* is intentionally not granted at all — Hermes drafts, you send.

## Domains → connectors (your life, mapped)

- **Work pipeline** → ZoomInfo + Notion + Gmail + Granola (Vantage, Hermes)
- **Relationships (friends/family)** → Gmail + `brain/10-people` (Hermes)
- **Customer needs** → Gmail + Granola + Notion (Hermes → Vantage)
- **D&D / MTG / Discord guild** → `brain/40-games` + web research (Bard)
- **Your day / time** → Calendar (Chronos)
- **The hub improving itself** → GitHub + web (Hephaestus, Hermes)

## Adding a connector
A missing connector is a Hephaestus proposal, not a blocker. He surfaces it as an
"add X? (y/n)"; on yes, it's wired and documented here. New reach is always consent-gated.
