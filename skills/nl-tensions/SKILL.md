---
name: nl-tensions
description: "Detect contradictions, said-vs-did gaps, and non-obvious tensions in Dutch public policy using the nl-gov-data MCP. Produces structured, source-cited tension reports for public-affairs consultants — dormant dossiers, expired motions, taxonomy absences, coalition flips, ministerial commitments not kept, claim-vs-structure mismatches. Use this skill whenever the user asks about tensions, contradictions, gaps, what's not adding up, said-vs-spent, said-vs-done, what the minister promised vs delivered, where a policy is stuck, why something hasn't moved, or angles for a roundtable on a Dutch policy topic. Do NOT trigger for monitoring ('what's happening on X' goes to nl-gov-data) or strategy ('what should we recommend' — out of scope). Output is evidence-and-structure only; never recommendations."
---

# Tensions (MCP-hosted skill)

This skill's full instructions are hosted on the `nl-gov-data` MCP server. Do not hardcode workflow logic locally — always fetch the live version from the MCP.

## Loading instructions

1. Read the main skill instructions:
   → call the `fs_read` tool on the `nl-gov-data` MCP with `path="skills/nl-tensions/SKILL.md"`.

2. Discover reference files (and any other skill assets), then read on demand:
   → call `fs_list` with `path="skills/nl-tensions"` (and `path="skills/nl-tensions/references"`),
   → call `fs_read` with `path="skills/nl-tensions/references/<file>"`.

Follow the instructions returned by the MCP exactly.

## This MCP is the only correct path

Produce this skill's output **only** by following the live SKILL.md fetched above and calling the `nl-gov-data` MCP's own tools. Do **not** substitute a local or identically-named base skill from elsewhere, and do **not** invent your own output path. A locally-produced or unbranded artifact is **wrong output, not a fallback** — it bypasses the server-side brand and quality gates.

## If the `nl-gov-data` MCP is slow to respond

This server scales to zero to save cost, so the first call may take ~10–30s to cold-start. If `fs_read` or a tool errors with unavailable/timeout:

1. Tell the user the server is starting, then retry the same `fs_read` call — the call itself wakes the container.
2. Retry with a short backoff up to ~3 times.
3. Only if it is still unreachable after retries, STOP and report. Never downgrade to a local or base skill just to "get something out".
