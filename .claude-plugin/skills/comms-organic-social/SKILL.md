---
name: comms-organic-social
description: "Build organic (never paid) B2B social strategy: editorial pillars, content calendars, executive/founder thought leadership, employee advocacy, community-building, AEO/GEO (content cited by AI answer engines), dark-funnel measurement. Models engagements as an audience x narrative-pillar matrix; produces a DOCX-first client strategy with evidence-tiered citations. Use when asked to build an organic social strategy, plan a campaign or narrative arc, create a content calendar, build editorial pillars or a community/employee-advocacy playbook, set up an executive LinkedIn program, optimise for AI answer engines, plan LinkedIn/Reddit content, or say you need a social presence — never for paid ads, boosting, or targeting/bidding."
metadata:
  stromy-client-summary: "Builds your organic (unpaid) social strategy, editorial calendar and measurement plan, and can turn the approved calendar into checked post objects."
---
<!--
  GENERATED FILE — DO NOT EDIT.
  Owner:       scripts/sync-mcp-skill-stubs.py (via sync-on-mcp-skill-change.yml)
  Source:      MCPs/comms-mcp/skills/comms-organic-social/SKILL.md
  This workflow pushes DIRECT to this repo's main — a local edit here will be
  overwritten or rejected non-fast-forward. Edit the source, push, then:
    gh workflow run sync-on-mcp-skill-change.yml -R stromy-org/stromy-org
  Hand-authored skill? Set `_local: true` in frontmatter instead.
-->

# Organic Social Campaign (MCP-hosted skill)

This skill's full instructions are hosted on the `comms` MCP server. Do not hardcode workflow logic locally — always fetch the live version from the MCP.

## Before you start — this skill needs the `comms` connector

This skill's instructions live on the `comms` MCP, which reaches you as an **authorized connector** rather than as part of the plugin. Before step 1 below, check whether this conversation actually has the `comms` MCP's tools (`fs_read` / `fs_list`) available to call.

**If those tools are not present at all, STOP — and do not retry.** A missing tool is not a slow server: it means the connector is either not added to this workspace or not switched on for this conversation. Retrying cannot fix it. Tell the user plainly what to do, naming the connector:

> This needs the **Comms** connector, which isn't switched on for this chat. Open your connector settings, check it's connected and enabled for this conversation, then ask me again.

Then stop and wait. Never fall back to a local or identically-named base skill, and never answer from your own knowledge instead — an unsourced answer is **wrong output, not a fallback**.

## Loading instructions

1. Read the main skill instructions:
   → call the `fs_read` tool on the `comms` MCP with `path="skills/comms-organic-social/SKILL.md"`.

   **Read it to the end.** `fs_read` returns one page at a time. If the result's `next_offset_chars` is not null — or the returned text ends in a `<<< PARTIAL READ … >>>` block — the body is incomplete: call `fs_read` again with `offset_chars` set to that value and concatenate, repeating until it comes back null. Do **not** start work on a partial skill body. Hard rules and anti-patterns often sit in the final third, and a partial read fails silently — it looks like a complete skill.

2. Discover reference files (and any other skill assets), then read on demand:
   → call `fs_list` with `path="skills/comms-organic-social"` (and `path="skills/comms-organic-social/references"`),
   → call `fs_read` with `path="skills/comms-organic-social/references/<file>"`.

Follow the instructions returned by the MCP exactly.

## This MCP is the only correct path

Produce this skill's output **only** by following the live SKILL.md fetched above and calling the `comms` MCP's own tools. Do **not** substitute a local or identically-named base skill from elsewhere, and do **not** invent your own output path. A locally-produced or unbranded artifact is **wrong output, not a fallback** — it bypasses the server-side brand and quality gates.
