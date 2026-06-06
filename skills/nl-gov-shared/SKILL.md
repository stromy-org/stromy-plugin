---
name: nl-gov-shared
description: "References hub for the Dutch government data skill family (nl-gov-data, tensions, nl-policy-legislative-landscape, nl-parliamentary-positioning, nl-official-issue-framing). Not invoked directly — exists to host canonical specs (portal docs, tool reference, output contract, evidence rules, domain packs) cited by all sibling skills."
---

# nl-gov-shared (MCP-hosted skill)

This skill's full instructions are hosted on the `nl-gov-data` MCP server. Do not hardcode workflow logic locally — always fetch the live version from the MCP.

## Loading instructions

1. Read the main skill instructions:
   → call the `fs_read` tool on the `nl-gov-data` MCP with `path="skills/nl-gov-shared/SKILL.md"`.

2. Discover reference files (and any other skill assets), then read on demand:
   → call `fs_list` with `path="skills/nl-gov-shared"` (and `path="skills/nl-gov-shared/references"`),
   → call `fs_read` with `path="skills/nl-gov-shared/references/<file>"`.

Follow the instructions returned by the MCP exactly.
