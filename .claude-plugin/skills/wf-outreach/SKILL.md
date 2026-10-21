---
name: wf-outreach
description: "Run hosted outreach follow-ups that land as drafts in the client's own Outlook mailbox: check the mailbox connection and campaign readiness, upload a prospect list, preview with a dry run, start a draft-creating run, and review deliveries that need a human decision. Use when a client asks to connect Outlook for outreach, check whether their mailbox is connected, run or preview outreach follow-ups for a campaign, or see drafts that need review, even if they never say \"workflow\". Never sends email. Not for writing a single email in the conversation, or for research workflows (wf-stakeholder-analysis)."
metadata:
  stromy-client-summary: "Plan outreach follow-ups that appear as Outlook drafts in your own mailbox; you review and send."
---
<!--
  GENERATED FILE — DO NOT EDIT.
  Owner:       scripts/sync-mcp-skill-stubs.py (via sync-on-mcp-skill-change.yml)
  Source:      MCPs/stromy-workflows-mcp/skills/wf-outreach/SKILL.md
  This workflow pushes DIRECT to this repo's main — a local edit here will be
  overwritten or rejected non-fast-forward. Edit the source, push, then:
    gh workflow run sync-on-mcp-skill-change.yml -R stromy-org/stromy-org
  Hand-authored skill? Set `_local: true` in frontmatter instead.
-->

# Hosted outreach follow-ups (MCP-hosted skill)

This skill's full instructions are hosted on the `stromy-workflows` MCP server. Do not hardcode workflow logic locally — always fetch the live version from the MCP.

## Before you start — this skill needs the `stromy-workflows` connector

This skill's instructions live on the `stromy-workflows` MCP, which reaches you as an **authorized connector** rather than as part of the plugin. Before step 1 below, check whether this conversation actually has the `stromy-workflows` MCP's tools (`fs_read` / `fs_list`) available to call.

**If those tools are not present at all, STOP — and do not retry.** A missing tool is not a slow server: it means the connector is either not added to this workspace or not switched on for this conversation. Retrying cannot fix it. Tell the user plainly what to do, naming the connector:

> This needs the **Stromy Workflows** connector, which isn't switched on for this chat. Open your connector settings, check it's connected and enabled for this conversation, then ask me again.

Then stop and wait. Never fall back to a local or identically-named base skill, and never answer from your own knowledge instead — an unsourced answer is **wrong output, not a fallback**.

## Loading instructions

1. Read the main skill instructions:
   → call the `fs_read` tool on the `stromy-workflows` MCP with `path="skills/wf-outreach/SKILL.md"`.

   **Read it to the end.** `fs_read` returns one page at a time. If the result's `next_offset_chars` is not null — or the returned text ends in a `<<< PARTIAL READ … >>>` block — the body is incomplete: call `fs_read` again with `offset_chars` set to that value and concatenate, repeating until it comes back null. Do **not** start work on a partial skill body. Hard rules and anti-patterns often sit in the final third, and a partial read fails silently — it looks like a complete skill.

2. Discover reference files (and any other skill assets), then read on demand:
   → call `fs_list` with `path="skills/wf-outreach"` (and `path="skills/wf-outreach/references"`),
   → call `fs_read` with `path="skills/wf-outreach/references/<file>"`.

Follow the instructions returned by the MCP exactly.

## This MCP is the only correct path

Produce this skill's output **only** by following the live SKILL.md fetched above and calling the `stromy-workflows` MCP's own tools. Do **not** substitute a local or identically-named base skill from elsewhere, and do **not** invent your own output path. A locally-produced or unbranded artifact is **wrong output, not a fallback** — it bypasses the server-side brand and quality gates.
