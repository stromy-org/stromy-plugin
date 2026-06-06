---
name: nl-issue-framing
description: "Analyze how a named subject — a company, product, organisation, technology, sector, or specific policy issue — is framed in official Dutch government and parliamentary records through nl-gov-data. Use this whenever the user wants official-source reputation or issue framing for a specific entity or issue: how an organisation is portrayed, how a product or technology is treated in policy, how a contested issue is characterised, what reputational risks surface in official records. Sector domain packs (e.g. pharma/medicine — Novo Nordisk, GLP-1s, Wegovy, Ozempic, semaglutide, reimbursement, shortages, package management) supply ready keyword banks, default frames, and legal anchors. Produces narrative analysis, mention/context tables, issue maps, PA/PR implications, and DOCX-ready source appendices."
---

# Dutch Official Issue & Entity Framing (MCP-hosted skill)

This skill's full instructions are hosted on the `nl-gov-data` MCP server. Do not hardcode workflow logic locally — always fetch the live version from the MCP.

## Loading instructions

1. Read the main skill instructions:
   → call the `fs_read` tool on the `nl-gov-data` MCP with `path="skills/nl-issue-framing/SKILL.md"`.

2. Discover reference files (and any other skill assets), then read on demand:
   → call `fs_list` with `path="skills/nl-issue-framing"` (and `path="skills/nl-issue-framing/references"`),
   → call `fs_read` with `path="skills/nl-issue-framing/references/<file>"`.

Follow the instructions returned by the MCP exactly.

## This MCP is the only correct path

Produce this skill's output **only** by following the live SKILL.md fetched above and calling the `nl-gov-data` MCP's own tools. Do **not** substitute a local or identically-named base skill from elsewhere, and do **not** invent your own output path. A locally-produced or unbranded artifact is **wrong output, not a fallback** — it bypasses the server-side brand and quality gates.

## If the `nl-gov-data` MCP is slow to respond

This server scales to zero to save cost, so the first call may take ~10–30s to cold-start. If `fs_read` or a tool errors with unavailable/timeout:

1. Tell the user the server is starting, then retry the same `fs_read` call — the call itself wakes the container.
2. Retry with a short backoff up to ~3 times.
3. Only if it is still unreachable after retries, STOP and report. Never downgrade to a local or base skill just to "get something out".
