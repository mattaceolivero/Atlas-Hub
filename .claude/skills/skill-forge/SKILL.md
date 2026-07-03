---
name: skill-forge
description: Build a new reusable skill for the Atlas Hub when a capability is missing and no prebuilt skill exists. Use after Matt approves building. Produces a tested, wired-in SKILL.md under .claude/skills/. This is the mechanism behind the hub's self-improvement.
---

# Skill Forge

The hub's ability to grow its own capabilities. Invoked by Hephaestus (or Atlas directly)
after the permission protocol in `CLAUDE.md` has produced a "yes, build it."

## Precondition: reuse check
Do NOT build if it already exists. First confirm (via Hermes / search) that no prebuilt
skill, plugin, or MCP server covers this. Building is the last resort, not the first.

## Steps

1. **Write the spec** (3–5 lines): the capability's name, the trigger (when it should
   fire), inputs, outputs, and which tools/connectors it needs.

2. **Scaffold** the skill:
   - `mkdir .claude/skills/<kebab-name>/`
   - Create `SKILL.md` with YAML frontmatter (`name`, `description` — the description is
     what makes it discoverable, so write it as "Use when…") followed by clear,
     imperative instructions. Keep it single-purpose.
   - Add reference files or scripts in the same folder only if genuinely needed.

3. **Test end-to-end.** Run the skill against one real example. Capture the result. If it
   didn't actually work, fix it before declaring done. An untested skill is not a skill.

4. **Wire it in.** Add it to the relevant agent's `tools`/description or the CLAUDE.md
   skills list so Atlas will reach for it. If it warrants a connector Matt hasn't
   approved, stop and route that approval up — don't self-grant reach.

5. **Log & commit.** Append to `brain/50-system/agent-log.md`, `capture_thought` a
   one-liner, and commit to the working branch with a descriptive message.

## Quality bar
- One skill = one job. If you're tempted to add a second job, that's a second skill.
- The description field is the interface — invest in it; it's how Atlas discovers the
  skill later.
- Prefer editing an existing skill over creating a near-duplicate.

## Template

```markdown
---
name: <kebab-name>
description: <One or two sentences. Start with "Use when…" so it's discoverable.>
---

# <Human Name>

<What it does, in one line.>

## Steps
1. …
2. …

## Output
<What the caller gets back.>
```
