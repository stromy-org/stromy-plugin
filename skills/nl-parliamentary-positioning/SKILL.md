---
name: nl-parliamentary-positioning
description: "Map Dutch parliamentary positioning and official political posture from nl-gov-data. Use this whenever the user asks which MPs, factions, committees, ministries, votes, questions, motions, debates, petitions, forums, or official bodies are active around a Dutch policy topic. Produces source-backed PA/PR stakeholder maps, faction/MP activity summaries, committee and ministry maps, forum activity tables, engagement signals, and DOCX-ready client analysis. Do not treat this as public sentiment; it is official parliamentary and institutional positioning."
---

# Dutch Parliamentary Positioning (MCP-hosted skill)

This skill's full instructions are hosted on the `nl-gov-data` MCP server. Do not hardcode workflow logic locally — always fetch the live version from the MCP.

## Loading instructions

1. Read the main skill instructions:
   → call the `fs_read` tool on the `nl-gov-data` MCP with `path="skills/nl-parliamentary-positioning/SKILL.md"`.

2. Discover reference files (and any other skill assets), then read on demand:
   → call `fs_list` with `path="skills/nl-parliamentary-positioning"` (and `path="skills/nl-parliamentary-positioning/references"`),
   → call `fs_read` with `path="skills/nl-parliamentary-positioning/references/<file>"`.

Follow the instructions returned by the MCP exactly.
