---
name: eu-funding-map
description: "Map EU money around a topic, country, region or organisation: open and forthcoming funding calls (Funding & Tenders), CORDIS research projects, cohesion projects, EU budget beneficiaries (Financial Transparency System), TED procurement and EU sanctions regimes, every amount typed and never summed across kinds. Use for \"which EU calls on hydrogen are open\", \"what Horizon projects does this organisation join\", \"who won EU tenders for cybersecurity in Belgium\". Not for: lobbying (use eu-influence-map), upcoming deadlines (use eu-horizon-scan), a single lookup (use eu-gov-data). Never a sanctions clearance or compliance check."
metadata:
  stromy-client-summary: "Map EU money around a topic, place or organisation: funding calls, research and regional projects, EU budget commitments and tenders, each amount kept in its own kind and currency."
---
<!--
  GENERATED FILE — DO NOT EDIT.
  Owner:       scripts/sync-mcp-skill-stubs.py (via sync-on-mcp-skill-change.yml)
  Source:      MCPs/eu-gov-data/skills/eu-funding-map/SKILL.md
  This workflow pushes DIRECT to this repo's main — a local edit here will be
  overwritten or rejected non-fast-forward. Edit the source, push, then:
    gh workflow run sync-on-mcp-skill-change.yml -R stromy-org/stromy-org
  Hand-authored skill? Set `_local: true` in frontmatter instead.
-->

# EU Funding Map (MCP-hosted skill)

This skill's full instructions are hosted on the `eu-gov-data` MCP server. Do not hardcode workflow logic locally — always fetch the live version from the MCP.

## Loading instructions

1. Read the main skill instructions:
   → call the `fs_read` tool on the `eu-gov-data` MCP with `path="skills/eu-funding-map/SKILL.md"`.

   **Read it to the end.** `fs_read` returns one page at a time. If the result's `next_offset_chars` is not null — or the returned text ends in a `<<< PARTIAL READ … >>>` block — the body is incomplete: call `fs_read` again with `offset_chars` set to that value and concatenate, repeating until it comes back null. Do **not** start work on a partial skill body. Hard rules and anti-patterns often sit in the final third, and a partial read fails silently — it looks like a complete skill.

2. Discover reference files (and any other skill assets), then read on demand:
   → call `fs_list` with `path="skills/eu-funding-map"` (and `path="skills/eu-funding-map/references"`),
   → call `fs_read` with `path="skills/eu-funding-map/references/<file>"`.

Follow the instructions returned by the MCP exactly.

## This MCP is the only correct path

Produce this skill's output **only** by following the live SKILL.md fetched above and calling the `eu-gov-data` MCP's own tools. Do **not** substitute a local or identically-named base skill from elsewhere, and do **not** invent your own output path. A locally-produced or unbranded artifact is **wrong output, not a fallback** — it bypasses the server-side brand and quality gates.

## If the `eu-gov-data` MCP is slow to respond

This server scales to zero to save cost, so the first call after an idle period wakes the container — typically ~10–30s, and up to ~1–2 min for a heavier image (media / browser tier). If `fs_read` or a tool errors with unavailable/timeout:

1. Tell the user the server is starting, then retry the same call — the call itself wakes the container.
2. Retry with a short backoff up to ~3 times.
3. Only if it is still unreachable after retries, STOP and report. Never downgrade to a local or base skill just to "get something out".
