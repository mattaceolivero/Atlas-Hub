# Decision Record

The trade-offs behind the architecture, so future-you (and the agents) know *why*, not
just *what*. You asked me to make the best calls and show reasoning — here it is.

### D1 — One orchestrator, specialists behind it
**Chose:** Atlas as the sole interface; specialists as subagents you never address
directly.
**Over:** letting you talk to each agent, or a flat multi-agent chat.
**Why:** you explicitly want one place and one voice. A single orchestrator also owns
context and synthesis, which is where multi-agent systems usually fall apart (fragmented
state, contradictory outputs).

### D2 — Markdown vault as primary memory (not Notion, not a vector DB)
**Chose:** an Obsidian-compatible `brain/` folder of markdown as the source of truth;
`open-brain` as a search index; Notion as an *output* surface only.
**Over:** Notion-as-brain, or a hosted vector database.
**Why:** you already live in Obsidian and hate lock-in and scatter. Markdown is portable,
greppable, git-versioned, and diff-able, and it merges cleanly with your existing vault.
Notion isn't greppable or local; a vector DB adds infra and hides your truth behind an
index. We still use both where they're genuinely better (Notion for shareable dashboards,
open-brain for recall) — just not as the system of record.

### D3 — Six specialists, single-purpose, skills-biased
**Chose:** Atlas + Hermes, Athena, Hestia, Hephaestus, Chronos, Bard; new capabilities
default to a *skill*, not a new agent.
**Over:** one mega-agent, or a large swarm.
**Why:** you said small team, each doing one job, and you hate sprawl. One agent can't
hold this many distinct tool-sets and cares cleanly; a swarm reintroduces the scatter.
Six is enough to cover work + life without becoming a bureaucracy. Skills-over-agents
keeps the org chart flat as the hub grows.

### D4 — Narrow, one-time consent line
**Chose:** ask once for spend / outbound / irreversible / new-reach; auto-run everything
else and finish on "yes" without re-asking.
**Over:** ask-for-everything (annoying, not Jarvis) or full autonomy (unsafe with your
money and reputation).
**Why:** this is exactly the behavior you described. It maximizes autonomy while protecting
the two things you can't undo — spent money and sent messages.

### D5 — Gmail drafts, never auto-send
**Chose:** Hestia drafts replies; sending is always your click. Gmail send isn't even
granted.
**Why:** your outbound reputation with customers, friends, and family is irreplaceable. A
wrong auto-sent email is a real cost; a draft costs nothing.

### D6 — Build in stages; voice last
**Chose:** text-first collective now (Stage A), voice front-end later (Stage B).
**Over:** chasing the talking-Jarvis UI first.
**Why:** voice on a shallow brain is a gimmick. The value is a system that *knows your
life*; that's the hard part and it's built first. Voice becomes a thin, easy final layer
because the artifacts port directly to the Agent SDK.

### D7 — Greek pantheon naming
**Chose:** Atlas (you named him) leads a Greek family — Hermes (you named him), Athena,
Hestia, Hephaestus, Chronos, Bard.
**Why:** cohesive, memorable, and each name signals the job (Hephaestus the forge = the
builder; Hestia the hearth = relationships; Chronos = time). Small thing, but it makes the
team feel like one thing, which is the whole point.

### D8 — Consolidation is a documented local routine, not a cloud action
**Chose:** the vault-intake happens when you run Atlas locally and point it at your drive.
**Why:** I built this from a cloud container that cannot see your laptop or external drive.
Rather than pretend, the design makes the brain *ready to receive* your scatter and gives
you an exact command to run locally. Honest and functional beats magic that doesn't exist.
