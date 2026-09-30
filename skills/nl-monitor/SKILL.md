---
name: nl-monitor
description: "Recurring monitoring and alert product for Dutch parliamentary and legislative activity. Watches a defined topic/dossier/actor matrix over weekly windows and produces a weekly briefing: breaking alerts, dossier-status, forward agenda. Use whenever the user wants a topic or dossier set monitored on a cadence, asks for a weekly brief, asks 'what changed', wants a threshold alert on a watched dossier, or wants a re-runnable digest. Not for: single-dossier passage forecasting (→ nl-dossier-tracker); 6-36 month foresight (→ nl-horizon-scan); toezeggingen delivery tracking (→ nl-accountability); contradiction hunting (→ nl-tensions); a one-off pull-up-and-summarise on a named dossier with no recurring cadence (→ nl-gov-data)."
metadata:
  stromy-client-summary: "Set up a recurring watch on Dutch parliamentary activity and get a regular briefing."
---
<!--
  GENERATED FILE — DO NOT EDIT.
  Owner:       scripts/sync-mcp-skill-stubs.py (via sync-on-mcp-skill-change.yml)
  Source:      MCPs/nl-gov-data/skills/nl-monitor/SKILL.md
  This workflow pushes DIRECT to this repo's main — a local edit here will be
  overwritten or rejected non-fast-forward. Edit the source, push, then:
    gh workflow run sync-on-mcp-skill-change.yml -R stromy-org/stromy-org
  Hand-authored skill? Set `_local: true` in frontmatter instead.
-->

# NL Monitor (MCP-hosted skill)

This skill's full instructions are hosted on the `nl-gov-data` MCP server. Do not hardcode workflow logic locally — always fetch the live version from the MCP.

## Loading instructions

1. Read the main skill instructions:
   → call the `fs_read` tool on the `nl-gov-data` MCP with `path="skills/nl-monitor/SKILL.md"`.

   **Read it to the end.** `fs_read` returns one page at a time. If the result's `next_offset_chars` is not null — or the returned text ends in a `<<< PARTIAL READ … >>>` block — the body is incomplete: call `fs_read` again with `offset_chars` set to that value and concatenate, repeating until it comes back null. Do **not** start work on a partial skill body. Hard rules and anti-patterns often sit in the final third, and a partial read fails silently — it looks like a complete skill.

2. Discover reference files (and any other skill assets), then read on demand:
   → call `fs_list` with `path="skills/nl-monitor"` (and `path="skills/nl-monitor/references"`),
   → call `fs_read` with `path="skills/nl-monitor/references/<file>"`.

Follow the instructions returned by the MCP exactly.

## This MCP is the only correct path

Produce this skill's output **only** by following the live SKILL.md fetched above and calling the `nl-gov-data` MCP's own tools. Do **not** substitute a local or identically-named base skill from elsewhere, and do **not** invent your own output path. A locally-produced or unbranded artifact is **wrong output, not a fallback** — it bypasses the server-side brand and quality gates.
