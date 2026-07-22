---
name: nl-parliamentary-positioning
description: "Map Dutch parliamentary positioning and official political posture from nl-gov-data. Use this whenever the user asks which MPs, factions, committees, ministries, votes, questions, motions, debates, petitions, forums, or official bodies are active around a Dutch policy topic. Two modes: Mode A produces source-backed PA/PR stakeholder maps, faction/MP activity summaries, committee and ministry maps, forum activity tables, engagement signals, and DOCX-ready client analysis. Mode B produces a per-legislator meeting-prep disposition brief — trigger on 'MP profile', 'disposition brief', 'meeting prep for <MP>', 'who am I meeting', or 'legislator brief'. Do not treat this as public sentiment; it is official parliamentary and institutional positioning. Do NOT trigger for: entity or issue reputation/framing analysis (→ nl-issue-framing); a said-vs-done contradiction focused on one actor (→ nl-tensions); a single-dossier deep-dive brief with a passage forecast (→ nl-dossier-tracker); a comprehensive, bounded pledge/commitment ledger (→ nl-accountability)."
---
<!--
  GENERATED FILE — DO NOT EDIT.
  Owner:       scripts/sync-mcp-skill-stubs.py (via sync-on-mcp-skill-change.yml)
  Source:      MCPs/nl-gov-data/skills/nl-parliamentary-positioning/SKILL.md
  This workflow pushes DIRECT to this repo's main — a local edit here will be
  overwritten or rejected non-fast-forward. Edit the source, push, then:
    gh workflow run sync-on-mcp-skill-change.yml -R stromy-org/stromy-org
  Hand-authored skill? Set `_local: true` in frontmatter instead.
-->

# Dutch Parliamentary Positioning (MCP-hosted skill)

This skill's full instructions are hosted on the `nl-gov-data` MCP server. Do not hardcode workflow logic locally — always fetch the live version from the MCP.

## Loading instructions

1. Read the main skill instructions:
   → call the `fs_read` tool on the `nl-gov-data` MCP with `path="skills/nl-parliamentary-positioning/SKILL.md"`.

2. Discover reference files (and any other skill assets), then read on demand:
   → call `fs_list` with `path="skills/nl-parliamentary-positioning"` (and `path="skills/nl-parliamentary-positioning/references"`),
   → call `fs_read` with `path="skills/nl-parliamentary-positioning/references/<file>"`.

Follow the instructions returned by the MCP exactly.

## This MCP is the only correct path

Produce this skill's output **only** by following the live SKILL.md fetched above and calling the `nl-gov-data` MCP's own tools. Do **not** substitute a local or identically-named base skill from elsewhere, and do **not** invent your own output path. A locally-produced or unbranded artifact is **wrong output, not a fallback** — it bypasses the server-side brand and quality gates.

## If the `nl-gov-data` MCP is slow to respond

This server scales to zero to save cost, so the first call after an idle period wakes the container — typically ~10–30s, and up to ~1–2 min for a heavier image (media / browser tier). If `fs_read` or a tool errors with unavailable/timeout:

1. Tell the user the server is starting, then retry the same call — the call itself wakes the container.
2. Retry with a short backoff up to ~3 times.
3. Only if it is still unreachable after retries, STOP and report. Never downgrade to a local or base skill just to "get something out".
