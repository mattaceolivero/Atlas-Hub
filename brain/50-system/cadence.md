# Cadence

The hub's recurring rhythm, owned by Chronos and registered by Atlas as scheduled
triggers. This is the one place to edit timing. Times are Matt's local time.

| Routine | When | What |
|---------|------|------|
| Morning briefing | Weekdays 07:00 | Calendar + inbox (Needs You) + pipeline + follow-ups + games due |
| Evening wrap | Weekdays 18:00 | Done / still open / set for tomorrow |
| Weekly review | Sunday 18:00 | Pipeline health, cold relationships, stalled projects, wins |
| Signals digest | Mon/Thu 08:00 | Hermes: what's new + improvement proposals |
| Lead run | Tuesday 09:00 | Athena: fresh leads against the ICP → Notion |

## To activate
Have Atlas register these with `create_trigger` (claude-code-remote) or `CronCreate`,
one per row, firing into the hub session. Edit this table to change cadence, then ask
Atlas to re-sync the triggers.

Status: **not yet registered** — activate when the hub runs in a persistent session.
