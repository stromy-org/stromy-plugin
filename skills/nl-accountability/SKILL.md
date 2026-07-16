---
name: nl-accountability
description: "Track what Dutch ministers and cabinets formally committed to, and classify each commitment's delivery status (Kept / Compromised / Stalled / Deferred / Broken / Not-yet-testable) with cited evidence. Cross-checks against Rijksfinanciën budget appropriations and CBS outcome statistics. Use this skill when the user asks what a minister promised vs delivered, wants a coalition-agreement scorecard, needs to track toezeggingen delivery for a client brief, wants a said-vs-done ledger, or wants to ground a promised-vs-delivered narrative in citable official-record evidence. Do NOT use for adversarial contradiction-hunting or angle-finding on a topic (→ `nl-tensions`) or for open-ended topic/dossier monitoring (→ `nl-gov-data`, referred to here as `nl-monitor`-shaped requests). This skill needs a **frozen, bounded commitment corpus** — it is a comprehensive tracker, not a spot-check."
---
<!--
  GENERATED FILE — DO NOT EDIT.
  Owner:       scripts/sync-mcp-skill-stubs.py (via sync-on-mcp-skill-change.yml)
  Source:      MCPs/nl-gov-data/skills/nl-accountability/SKILL.md
  This workflow pushes DIRECT to this repo's main — a local edit here will be
  overwritten or rejected non-fast-forward. Edit the source, push, then:
    gh workflow run sync-on-mcp-skill-change.yml -R stromy-org/stromy-org
  Hand-authored skill? Set `_local: true` in frontmatter instead.
-->

# Accountability (MCP-hosted skill)

This skill's full instructions are hosted on the `nl-gov-data` MCP server. Do not hardcode workflow logic locally — always fetch the live version from the MCP.

## Loading instructions

1. Read the main skill instructions:
   → call the `fs_read` tool on the `nl-gov-data` MCP with `path="skills/nl-accountability/SKILL.md"`.

2. Discover reference files (and any other skill assets), then read on demand:
   → call `fs_list` with `path="skills/nl-accountability"` (and `path="skills/nl-accountability/references"`),
   → call `fs_read` with `path="skills/nl-accountability/references/<file>"`.

Follow the instructions returned by the MCP exactly.

## This MCP is the only correct path

Produce this skill's output **only** by following the live SKILL.md fetched above and calling the `nl-gov-data` MCP's own tools. Do **not** substitute a local or identically-named base skill from elsewhere, and do **not** invent your own output path. A locally-produced or unbranded artifact is **wrong output, not a fallback** — it bypasses the server-side brand and quality gates.

## If the `nl-gov-data` MCP is slow to respond

This server scales to zero to save cost, so the first call may take ~10–30s to cold-start. If `fs_read` or a tool errors with unavailable/timeout:

1. Tell the user the server is starting, then retry the same `fs_read` call — the call itself wakes the container.
2. Retry with a short backoff up to ~3 times.
3. Only if it is still unreachable after retries, STOP and report. Never downgrade to a local or base skill just to "get something out".
