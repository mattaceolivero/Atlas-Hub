---
name: lead-scout
description: Find, score, and deliver best-fit leads to Notion against Matt's ICP. Use when Vantage runs a prospecting job or Matt asks to find leads / research prospects for outreach.
---

# Lead Scout

Turn Matt's criteria into a short list of decision-ready leads in Notion. Quality over
volume — Matt wants the few worth contacting, not a dump.

## Steps

1. **Load criteria.** Read `brain/20-work-pipeline/icp.md`. If thin, infer from recent
   won/lost deals and flag the gap for Atlas — don't guess silently.

2. **Source** (ZoomInfo + web):
   - `search_companies` on ICP firmographics → shortlist accounts
   - `find_similar_companies` to expand from known good customers
   - `search_intent` for timing signals where available
   - `search_contacts` / `get_recommended_contacts` for the right person at each account
   - Web research for context ZoomInfo lacks (recent news, "why now")

3. **Score** each lead 1–5 on: fit (matches ICP), timing (intent/trigger), reachability.
   Drop anything below 3. Note the reason so the bar is auditable.

4. **Enrich survivors:** title, company one-liner, a specific "why now", and a suggested
   outreach angle (hand the angle off — do not send anything).

5. **Deliver to Notion.** Upsert into the **Leads** database (create it if absent) with a
   fixed schema: `Name, Title, Company, Fit (1–5), Why Now, Angle, Source, Status, Date`.
   Dedupe against existing rows.

6. **Log** the run in `brain/20-work-pipeline/lead-runs.md` (date, criteria, counts) and
   `capture_thought` the headline.

## Compliance
B2B research only. No bulk export, no spam, legitimate outreach basis. Respect ZoomInfo's
acceptable-use policy.

## Output
Count found / passed the bar, top 3 with the "why now", and the Notion link.
