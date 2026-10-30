---
name: kit-prospect-contact
description: "Build a verified contact card for one named person at a company: work email with a deliverability verdict, LinkedIn profile and current role, a confidence grade and the sources behind it, using the Toolkit `find_contact` tool. Use when asked for someone's email or contact details, 'how do I reach <name> at <company>', 'find the email of the CEO of <company>' once the person is named, or to check whether an address will deliver. One person per request. Not for building a list of many contacts, private or personal addresses, phone numbers, or writing and sending the outreach email itself."
metadata:
  stromy-client-summary: "Find a decision-maker's verified work email and LinkedIn profile from a name and company, with a confidence grade and the sources behind it."
---
<!--
  GENERATED FILE — DO NOT EDIT.
  Owner:       scripts/sync-mcp-skill-stubs.py (via sync-on-mcp-skill-change.yml)
  Source:      MCPs/toolkit-mcp/skills/kit-prospect-contact/SKILL.md
  This workflow pushes DIRECT to this repo's main — a local edit here will be
  overwritten or rejected non-fast-forward. Edit the source, push, then:
    gh workflow run sync-on-mcp-skill-change.yml -R stromy-org/stromy-org
  Hand-authored skill? Set `_local: true` in frontmatter instead.
-->

# Contact card — one person, verified (MCP-hosted skill)

This skill's full instructions are hosted on the `toolkit` MCP server. Do not hardcode workflow logic locally — always fetch the live version from the MCP.

## Before you start — this skill needs the `toolkit` connector

This skill's instructions live on the `toolkit` MCP, a sign-in connector the plugin bundles. Each user connects it once. Before step 1 below, check whether this conversation actually has the `toolkit` MCP's tools (`fs_read` / `fs_list`) available to call.

**If those tools are not present at all, STOP — and do not retry.** A missing tool is not a slow server: it means the connector is not connected yet, or not switched on for this conversation. Retrying cannot fix it. Tell the user plainly what to do, naming the connector:

> This needs the **Toolkit** connector, which isn't connected for this chat. Open Customize, then Plugins, choose this plugin and open its **Connectors** tab. Click **Connect** next to **Toolkit** and sign in with your work account (if it says **Not added**, add it there first, or ask your workspace owner to). Then make sure it is switched on for this conversation and ask me again.

Then stop and wait. Never fall back to a local or identically-named base skill, and never answer from your own knowledge instead — an unsourced answer is **wrong output, not a fallback**.

## Loading instructions

1. Read the main skill instructions:
   → call the `fs_read` tool on the `toolkit` MCP with `path="skills/kit-prospect-contact/SKILL.md"`.

   **Read it to the end.** `fs_read` returns one page at a time. If the result's `next_offset_chars` is not null — or the returned text ends in a `<<< PARTIAL READ … >>>` block — the body is incomplete: call `fs_read` again with `offset_chars` set to that value and concatenate, repeating until it comes back null. Do **not** start work on a partial skill body. Hard rules and anti-patterns often sit in the final third, and a partial read fails silently — it looks like a complete skill.

2. Discover reference files (and any other skill assets), then read on demand:
   → call `fs_list` with `path="skills/kit-prospect-contact"` (and `path="skills/kit-prospect-contact/references"`),
   → call `fs_read` with `path="skills/kit-prospect-contact/references/<file>"`.

Follow the instructions returned by the MCP exactly.

## This MCP is the only correct path

Produce this skill's output **only** by following the live SKILL.md fetched above and calling the `toolkit` MCP's own tools. Do **not** substitute a local or identically-named base skill from elsewhere, and do **not** invent your own output path. A locally-produced or unbranded artifact is **wrong output, not a fallback** — it bypasses the server-side brand and quality gates.

## If the `toolkit` MCP is slow to respond

This server scales to zero to save cost, so the first call after an idle period wakes the container — typically ~10–30s, and up to ~1–2 min for a heavier image (media / browser tier). If `fs_read` or a tool errors with unavailable/timeout:

1. Tell the user the server is starting, then retry the same call — the call itself wakes the container.
2. Retry with a short backoff up to ~3 times.
3. Only if it is still unreachable after retries, STOP and report. Never downgrade to a local or base skill just to "get something out".
