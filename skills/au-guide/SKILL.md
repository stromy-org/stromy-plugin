---
name: au-guide
description: "Getting-started guide for researching Australian government, legislation, parliament and public spending — what to ask for, what the Hansard corpus can do that nothing else can, which caveats to expect, and how findings hand off to your branded documents. Use whenever someone asks \"how do I research Australian government/parliament/legislation\", \"what can this do for Australia\", \"how do I get started with AU data\", \"what's in Hansard\", or any orientation question about Australian public-affairs research. Routes to the right workflow and hands off to the document tools; does not itself produce documents."
---
<!--
  GENERATED FILE — DO NOT EDIT.
  Owner:       scripts/sync-mcp-skill-stubs.py (via sync-on-mcp-skill-change.yml)
  Source:      MCPs/au-gov-data/skills/au-guide/SKILL.md
  This workflow pushes DIRECT to this repo's main — a local edit here will be
  overwritten or rejected non-fast-forward. Edit the source, push, then:
    gh workflow run sync-on-mcp-skill-change.yml -R stromy-org/stromy-org
  Hand-authored skill? Set `_local: true` in frontmatter instead.
-->

# AU Guide — getting started with Australian government research (MCP-hosted skill)

This skill's full instructions are hosted on the `au-gov-data` MCP server. Do not hardcode workflow logic locally — always fetch the live version from the MCP.

## Loading instructions

1. Read the main skill instructions:
   → call the `fs_read` tool on the `au-gov-data` MCP with `path="skills/au-guide/SKILL.md"`.

2. Discover reference files (and any other skill assets), then read on demand:
   → call `fs_list` with `path="skills/au-guide"` (and `path="skills/au-guide/references"`),
   → call `fs_read` with `path="skills/au-guide/references/<file>"`.

Follow the instructions returned by the MCP exactly.

## This MCP is the only correct path

Produce this skill's output **only** by following the live SKILL.md fetched above and calling the `au-gov-data` MCP's own tools. Do **not** substitute a local or identically-named base skill from elsewhere, and do **not** invent your own output path. A locally-produced or unbranded artifact is **wrong output, not a fallback** — it bypasses the server-side brand and quality gates.
