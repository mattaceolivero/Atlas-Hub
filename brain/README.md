# The Brain 🧠

This folder is the durable memory of the Atlas collective — and the **consolidation
target** for your scattered notes, half-built projects, and the "AI Vault" Obsidian vault
on your external drive.

It is a plain **Obsidian-compatible markdown vault**. Open this folder directly in
Obsidian and it just works: `[[wikilinks]]`, `#tags`, backlinks, graph view. No
proprietary format, nothing locked in. Every agent reads from and writes to here.

## Structure

| Folder | Holds |
|--------|-------|
| `00-inbox/` | Unsorted captures. Dump here fast; triage into the right folder later. |
| `10-people/` | One note per person — customers, friends, family, guild members, players. |
| `20-work-pipeline/` | Deals, leads, customers, outreach, the ICP. |
| `30-projects/` | Active projects and the half-built work being consolidated. |
| `40-games/` | D&D (DMing + playing), Magic: The Gathering, the Discord guild. |
| `50-system/` | How the hub runs: decisions, cadence, the agent activity log, signals. |

## Consolidation plan (your scattered work → here)

Because I run in the cloud, I can't reach your local machine or external drive directly.
When you open this repo on your machine with Claude Code, run the intake:

> "Atlas, ingest my Obsidian vault at `<path>` into the brain."

Atlas + Hephaestus will: read your existing notes, map them to the folders above, merge
duplicates, preserve your `[[links]]`, and log what came from where in
`50-system/intake-log.md`. Point-and-consolidate, not rebuild-from-scratch.

## Rules
- Notes are markdown. Link people/projects/games with `[[wikilinks]]`.
- Every durable fact lands here; the searchable gist also goes to `open-brain`.
- One place. Always.
