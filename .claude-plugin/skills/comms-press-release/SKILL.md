---
name: comms-press-release
description: "Write and manage corporate press releases end to end — newsworthiness assessment, drafting, legal review, and distribution planning. Use when asked to write a press release, draft a media announcement, create a news release, prepare a PR statement, or produce journalist-ready content for an announcement — even 'announce this' or 'we need to tell the media about X'. Produces AP-style, journalist-ready releases (inverted pyramid, datelines, sourced quotes, boilerplate) across launches, funding rounds, partnerships, acquisitions, hires, milestones, research, and crisis comms. Not for proofreading an already-drafted release for typos/house style, or for measuring media coverage after publication."
metadata:
  stromy-client-summary: "Takes an announcement from newsworthiness check to a journalist-ready press release, with sign-offs and distribution planned."
---
<!--
  GENERATED FILE — DO NOT EDIT.
  Owner:       scripts/sync-mcp-skill-stubs.py (via sync-on-mcp-skill-change.yml)
  Source:      MCPs/comms-mcp/skills/comms-press-release/SKILL.md
  This workflow pushes DIRECT to this repo's main — a local edit here will be
  overwritten or rejected non-fast-forward. Edit the source, push, then:
    gh workflow run sync-on-mcp-skill-change.yml -R stromy-org/stromy-org
  Hand-authored skill? Set `_local: true` in frontmatter instead.
-->

# Corporate Press Release (MCP-hosted skill)

This skill's full instructions are hosted on the `comms` MCP server. Do not hardcode workflow logic locally — always fetch the live version from the MCP.

## Before you start — this skill needs the `comms` connector

This skill's instructions live on the `comms` MCP, which reaches you as an **authorized connector** rather than as part of the plugin. Before step 1 below, check whether this conversation actually has the `comms` MCP's tools (`fs_read` / `fs_list`) available to call.

**If those tools are not present at all, STOP — and do not retry.** A missing tool is not a slow server: it means the connector is either not added to this workspace or not switched on for this conversation. Retrying cannot fix it. Tell the user plainly what to do, naming the connector:

> This needs the **Comms** connector, which isn't switched on for this chat. Open your connector settings, check it's connected and enabled for this conversation, then ask me again.

Then stop and wait. Never fall back to a local or identically-named base skill, and never answer from your own knowledge instead — an unsourced answer is **wrong output, not a fallback**.

## Loading instructions

1. Read the main skill instructions:
   → call the `fs_read` tool on the `comms` MCP with `path="skills/comms-press-release/SKILL.md"`.

   **Read it to the end.** `fs_read` returns one page at a time. If the result's `next_offset_chars` is not null — or the returned text ends in a `<<< PARTIAL READ … >>>` block — the body is incomplete: call `fs_read` again with `offset_chars` set to that value and concatenate, repeating until it comes back null. Do **not** start work on a partial skill body. Hard rules and anti-patterns often sit in the final third, and a partial read fails silently — it looks like a complete skill.

2. Discover reference files (and any other skill assets), then read on demand:
   → call `fs_list` with `path="skills/comms-press-release"` (and `path="skills/comms-press-release/references"`),
   → call `fs_read` with `path="skills/comms-press-release/references/<file>"`.

Follow the instructions returned by the MCP exactly.

## This MCP is the only correct path

Produce this skill's output **only** by following the live SKILL.md fetched above and calling the `comms` MCP's own tools. Do **not** substitute a local or identically-named base skill from elsewhere, and do **not** invent your own output path. A locally-produced or unbranded artifact is **wrong output, not a fallback** — it bypasses the server-side brand and quality gates.

## If the `comms` MCP is slow to respond

This server scales to zero to save cost, so the first call after an idle period wakes the container — typically ~10–30s, and up to ~1–2 min for a heavier image (media / browser tier). If `fs_read` or a tool errors with unavailable/timeout:

1. Tell the user the server is starting, then retry the same call — the call itself wakes the container.
2. Retry with a short backoff up to ~3 times.
3. Only if it is still unreachable after retries, STOP and report. Never downgrade to a local or base skill just to "get something out".
